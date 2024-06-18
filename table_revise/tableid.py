import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml import etree

def add_coordinates(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        name = obj.find('name')
        new_name = name.text.split('_')[0]
        tableid = name.text.split('_')[1]
        bndbox = obj.find('bndbox')


        # 创建新的子元素
        tableid_elem = ET.Element('tableid')
        tableid_elem.text = str(tableid)
        name.text = str(new_name)

        # 将新元素添加到bndbox后面
        bndbox.append(tableid_elem)

    # 保存修改后的XML文件
    tree.write(xml_file)

# XML文件路径
xml_file = 'zxeCol0yTRKjbOAnzK6rNAAAACMAAQED.xml'


# 添加坐标
add_coordinates(xml_file)
