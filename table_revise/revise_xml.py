import os
import xml.etree.ElementTree as ET
import xml.dom.minidom

def remove_elements(xml_file, elements_to_remove, element_in_object):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for element_name in elements_to_remove:
        for elem in root.findall(element_name):
            root.remove(elem)

    for element in element_in_object:
        for obj in root.findall('object'):
            for elem in obj.findall(element):
                # print(elem)
                obj.remove(elem)

    tree.write(xml_file)


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

def add_col_row(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        name = obj.find('name')
        tableid = int(name.text.split('_')[1])
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # 在ymax后添加新字段
        startcol = ET.Element('startcol')
        startcol.text = str(get_index(xmin, x_list[tableid]))
        endcol = ET.Element('endcol')
        endcol.text = str(get_index(xmax, x_list[tableid])-1)
        startrow = ET.Element('startrow')
        startrow.text = str(get_index(ymax, y_list[tableid]))
        endrow = ET.Element('endrow')
        endrow.text = str(get_index(ymin, y_list[tableid])-1)

        bndbox.append(startcol)
        bndbox.append(endcol)
        bndbox.append(startrow)
        bndbox.append(endrow)

    tree.write(xml_file)

def sort_coordinates(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()


    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        name = obj.find('name')
        tableid = int(name.text.split('_')[1])
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # for x in x_list[tableid]:
        #     if all(abs(x - xmax) > 15):
        #         index = x_list[tableid].index(x)
        #         nex_xmin = (x + xmin) / 2
        #         x_list[tableid][index] = nex_xmin
        #     else:
        #         x_list[tableid].append(xmin)
        #
        # for x in x_list[tableid]:
        #     if all(abs(x - xmax) > 15):
        #         index = x_list[tableid].index(x)
        #         nex_xmax = (x + xmax) / 2
        #         x_list[tableid][index] = nex_xmax
        #     else:
        #         x_list[tableid].append(xmax)
        #
        # for y in y_list[tableid]:
        #     if all(abs(y - ymax) > 15):
        #         index = y_list[tableid].index(y)
        #         nex_ymin = (y + ymin) / 2
        #         y_list[tableid][index] = nex_ymin
        #     else:
        #         x_list[tableid].append(xmin)
        #
        # for y in y_list[tableid]:
        #     if all(abs(y - ymax) > 15):
        #         index = y_list[tableid].index(y)
        #         nex_ymax = (y + ymax) / 2
        #         y_list[tableid][index] = nex_ymax
        #     else:
        #         y_list[tableid].append(ymax)

        # 检查xmin和xmax
        should_add_xmin = all(abs(x - xmin) > 5 for x in x_list[tableid])
        should_add_xmax = all(abs(x - xmax) > 5 for x in x_list[tableid])
        if should_add_xmin:
            x_list[tableid].append(xmin)
        if should_add_xmax:
            x_list[tableid].append(xmax)

        # 检查ymin和ymax
        should_add_ymin = all(abs(y - ymin) > 5 for y in y_list[tableid])
        should_add_ymax = all(abs(y - ymax) > 5 for y in y_list[tableid])
        if should_add_ymin:
            y_list[tableid].append(ymin)
        if should_add_ymax:
            y_list[tableid].append(ymax)

    # 对列表进行排序
        x_list[tableid].sort()
        y_list[tableid].sort(reverse=True)

        for i in range(len(x_list[tableid])-1):
            if x_list[tableid][i+1] - x_list[tableid][i] < 15:
                x_list[tableid][i] = (x_list[tableid][i] + x_list[tableid][i+1]) / 2




def add_tableid(xml_file):
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

def normalization(xml_file):
    dom = xml.dom.minidom.parse(xml_file)

    # 格式化
    pretty_xml = dom.toprettyxml()


    line = pretty_xml.replace('\n', '').replace('\t', '')

    new_xml = xml.dom.minidom.parseString(line)
    xml_ok = new_xml.toprettyxml()

    # 写入文件
    with open(xml_file, 'w') as f:
        f.write(xml_ok)


def get_index(value, lst):
    # print(lst)
    for i, x in enumerate(lst):
        if abs(x - value) <= 20:
            return i
    return -1

def tablenum(xml_file, x_list, y_list):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    temp = 0

    for obj in root.findall('object'):
        name = obj.find('name')
        tableid = int(name.text.split('_')[1])+1

        if temp < tableid:
            temp = tableid

    for num in range(temp):
        x_list.append([])
        y_list.append([])

    # 保存修改后的XML文件
    tree.write(xml_file)




if __name__ == '__main__':

    elements_to_remove = ['folder', 'path', 'source', 'database', 'segmented' ]
    element_in_object = ['pose', 'truncated']

    xml_file = ""

    path = "000092444"

    files = os.listdir(path)

    for file in files:
        if file.endswith('.xml'):
            xml_file = os.path.join(path, file)

            x_list = []
            y_list = []
            add_coordinates(xml_file)
            remove_elements(xml_file, elements_to_remove, element_in_object)
            tablenum(xml_file, x_list, y_list)
            sort_coordinates(xml_file)
            print(x_list)
            print(y_list)
            add_col_row(xml_file)
            add_tableid(xml_file)
            normalization(xml_file)
            print({xml_file})
