import os
import shutil
import xml.etree.ElementTree as ET
root = 'original_data'

defects_set = set()

for subdir, dirs, files in os.walk(root):
    for file in files:
        if file.endswith('.xml'):
            xml_file_path = os.path.join(subdir, file)
            # 將xml解析成樹狀結構，並獲取此份xml的根節點
            tree = ET.parse(xml_file_path)
            root = tree.getroot()

            # 尋找所有的 MachineDefect
            for component in root.findall('.//Component'):
                for window in component.findall('.//Window'):
                    machine_defect = window.get('MachineDefect')
                    defects_set.add(machine_defect)

# 將找到的 MachineDefect 轉換為排序後的列表
sorted_defects = sorted(defects_set)

# 印出排序後的 MachineDefect
for defect in sorted_defects:
    print(defect)
