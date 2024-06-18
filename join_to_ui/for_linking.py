import json
from datetime import datetime
import time
from fileMethod import fileInfo


def rewrite_file(content):

    # info list用於存放改寫後的內容
    info = []

    # 紀錄 question的編號，避免 answer對不上 question
    question_ids = set()

    # 取得該文件之 地址、寬、高
    image_path, w, h = fileInfo.getFileInfo(content)

    # 由於 question的編號是看item，answer則是看 parent_node，故建立 num dict，存放 item與 parent_node的對應關係
    number = {}

    # 紀錄當前時間，用於圖片命名
    current = datetime.now()
    msec = int(time.perf_counter() * 1000)
    record_name = f"{current.year}_{current.month}_{current.day}_{current.hour}_{current.minute}_{current.second}_{msec}.png"

    # 遍歷所有 item
    for item in content["label_info"]:
        x, y, sub_info, link = [], [], {}, []
        # 紀錄 item編號
        seq_num = int(item)

        # 取得 parent_node, description, points, recognition, shape
        parent_node, description, points, recognition, shape = fileInfo.getItemInfo(content, item)

        # 判斷 shape種類
        if shape != "Rect":
            raise ValueError(f"id:{item} is polygon.")

        else:
            # 紀錄 parent_node編號
            id = int(parent_node.split("-")[0])

            # 根據文件需求，取得整數型態的xy值
            xmin, ymin, xmax, ymax = fileInfo.getRectCoordinateToInt(points, w, h)


            # 記錄除 answer之外的 item與 parent_node之間的關係
            if description == "answer":
                pass
            else:
                number[id] = seq_num


            # 原標註文件的 head改為 header
            if description == "head":
                description = "header"
            # 紀錄 question的編號
            elif description == "question":
                question_ids.add(id)
            # answer尋找對應的 question編號，若找不到輸出錯誤訊息
            elif description == "answer":
                question_id = id
                if question_id not in question_ids:
                    raise ValueError(
                        f"Error: Answer with ID {id} is referencing a non-existent question ID {question_id} in {image_path}")


            # recognition = 新文件的 transcription
            sub_info["transcription"] = recognition
            # description = 新文件的 label
            sub_info["label"] = description
            # 將四個座標節點寫入 point
            sub_info["point"] = [[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]


            # 通過"-"判斷當前標註內容的層級
            # 若為1，則當前物件非answer，無須 linking
            # 反之，若為2則需要
            check_layer = parent_node.split("-")
            if len(check_layer) == 1:
                sub_info["id"] = seq_num
                sub_info["linking"] = []
            elif len(check_layer) == 2:
                link = [number[int(check_layer[0])], seq_num]
                sub_info["id"] = seq_num
                sub_info["linking"] = [link]

            info.append(sub_info)

    record = f"{record_name}\t{json.dumps(info, ensure_ascii=False)}\n"
    return record


if __name__ == "__main__":
    input_file = "images_4.json"
    output_file = "temp/output.json"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    try:
        rewrite_data = rewrite_file(data)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(rewrite_data)
    except Exception as e:
        print(e)
