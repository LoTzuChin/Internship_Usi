import os
import shutil


def move_files_from_subfolders(root_folder):
    # 检查输入的路径是否存在
    if not os.path.exists(root_folder):
        print("Error: The specified folder path does not exist.")
        return

    # 递归遍历所有子文件夹
    for foldername, subfolders, filenames in os.walk(root_folder):
        # 检查当前文件夹是否以 "_pic" 结尾
        if foldername.endswith("_pic"):
            # 循环处理当前文件夹中的所有文件

            pic_parent_folder_path = os.path.dirname(foldername)

            for filename in filenames:
                # 构建源文件路径
                source_path = os.path.join(foldername, filename)

                # 构建目标文件路径，即将文件移动到与 "_pic" 文件夹同层级的位置
                destination_path = os.path.join(pic_parent_folder_path, filename)

                # 如果目标文件已经存在，则直接覆盖
                if os.path.exists(destination_path):
                    os.remove(destination_path)

                # 移动文件
                shutil.move(source_path, destination_path)

                print(f"Moved '{filename}' to '{destination_path}'")


# 调用函数，传入要操作的根文件夹路径
root_folder = "2024-03-01~2024-03-03"
move_files_from_subfolders(root_folder)
