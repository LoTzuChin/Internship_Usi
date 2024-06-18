import json
import os
import shutil
from datetime import datetime
import time


def rewrite_text(input_folder, img_dir):
    # 紀錄 question 的 id，用於確認 answer 的 linking 是否正確
    question_ids = set()
    sub_question_ids = set()
    rewritten_lines = []
    img_id = 0
    timestamp_msec = int(time.perf_counter() * 1000)

    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".txt"):
                input_file = os.path.join(root, filename)
                question_ids.clear()
                sub_question_ids.clear()
                with open(input_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line in lines:
                    currentDateAndTime = datetime.now()
                    timestamp_msec = int(time.perf_counter() * 1000)
                    print(timestamp_msec)
                    parts = line.strip().split('\t')
                    # 標註的文件名稱，ex：报关进口PDF-202450410.pdf/images_2.png
                    orig_filename = parts[0]
                    orig_filename = (orig_filename.split("/"))[-1]
                    img_id += 1

                    # 复制并重命名图片文件
                    new_filename = f"{currentDateAndTime.year}_{currentDateAndTime.month}_{currentDateAndTime.day}_{currentDateAndTime.hour}_{currentDateAndTime.minute}_{currentDateAndTime.second}_{timestamp_msec}.png"
                    shutil.copyfile(os.path.join(root, orig_filename), os.path.join(img_dir, new_filename))

                    data = json.loads(parts[1])

                    for item in data:
                        sub = False
                        label_name = item["key_cls"].split('_')
                        if item["key_cls"].split('_')[0] == "sub":
                            item.clear()


                        else:
                            item["label"] = item["key_cls"].split('_')[0]
                            item["id"] = int(item["key_cls"].split('_')[1])


                            # 先保存 label 和 points 的值
                            label = item.pop("label")
                            points = item.pop("points")
                            id = item.pop("id")

                            # 將 label 和 points 的值插入回去，但位置已經調換了
                            item["label"] = label
                            item["points"] = points
                            item["id"] = id

                            # 如果 label 是 question 的話，將 id 加到 question_ids 的 set 中
                            if item["label"] == "question":
                                question_ids.add(id)
                            # elif item["label"] == 'sub_question':
                            #     sub_question_ids.add(id)
                                # print(item["id"])
                            # print(id)
                            if item["label"] == "head":
                                item["label"] = "header"

                            # 判斷該行是否有 linking
                            # if sub:
                            #     if len(item["key_cls"].split('_')) > 3:
                            #         answer_id = int(item["key_cls"].split('_')[2])
                            #         question_id = int(item["key_cls"].split('_')[3])
                            #         # 確認被 answer linking 的 question 存在
                            #         if item["label"] == "sub_answer":
                            #             if question_id not in sub_question_ids:
                            #                 raise ValueError(
                            #                     f"Error: Answer with ID {item['id']} is referencing a non-existent question ID {question_id} in {parts}")
                            #         item["linking"] = [[question_id, answer_id]]
                            #     else:
                            #         item["linking"] = []
                            # else:
                            if len(item["key_cls"].split('_')) > 2:
                                answer_id = int(item["key_cls"].split('_')[1])
                                question_id = int(item["key_cls"].split('_')[2])
                                # 確認被 answer linking 的 question 存在
                                if item["label"] == "answer":
                                    if question_id not in question_ids:
                                        raise ValueError(f"Error: Answer with ID {item['id']} is referencing a non-existent question ID {question_id} in {parts}")
                                item["linking"] = [[question_id, answer_id]]
                            else:
                                item["linking"] = []

                            del item["difficult"]
                            del item["key_cls"]

                    # 更新文件名
                    rewritten_line = f"{new_filename}\t{json.dumps(data, ensure_ascii=False)}\n"
                    print(rewritten_line)
                    rewritten_lines.append(rewritten_line)

    return rewritten_lines



def save_as_json(rewritten_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(rewritten_data)


if __name__ == "__main__":
    input_folder = "regular_data"
    output_file = "label/Label.json"

    img_label_dir = "label"
    img_dir = "label/image"

    if not os.path.exists(img_label_dir):
        os.makedirs(img_label_dir)
        os.makedirs(img_dir)

    try:
        rewritten_data = rewrite_text(input_folder, img_dir)
        save_as_json(rewritten_data, output_file)
    except ValueError as e:
        print(e)
