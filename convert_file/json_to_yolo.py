import json
import os

def json_to_yolo(data):
    """
    :param data: json文件中撰寫的內容
    :function: 將 labelme標註結束的 json文件，轉換為 yolo格式
    :return: 格式修改完的內容
    """

    # 尋找json文件中的 imageWidth 和 imageHeight，獲取圖片的寬與高
    image_width = data['imageWidth']
    image_height = data['imageHeight']

    yolo_boxes = []

    # 尋找 json文件內全部的 shapes，根據 label名稱進行分類。POL為一類，其餘皆為一類
    for shape in data['shapes']:
        if shape['label'] == 'POL':
            label = 1
        else:
            label = 0

        # 將 label的數值先放入列表中
        box = [label]

        points = shape['points']

        # 由於 yolo格式是要獲取標註點與圖片之間的比值關係，故將其進行運算，並將計算的結果加入當筆列表中
        for point in points:
            x = point[0] / image_width
            y = point[1] / image_height
            box.extend([x, y])

        # 整合此份 json文件中全部所需的資料
        yolo_boxes.append(box)

    return yolo_boxes


json_folder = "D:/json_to_yolo/JQ_0131_to_0205/JQ_0131_to_0205/U600/Train/json_label" # input path: 傳入存放 json文件的資料夾路徑
yolo_labels = "D:/json_to_yolo/JQ_0131_to_0205/JQ_0131_to_0205/U600/Train/txt_label" # output path: 輸出轉為yolo格式txt檔的資料夾路徑

# 讀取在輸入資料夾中的 json檔，並創建同名的 txt檔
for json_file in os.listdir(json_folder):
    if json_file.endswith('.json'):
        json_name = os.path.basename(json_file).split('.')[0]
        output_file = os.path.join(yolo_labels, f'{json_name}.txt')
        jsonfile = os.path.join(json_folder, f'{json_name}.json')

        # 讀取 json檔中的內容，並存入 data變數中
        with open(jsonfile, 'r') as file:
            data = json.load(file)

        # 呼叫 json_to_yolo函數，取得轉換後的結果
        boxes = json_to_yolo(data)

        # 根據回傳的內容完成 txt檔的撰寫
        with open(output_file, 'w') as f:
            for box in boxes:
                result_str = ' '.join(str(data) for data in box)
                f.write(result_str + '\n')
