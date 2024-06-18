import os

def create_ng_folder(root_dir):
    # 遍历根目录下的所有文件和文件夹
    for foldername, subfolders, filenames in os.walk(root_dir):
        # 检查当前文件夹是否以 "_pic" 结尾
        if foldername.endswith("_xml"):
            # 循环处理当前文件夹中的所有文件

            pic_parent_folder_path = os.path.dirname(foldername)
            # 构建"NG"文件夹的路径
            ng_folder = os.path.join(pic_parent_folder_path, 'realNG')
            ok_folder = os.path.join(pic_parent_folder_path, "OK")
            # 在同一层级下创建"NG"文件夹
            os.makedirs(ng_folder, exist_ok=True)
            os.makedirs(ok_folder, exist_ok=True)
            # 找到一个符合条件的子文件夹就退出内层循环


if __name__ == "__main__":
    root_directory = "2024-03-01~2024-03-03"
    create_ng_folder(root_directory)
