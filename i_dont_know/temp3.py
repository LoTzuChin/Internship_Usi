import os

def delete_empty_folders(root_folder):
    for folder_name, subfolders, files in os.walk(root_folder, topdown=False):
        for subfolder in subfolders:
            folder_path = os.path.join(folder_name, subfolder)
            if not os.listdir(folder_path):
                print(f"Deleting empty folder: {folder_path}")
                os.rmdir(folder_path)

# 指定要操作的根目錄
root_folder = 'test'

# 呼叫函式刪除空資料夾
delete_empty_folders(root_folder)
