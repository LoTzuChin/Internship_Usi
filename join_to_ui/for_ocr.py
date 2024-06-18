import os
import random
import shutil
import cv2
from fileMethod import fileInfo
import json

def rewriteFile(id, picPath, jsonPath, datasetPath, type):
    """
    將圖片資訊寫入該 type之 txt
    :param id: 該圖片的 id
    :param picPath: 圖片的路徑
    :param jsonPath: 圖片標註之 json檔路徑
    :param datasetPath: 存放 txt之資料集路徑
    :param type: 分為 train, validation, test
    :return: None
    """
    with open(jsonPath, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data['label_info']:
        mode = data['label_info'][item]['mode']

        if mode == 'OCR' and int(item) == int(id):
            recognition = data['label_info'][item]['recognition']

            match type:
                case 'train':
                    open_txt = 'train.txt'
                case 'validation':
                    open_txt = 'validation.txt'
                case 'test':
                    open_txt = 'test.txt'
                case _:
                    open_txt = ''
                    print("Type error!")

            with open(os.path.join(datasetPath, open_txt), 'a') as f:
                f.write(f"{picPath}\t{recognition}\n")

            f.close()


def cropPicure(input_folder, output_folder):
    """
    根據標註範圍裁切圖片
    :param input_folder: 圖片已標註完成之資料夾 (含 json檔)
    :param output_folder: 存放裁切完成之圖片資料夾
    :return: None
    """
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".jpg"):
                name = filename.split('.')[0]
                jsonName = os.path.join(root, name + '.json')
                picName = os.path.join(root, filename)
                with open(jsonName, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    image_path, w, h = fileInfo.getFileInfo(data)
                image = cv2.imread(picName)

                for item in data["label_info"]:
                    mode = data['label_info'][item]['mode']
                    if mode == 'OCR':
                        points = data['label_info'][item]['points']
                        img = image

                        # 讀取該標註位置之xy值進行圖片裁切
                        xmin, ymin, xmax, ymax = fileInfo.getRectCoordinateToInt(points, w, h)
                        cropped = img[ymin: ymax, xmin: xmax]

                        # 讀取該圖翻轉角度，進行校正
                        angle = int(data['label_info'][item]["description"].split('_')[0])
                        match angle:
                            case  90:
                                rotated_cropped = cv2.rotate(cropped, cv2.ROTATE_90_CLOCKWISE)
                            case 180:
                                rotated_cropped = cv2.rotate(cropped, cv2.ROTATE_180)
                            case 270:
                                rotated_cropped = cv2.rotate(cropped, cv2.ROTATE_90_COUNTERCLOCKWISE)
                            case _:
                                rotated_cropped = cropped

                        if not os.path.exists(output_folder):
                            os.makedirs(output_folder)

                        # 為新圖片及對應之 json重新命名，並加入暫存資料夾 cropped
                        new_name = name + "_" + item + ".jpg"
                        new_json_name = name + "_" + item + '.json'
                        new_path = os.path.join(output_folder, new_name)
                        new_json_path = os.path.join(output_folder, new_json_name)
                        cv2.imwrite(new_path, rotated_cropped)
                        shutil.copy(jsonName, new_json_path)


def randomToDataset(cropped_dir, train_percent, validation_percent):
    """
    根據輸入的比例隨機分配
    :param cropped_dir: 裁切完成之圖片資料夾
    :param train_percent: 訓練集比比例
    :param validation_percent: 驗證集比例
    :return: None
    """
    train_percent = train_percent
    val_percent = validation_percent
    trainval_percent = train_percent + val_percent

    filenames = []

    for root, dirs, files in os.walk(cropped_dir):
        for name in files:
            if name.endswith(".jpg"):
                filenames.append(name)

    filenum = len(filenames)
    # 先將 train + val 的資料及分割出來，再個別分出 train和 val
    num_trainval = int(round(filenum * trainval_percent))
    sample_trainval = random.sample(filenames, num_trainval)
    num_train = int(round(num_trainval * (train_percent / trainval_percent)))

    sample_train = random.sample(sample_trainval, num_train)  # 從 train + val 中取得 train dataset
    sample_val = list(set(sample_trainval).difference(set(sample_train)))  # val 為 train + val中 train 的差集
    sample_test = list(set(filenames).difference(set(sample_trainval)))  # tset 為 全部資料中 train + val 的差集


    return sample_train, sample_val, sample_test


def movePic(sample_list, cropped_dir, dataset_path, type):
    """
    將裁剪好的圖片根據隨機份配移動至指定資料夾
    :param sample_list: 隨機分配後所得之序列
    :param cropped_dir: 裁切好的圖片之資料夾
    :param dataset_path: 存放資料集之路徑
    :param type: 分為 train, validation, test
    :return: None
    """
    for name in sample_list:
        shutil.move(os.path.join(cropped_dir, name), os.path.join(dataset_path, type))
        id = name.split('.')[0].split('_')[-1]
        picPath = os.path.join(dataset_path, type, name)
        jsonName = name.split('.')[0] + '.json'
        jsonPath = os.path.join(cropped_dir, jsonName)
        rewriteFile(id, picPath, jsonPath, dataset_path, type)

    return

def makeDir(dataset_path, type):
    """
    創建尚不存在的資料夾
    :param dataset_path: 路徑
    :param type: 資料夾名稱
    :return: None
    """
    if not os.path.exists(os.path.join(dataset_path, type)):
        os.makedirs(os.path.join(dataset_path, type))

    return


if __name__ == "__main__":

    input_folder = "111" # 輸入資料夾的位置

    main_folder = "0605" # 欲存放的最外層資料夾
    cropped_dir = os.path.join(main_folder, "cropped_pic") # 被裁切圖片的暫時存放區
    dataset = os.path.join(main_folder, "dataset") # 完整資料集位置

    train = "train"
    validation = "validation"
    test = "test"

    train_percent = float(input("train proportion (range: 0~1): "))
    validation_percent = float(input("validation proportion (range: 0~1): "))
    test_percent = 1 - train_percent - validation_percent

    print("--------------------------------------------------")
    print(f"dataset -> train: {train_percent}")
    print(f"           validation: {validation_percent}")
    print(f"           test: {test_percent}")
    print("--------------------------------------------------")

    cropPicure(input_folder, cropped_dir)

    makeDir(dataset, train)
    makeDir(dataset, validation)
    makeDir(dataset, test)

    sample_train, sample_val, sample_test = randomToDataset(cropped_dir, train_percent, validation_percent)

    try:
        movePic(sample_train, cropped_dir, dataset, train)
        movePic(sample_val, cropped_dir, dataset, validation)
        movePic(sample_test, cropped_dir, dataset, test)
        shutil.rmtree(cropped_dir)
    except shutil.Error as e:
        print(f"error: {e}")
        print("The path already exists.")
        a = input("Do you need to remove the folder? y/n: ")
        if a == 'y':
            shutil.rmtree(main_folder)
    except Exception as e:
        print(f"unknow error: {e}")