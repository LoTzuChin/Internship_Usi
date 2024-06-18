import os
import shutil

def move_files_from_subfolders(root_folder):
    # 檢查輸入的路徑是否存在
    if not os.path.exists(root_folder):
        print("Error: The specified folder path does not exist.")
        return

    # 遍歷所有子文件夾
    for foldername, subfolders, filenames in os.walk(root_folder):
        # 檢查當前文件夾是否以 "_xml" 結尾
        if foldername.endswith("_xml"):
            # 獲取更上一層文件夾的路徑
            parent_folder = os.path.dirname(foldername)

            # 獲取父文件夾的名稱
            parent_folder_name = os.path.basename(parent_folder)

            # 分割父文件夾名稱以獲取前半部分
            new_parent_folder_name = parent_folder_name.rsplit("_", maxsplit=1)[0]

            ng_folder = os.path.join(parent_folder, "realNG")
            ok_folder = os.path.join(parent_folder, "OK")

            # 構建新的目標文件夾路徑
            xml_target_folder = os.path.join(os.path.dirname(parent_folder), new_parent_folder_name, "xml", parent_folder_name)
            ng_target_folder = os.path.join(os.path.dirname(parent_folder), new_parent_folder_name, "realNG")
            ok_target_folder = os.path.join(os.path.dirname(parent_folder), new_parent_folder_name, "OK")

            # 如果目標文件夾不存在，則創建它
            if not os.path.exists(xml_target_folder):
                os.makedirs(xml_target_folder)
            if not os.path.exists(ng_target_folder):
                os.makedirs(ng_target_folder)
            if not os.path.exists(ok_target_folder):
                os.makedirs(ok_target_folder)

            # 移動 "_xml" 結尾的文件夾到 xml 目標文件夾
            shutil.move(foldername, xml_target_folder)
            print(f"xml Moved {foldername} to {xml_target_folder}")

            for filename in os.listdir(ng_folder):
                old_file_path = os.path.join(ng_folder, filename)
                new_ng_path = os.path.join(ng_target_folder, filename)
                print(new_ng_path)
                shutil.move(old_file_path, new_ng_path)
                print(f"Moved {old_file_path} to {new_ng_path}")
                os.rmdir(ng_folder)

            for filename in os.listdir(ok_folder):
                old_file_path = os.path.join(ok_folder, filename)
                new_ok_path = os.path.join(ok_target_folder, filename)
                shutil.move(old_file_path, new_ok_path)
                print(f"Moved {old_file_path} to {new_ok_path}")
                os.rmdir(ok_folder)

            os.rmdir(os.path.dirname(foldername))


# 調用函數，傳入要操作的根文件夾路徑
root_folder = "test"
move_files_from_subfolders(root_folder)
