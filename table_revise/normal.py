import xml.etree.ElementTree as ET
import xml.dom.minidom
from xml import etree

def add_coordinates(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()



    dom = xml.dom.minidom.parse(xml_file)

    # 格式化XML文件
    pretty_xml = dom.toprettyxml()

    # print(pretty_xml)

    line = pretty_xml.replace('\n', '').replace('\t', '')
    print(line)

    new_xml = xml.dom.minidom.parseString(line)
    xml_ok = new_xml.toprettyxml()

    print(xml_ok)

    # cleaned_lines = [line for line in lines if line.strip()]
    # cleaned_xml = '\n'.join(cleaned_lines)

    # 写入文件
    with open(output, 'w') as f:
        f.write(xml_ok)



# XML文件路径
xml_file = 'zxeCol0yTRKjbOAnzK6rNAAAACMAAQED.xml'
output = 'out.xml'

# 添加坐标
add_coordinates(xml_file)
