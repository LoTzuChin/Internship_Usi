import xml.etree.ElementTree as ET

def add_coordinates(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # 在ymax后添加新字段
        startcol = ET.Element('startcol')
        startcol.text = str(get_index(xmin, x_list))
        endcol = ET.Element('endcol')
        endcol.text = str(get_index(xmax, x_list)-1)
        startrow = ET.Element('startrow')
        startrow.text = str(get_index(ymax, y_list))
        endrow = ET.Element('endrow')
        endrow.text = str(get_index(ymin, y_list)-1)

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
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        # 检查xmin和xmax
        should_add_xmin = all(abs(x - xmin) > 5 for x in x_list)
        should_add_xmax = all(abs(x - xmax) > 5 for x in x_list)
        if should_add_xmin:
            x_list.append(xmin)
        if should_add_xmax:
            x_list.append(xmax)

        # 检查ymin和ymax
        should_add_ymin = all(abs(y - ymin) > 5 for y in y_list)
        should_add_ymax = all(abs(y - ymax) > 5 for y in y_list)
        if should_add_ymin:
            y_list.append(ymin)
        if should_add_ymax:
            y_list.append(ymax)

    # 对列表进行排序
    x_list.sort()
    y_list.sort(reverse=True)

    print(x_list)
    print(y_list)

def get_index(value, lst):
    for i, x in enumerate(lst):
        if abs(x - value) <= 5:
            return i
    return -1

# XML文件路径
xml_file = 'zxeCol0yTRKjbOAnzK6rNAAAACMAAQED.xml'

x_list = []
y_list = []
# 第一步：添加坐标

# 第二步：对坐标进行排序
sort_coordinates(xml_file)
add_coordinates(xml_file)