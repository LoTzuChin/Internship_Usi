import os
import shutil

def organize_folders(root_dir):
    done_dir = os.path.join(root_dir, 'done')
    if not os.path.exists(done_dir):
        os.makedirs(done_dir)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname.endswith('_pic'):
                pic_dir = os.path.join(dirpath, dirname)
                pic_files = [file for file in os.listdir(pic_dir) if not os.path.isdir(os.path.join(pic_dir, file))]
                if len(pic_files) == 2:
                    new_folder = os.path.join(done_dir, os.path.relpath(dirpath, root_dir).lstrip('./'), dirname)
                    if not os.path.exists(new_folder):
                        os.makedirs(new_folder)
                    for pic_file in pic_files:
                        shutil.move(os.path.join(pic_dir, pic_file), new_folder)
                    if not os.listdir(pic_dir):
                        os.rmdir(pic_dir)

            if dirname.endswith('_xml'):
                xml_dir = os.path.join(dirpath, dirname)
                new_folder = os.path.join(done_dir, os.path.relpath(dirpath, root_dir).lstrip('./'), dirname)
                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)
                for xml_file in os.listdir(xml_dir):
                    shutil.move(os.path.join(xml_dir, xml_file), new_folder)
                if not os.listdir(xml_dir):
                    os.rmdir(xml_dir)

if __name__ == "__main__":
    root_directory = "2024-03-01~2024-03-03"
    organize_folders(root_directory)
