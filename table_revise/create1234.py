import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml import etree

def add_coordinates(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # 添加新的坐标点
        x1 = xmin
        y1 = ymin
        x2 = xmax
        y2 = ymin
        x3 = xmax
        y3 = ymax
        x4 = xmin
        y4 = ymax

        # 创建新的子元素
        x1_elem = ET.Element('x1')
        x1_elem.text = str(x1)
        y1_elem = ET.Element('y1')
        y1_elem.text = str(y1)
        x2_elem = ET.Element('x2')
        x2_elem.text = str(x2)
        y2_elem = ET.Element('y2')
        y2_elem.text = str(y2)
        x3_elem = ET.Element('x3')
        x3_elem.text = str(x3)
        y3_elem = ET.Element('y3')
        y3_elem.text = str(y3)
        x4_elem = ET.Element('x4')
        x4_elem.text = str(x4)
        y4_elem = ET.Element('y4')
        y4_elem.text = str(y4)


        # 将新元素添加到bndbox后面
        bndbox.append(x1_elem)
        bndbox.append(y1_elem)
        bndbox.append(x2_elem)
        bndbox.append(y2_elem)
        bndbox.append(x3_elem)
        bndbox.append(y3_elem)
        bndbox.append(x4_elem)
        bndbox.append(y4_elem)

    # 保存修改后的XML文件
    tree.write(xml_file)


    # dom = xml.dom.minidom.parse(xml_file)

    # 格式化XML文件
    # pretty_xml = dom.toprettyxml()
    #
    # # lines = pretty_xml.split('\n')
    # # cleaned_lines = [line for line in lines if line.strip()]
    # # cleaned_xml = '\n'.join(cleaned_lines)
    #
    # # 写入文件
    # with open(output, 'w') as f:
    #     f.write(pretty_xml)

# XML文件路径
xml_file = 'zxeCol0yTRKjbOAnzK6rNAAAACMAAQED.xml'
output = 'out.xml'

# 添加坐标
add_coordinates(xml_file)
