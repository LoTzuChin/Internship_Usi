import pymongo
import json
import os

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client.test
collection = db.test_for_label

json_file = "D:/test_for_mongodb/json_label/20240201014414_AVC601100AP730A3C09_T@U600_60_top.json"
with open(json_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 提取所需字段并构建 MongoDB 文档
documents = []
for shape in data['shapes']:
    document = {
        'label': shape['label'],
        'points': shape['points']
    }
    documents.append(document)

# 添加图片的高度和宽度信息
image_info = {
    '_id': os.path.basename(json_file),
    'imageHeight': data['imageHeight'],
    'imageWidth': data['imageWidth']
}

# 将数据插入到 MongoDB 集合中
result = collection.insert_one({**image_info, 'shapes': documents})

print(result)