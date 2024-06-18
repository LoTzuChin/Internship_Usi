import os
import shutil
import xml.etree.ElementTree as ET

def generate_new_file_name(img_name, c_model, part_no):
    """
    用於將圖片名稱進行修改、插入，達到目標名稱之方法
    :param img_name: 圖片名稱
    :param c_model: cModel編號
    :param part_no: PartNo編號
    :return: 新的 img_name
    """

    # 原圖片命名規則：20240301050000_8503eace-abe9-4264-9e37-c752de118389_T@C500_8_side.jpg
    # 欲將中間插入cModel和 PartNo的編號，故須先將"@"前後先拆開再重新組合
    index = img_name.find("@")
    if index != -1:
        before_at = img_name[:index] # @ 之前：20240301050000_8503eace-abe9-4264-9e37-c752de118389_T
        after_at = img_name[index + 1:] # @ 之後：C500_8_side.jpg

        # 新命名規則
        new_file_name = f"{before_at}@{c_model}@{part_no}@{after_at}"

        return new_file_name
    else:
        return img_name

def move_files(root_dir, defect_type):

    # 定義圖片及xml的資料夾
    img_output_dir = f'{defect_type.lower()}_pic'
    xml_output_dir = f'{defect_type.lower()}_xml'

    # 遍歷資料夾
    for subdir, dirs, files in os.walk(root_dir):

        # 建構新資料夾最外層，以日期進行命名：2024-03-01~2024-03-03
        dir_class = os.listdir(root_dir)
        dir_class.sort()
        class_title = '~'.join([dir_class[0], dir_class[-1]])

        for file in files:
            if file.endswith('.xml'):
                xml_file_path = os.path.join(subdir, file)
                # 將xml解析成樹狀結構，並獲取此份xml的根節點
                tree = ET.parse(xml_file_path)
                root = tree.getroot()

                # 尋找符合定義之 defect_type
                for component in root.findall('.//Component'):
                    for window in component.findall('.//Window'):
                        machine_defect = window.get('MachineDefect')
                        if machine_defect == defect_type:

                            # 存取該物件 cModel、PartNo、CompName之編號
                            c_model = root.get('cModel')
                            part_no = component.get('PartNo')
                            component_name = component.get('CompName')

                            # 將具有欲尋找之defect_type圖片地址儲存，含 top和 side
                            pic_path_1 = window.get('PicPath1')
                            pic_path_2 = window.get('PicPath2')

                            # img_path_1和 img_path_2儲存了原始圖片路徑
                            img_path_1 = os.path.join(root_dir, pic_path_1)
                            img_path_2 = os.path.join(root_dir, pic_path_2)

                            # 新存入 image與 xml的文件夾路徑
                            img_output_path = os.path.join(class_title, c_model, part_no, component_name, img_output_dir)
                            xml_output_path = os.path.join(class_title, c_model, part_no, component_name, xml_output_dir)

                            # 將圖片複製到新文件夾中並重新命名
                            if not os.path.exists(img_output_path):
                                os.makedirs(img_output_path)
                            new_img_name_1 = generate_new_file_name(os.path.basename(pic_path_1), c_model, part_no)
                            new_img_name_2 = generate_new_file_name(os.path.basename(pic_path_2), c_model, part_no)
                            shutil.copy(img_path_1, os.path.join(img_output_path, new_img_name_1))
                            shutil.copy(img_path_2, os.path.join(img_output_path, new_img_name_2))

                            # 將 xml複製到新文件夾中
                            if not os.path.exists(xml_output_path):
                                os.makedirs(xml_output_path)
                            shutil.copy(xml_file_path, xml_output_path)

                            break
                        else:
                            continue



if __name__ == "__main__":

    root_dir = 'original_data'

    # 調用函數，defect_type須根據欲分類之缺陷進行修改
    move_files(root_dir, 'Billboard')
    print("billboard done")
    move_files(root_dir, 'Bridge')
    print("bridge done")
    move_files(root_dir, 'Broken')
    print("broken done")
    move_files(root_dir, 'Flipover')
    print("flipover done")
    move_files(root_dir, 'General')
    print("general done")
    move_files(root_dir, 'Missing')
    print("missing done")
    move_files(root_dir, 'Part incline')
    print("part incline done")
    move_files(root_dir, 'Polarity')
    print("polarity done")
    move_files(root_dir, 'Shift')
    print("shift done")
    move_files(root_dir, 'Tombstone')
    print("tombstone done")
    move_files(root_dir, 'Wrong Part')