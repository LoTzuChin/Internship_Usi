import json
import os

def json_to_yolo(data):
    """
    將 標註結束的 json文件，轉換為 yolo格式
    :param data: json文件中撰寫的內容
    :return: 格式修改完的內容
    """
    yolo_boxes = []

    # 尋找 json文件內全部的item
    # 根據 mode進行分類。分為:OCR、Standard，和 其他
    for item in data['label_info']:
        mode = data['label_info'][item]['mode']

        match mode:
            case "OCR":
                label = 0
            case "Standard":
                label = 1
            case _:
                label = 2

        # 將 label的數值先放入列表中
        box = [label]

        # 因為標住格式已為比值關係，故根據格式整理，並直接插入列表中
        polygons = data["label_info"][item]["points"]
        coordinate = list(map(float, polygons.split(",")))
        box.extend(coordinate)

        # 整合此份 json文件中全部所需的資料
        yolo_boxes.append(box)

    return yolo_boxes

if __name__ =="__main__":
    json_folder = "111/222/333" # input path: 傳入存放 json文件的資料夾路徑
    yolo_labels = "123" # output path: 輸出轉為yolo格式txt檔的資料夾路徑

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


    # # 上面是處理整個資料夾，如果只用單一文件請參考下方程式
    # json_file = "images_4.json"
    # yolo_path = "111"
    #
    # json_name = os.path.basename(json_file).split('.')[0]
    # output_file = os.path.join(yolo_path, f'{json_name}.txt')
    #
    # # 讀取 json檔中的內容，並存入 data變數中
    # with open(json_file, 'r', encoding="utf-8") as file:
    #     data = json.load(file)
    #
    # # 呼叫 json_to_yolo函數，取得轉換後的結果
    # boxes = json_to_yolo(data)
    #
    # # 根據回傳的內容完成 txt檔的撰寫
    # with open(output_file, 'w') as f:
    #     for box in boxes:
    #         result_str = ' '.join(str(data) for data in box)
    #         f.write(result_str + '\n')