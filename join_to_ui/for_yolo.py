import os
import json
from fileMethod import fileInfo
from fileMethod import tableOperation

def rewriteFile(content, table_dic):
    """
    重寫新文件
    :param content: 原 json內容
    :param table_dic: 是否為合併儲存格的對應字典
    :return: 重寫完成的內容
    """
    boxes = []
    for item in content['label_info']:

        box = []
        if content['label_info'][item]['description'] != 'table':
            isMergeCell = table_dic[item]
        mode = content['label_info'][item]['mode']

        if mode == 'OCR':
            description = content['label_info'][item]['description']

            # 0: 有文字且非合併儲存格(對應原 json文件為answer)
            # 1: 欄位(對應原 json文件為question)
            # 2: 合併儲存格
            # 3: 整個table
            match description:
                case 'question':
                    num = 1
                case 'answer':
                    if isMergeCell == 0:
                        num = 0
                    else:
                        num = 2
                case 'table':
                    num = 3
                case _:
                    num = 5
                    print("Type error!")

            xmin, ymin, xmax, ymax = fileInfo.getRectCoordinate(content['label_info'][item]["points"])

            # 根據 yolo格式所需進行改寫
            x_ = (xmin + xmax) * 0.5
            y_ = (ymin + ymax) * 0.5
            w_ = (xmax - xmin)
            h_ = (ymax - ymin)


            box.append(f"{num} {x_} {y_} {w_} {h_}")
            boxes.append(box)

    return boxes


if __name__ == "__main__":
    json_file = "images_0.json"
    json_name = os.path.basename(json_file).split('.')[0]
    output_file = f'{json_name}.txt'

    with open(json_file ,'r' ,encoding="utf-8") as file:
        data = json.load(file)

    imagePath, w, h = fileInfo.getFileInfo(data)

    new_w = w / 100
    new_h = h / 100

    xlist, ylist, x_max, y_max = tableOperation.getAllXY(data, data["label_info"], w, h, new_w, new_h)


    table_struct, table_dict = tableOperation.getTableStruct(data, xlist, ylist, new_w, new_h, w, h)

    boxes = rewriteFile(data, table_dict)

    with open(output_file, 'w') as f:
        for box in boxes:
            result_str = ' '.join(str(data) for data in box)
            f.write(result_str + '\n')