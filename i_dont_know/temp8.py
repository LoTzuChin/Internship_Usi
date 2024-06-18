import os

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
            parent_folder = os.path.dirname(os.path.dirname(foldername))
            # 讀取更上一層文件夾中所有的名字
            parent_files = os.listdir(parent_folder)

            # 使用 "_" 分割並將名稱添加到集合中
            for file in parent_files:
                # 使用 "_" 分割名稱
                parts = file.rsplit("_", maxsplit=1)
                name = parts[0]  # 取得前面的名稱部分
                new_folder_name = os.path.join(parent_folder, name)
                os.makedirs(new_folder_name, exist_ok=True)  # 使用 exist_ok=True 避免重複創建
                print(f"Created folder: {new_folder_name}")

                # # 在新创建的文件夹内创建 ng, ok, xml 三个文件夹
                # subfolder_names = ['realNG', 'OK', 'xml']
                # for subfolder_name in subfolder_names:
                #     subfolder_path = os.path.join(new_folder_name, subfolder_name)
                #     os.makedirs(subfolder_path, exist_ok=True)
                #     print(f"Created subfolder: {subfolder_path}")

# 調用函數，傳入要操作的根文件夾路徑
root_folder = "test"
move_files_from_subfolders(root_folder)
