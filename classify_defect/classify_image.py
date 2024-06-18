import os
import shutil

input_folder = "D:/image_classification/0311"
output_folder = "D:/image_classification/0311_done"

def classify_files(input_folder, output_folder):
    """
    :param input_folder: 輸入文件夾的路徑
    :param output_folder: 輸出文件夾的路徑
    :function: 將文件夾內相同類別的零件圖片，通過其名稱進行分類
    """
    for root, dirs, files in os.walk(input_folder):
        for file in files:

            # 獲取圖片路徑: file_path,和 圖片完整名稱: file_name
            if file.endswith(".jpeg"):
                file_path = os.path.join(root, file)
                file_name = os.path.splitext(file)[0]

                # 獲取圖片所在之文件夾名稱
                # (由於文件夾命名如:[AA001]，有些則會在前面加上數字，如:[001]_[AA001])
                # (故split是為了取得後方英文字，replace則是為了拿掉[])
                dirs_name = os.path.basename(os.path.normpath(root).split('_')[-1].replace('[', '').replace(']', ''))

                # 圖片類別是根據圖片名稱"@"前所決定，如:C0800@50_side.jpeg，因此要找"@"的index
                index = file_name.find("@")
                if index != -1:
                    # 取得類別名稱，並使用其創建同名文件夾
                    prefix = file_name[:index]
                    output_subfolder = os.path.join(output_folder, prefix)
                    if not os.path.exists(output_subfolder):
                        os.makedirs(output_subfolder)

                    # 使用原資料夾名稱與圖片名結合成新的文件名稱
                    new_file_name = f"{dirs_name}_{file}"

                    output_file_path = os.path.join(output_subfolder, new_file_name)

                    # 移動圖片到指定的輸出文件夾
                    shutil.move(file_path,output_file_path)

    for sub_dirs in dirs:
        # 在每個文件夾中檢查是不是還有子文件夾
        sub_dirs_path = os.path.join(root, sub_dirs)
        classify_files((sub_dirs_path, output_folder))


def classify_defect(input_folder, output_folder):
    """
    :param input_folder: 輸入文件夾的路徑
    :param output_folder: 輸出文件夾的路徑
    :function: 在具有相同瑕疵名稱文件夾下的圖片歸類到一起
    """
    for root, dirs, files in os.walk(input_folder):
        for file in files:

            # 獲取原圖片路徑
            if file.endswith(".jpeg"):
                file_path = os.path.join(root, file)
                dir_path = os.path.dirname(root)

                # 原始分類好的圖片會坐落在: stain, shift, missing等文件夾
                # 有些圖片會有不止一種瑕疵, ex: stain_with_shift
                # 通過去除'_with', 可以得到以'_'區隔的瑕疵名稱
                dir_name = os.path.basename(os.path.normpath(root).replace('_with', ''))

                if 'exposure' in dir_name:
                    # 因為 exposure都是建立在各類別的子資料夾中，故分開處理
                    folder_name = os.path.basename(dir_path.replace('_with', ''))
                    output_subfolder = os.path.join(output_folder, folder_name, 'exposure')
                else:
                    # 將瑕疵名稱重新排列，目前是讓它升序排列
                    dir_class = dir_name.split('_')
                    dir_class.sort()

                    # 將list內的名稱通過'_'進行區分，作為新的文件夾名稱
                    class_title = '_'.join(dir_class)
                    output_subfolder = os.path.join(output_folder, class_title)

                if not os.path.exists(output_subfolder):
                    os.makedirs(output_subfolder)

                # 移動圖片到指定文件夾之內
                output_file_path = os.path.join(output_subfolder, file)
                shutil.move(file_path, output_file_path)

    for sub_dirs in dirs:
        # 在每個文件夾中檢查是不是還有子文件夾
        sub_dirs_path = os.path.join(root, sub_dirs)
        classify_defect((sub_dirs_path, output_folder))


if __name__ == '__main__':
    classify_defect(input_folder, output_folder)
    # classify_files(input_folder, output_folder)