import xml.etree.ElementTree as ET

def remove_elements(xml_file, elements_to_remove):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for element_name in elements_to_remove:
        for elem in root.findall(element_name):
            root.remove(elem)

    tree.write(xml_file)

# 要删除的元素列表
elements_to_remove = ['folder', 'path', 'source', 'database', 'segmented', 'pose', 'truncated']

# XML文件路径
xml_file = 'zxeCol0yTRKjbOAnzK6rNAAAACMAAQED.xml'

# 删除元素
remove_elements(xml_file, elements_to_remove)
