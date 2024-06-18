import xml.etree.ElementTree as ET
import os
import json
from fileMethod import fileInfo
from fileMethod import tableOperation
import xml.dom.minidom

def createObject(annotation, x, y, col, row, x_list, y_list, index):
    """
    在新文件中創建物件
    :param annotation: wtw格式文件內容
    :param x: 當前物件在 x_list中的 index
    :param y: 當前物件在 y_list中的 index
    :param col: 被合併的欄數
    :param row: 被合併的列數
    :param x_list: 該 table在 x軸上的節點
    :param y_list: 該 table 在y軸上的節點
    :param index: table的編號
    :return: 更新的 wtw格式文件內容
    """

    # 創建物件基本資訊欄位及內容
    object = ET.SubElement(annotation, "object")
    name = ET.SubElement(object, "name")
    difficult = ET.SubElement(object, "difficult")
    name.text = "box"
    difficult.text = "0"

    # 創建物件座標及表格資訊欄位
    bndbox = ET.SubElement(object, "bndbox")
    xmin = ET.SubElement(bndbox, "xmin")
    ymin = ET.SubElement(bndbox, "ymin")
    xmax = ET.SubElement(bndbox, "xmax")
    ymax = ET.SubElement(bndbox, "ymax")
    x1 = ET.SubElement(bndbox, "x1")
    y1 = ET.SubElement(bndbox, "y1")
    x2 = ET.SubElement(bndbox, "x2")
    y2 = ET.SubElement(bndbox, "y2")
    x3 = ET.SubElement(bndbox, "x3")
    y3 = ET.SubElement(bndbox, "y3")
    x4 = ET.SubElement(bndbox, "x4")
    y4 = ET.SubElement(bndbox, "y4")
    startcol = ET.SubElement(bndbox, "startcol")
    endcol = ET.SubElement(bndbox, "endcol")
    startrow = ET.SubElement(bndbox, "startrow")
    endrow = ET.SubElement(bndbox, "endrow")
    tableid = ET.SubElement(bndbox, "tableid")

    # 計算座雕相關欄為資訊
    x_end = x + col - 1
    y_end = y + row - 1

    y_len = len(y_list) - 1

    x_min = x_list[x]
    y_min = y_list[y]
    x_max = x_list[x_end + 1]
    y_max = y_list[y_end + 1]

    # 寫入座標表格資訊
    # y軸的部分因為 wtw格式是與座標資訊相反，故需要做倒序處理
    xmin.text = str(x_min)
    ymin.text = str(y_min)
    xmax.text = str(x_max)
    ymax.text = str(y_max)
    x1.text = str(x_min)
    y1.text = str(y_min)
    x2.text = str(x_max)
    y2.text = str(y_min)
    x3.text = str(x_max)
    y3.text = str(y_max)
    x4.text = str(x_min)
    y4.text = str(y_max)
    startcol.text = str(x)
    endcol.text = str(x_end)
    startrow.text = str(y_len - y_end - 1)
    endrow.text = str(y_len - y - 1)
    tableid.text = str(index)

    return annotation

def classifyTable(content, table, w, h):
    """
    通過儲存格座標與 table座標進行比對，確認處在 table
    :param content: 原 json內容
    :param table: table的 list
    :param w: 寬的誤差值
    :param h: 高的誤差值
    :return: 每個 table裡的 item group
    """
    group = [[]]
    for item in content["label_info"]:
        if data["label_info"][item]["description"] == "table":
            pass
        else:
            table_id = 0

            # 取得儲存格資訊
            parent_node, description, points, recognition, shape = fileInfo.getItemInfo(content, item)
            x_min, y_min, x_max, y_max = fileInfo.getRectCoordinate(points)

            # 判斷存在與哪個 table
            while (x_min < (table[table_id][0] - w)) or (y_min < (table[table_id][1] - h)) or (x_max > (table[table_id][2] + w)) or (y_max > (table[table_id][3] + h)):
                table_id += 1
            group[table_id].append(item)

    return group

def searchMergeCell(table, xlist, ylist, annotation, i, xlist_max, ylist_max):
    """
    根據還原的表格結構判斷創建物件，為1則直接創建，為3則確認合併哪些行列，再進行創建
    :param table: 還原的表格結構，由 0,1,2,3呈現
    :param xlist: 該 table在 x軸上的節點
    :param ylist: 該 table在 y軸上的節眼
    :param annotation: wtw格式的內容
    :param i: 處在的 table id
    :param xlist_max: 該 table的 x軸最大值，加入到 xlist中，完善所有節點
    :param ylist_max: 該 table的 y軸最大值，加入到 ylist中，完善所有節點
    :return: wtw格式的內容
    """
    xlist.append(xlist_max)
    ylist.append(ylist_max)
    for y in range(len(table)):
        for x in range(len(table[y])):
            col, row = 1, 1
            # 為 0則直接創建物件
            if table[y][x] == 0:
                annotation = createObject(annotation, x, y, col, row, xlist, ylist, i)
            # 為 3則搜尋合併的行列數，再創建物件
            elif table[y][x] == 3:
                col = colspan_dfs(table, y, x, col, True)
                row = rowspan_dfs(table, y, x, row, True)
                annotation = createObject(annotation, x, y, col, row, xlist, ylist, i)
            else:
                pass
    return annotation



def colspan_dfs(table, i, j, col, check_col = False):
    """
    搜索該格合併了多少行
    :param i: 被搜尋格的位置
    :param j: 被搜尋格的位置
    :param col: 紀錄合併行的數量
    :param check_col: 第一次進來時會是 True，避免誤判
    :return: 返回 col，即為合併行之數量
    """
    if (i >= len(table) or j >= len(table[0]) or table[i][j] == 0 or table[i][j] == 2):
        return col
    elif (table[i][j] == 1):
        col += 1
        return colspan_dfs(table, i, j + 1, col)  # right
    else:
        if check_col:
            return colspan_dfs(table, i, j + 1, col)  # right
        else:
            return col


def rowspan_dfs(table, i, j, row, check_row = False):
    """
    搜索該格合併了多少列
    :param i: 被搜尋格的位置
    :param j: 被搜尋格的位置
    :param row: 記錄合併列的數量
    :param check_row: 第一次進來時會是 True，避免誤判
    :return: 返回 row，即合併列之數量
    """
    if (i >= len(table) or j >= len(table[0]) or table[i][j] == 0 or table[i][j] == 1):
        return row
    elif (table[i][j] == 2):
        row += 1
        return rowspan_dfs(table, i + 1, j, row)  # down
    else:
        if check_row:
            return rowspan_dfs(table, i + 1, j, row)  # down
        else:
            return row

def normalization(xml_file):
    """
    格式化 xml檔
    :param xml_file: 撰寫完成的 xml檔
    :return: None
    """
    dom = xml.dom.minidom.parse(xml_file)

    pretty_xml = dom.toprettyxml()

    line = pretty_xml.replace('\n', '').replace('\t', '')

    new_xml = xml.dom.minidom.parseString(line)
    xml_ok = new_xml.toprettyxml()

    with open(xml_file, 'w') as f:
        f.write(xml_ok)


if __name__ == "__main__":
    json_file = "images_0.json"
    json_name = os.path.basename(json_file).split('.')[0]
    xml_file = f'{json_name}.xml'

    tableinfo = []

    with open(json_file ,'r' ,encoding="utf-8") as file:
        data = json.load(file)

    # 文件的基本資訊欄位與填寫
    annotation = ET.Element("annotation")
    folder = ET.SubElement(annotation, "folder")
    filename = ET.SubElement(annotation, "filename")
    size = ET.SubElement(annotation, "size")
    width = ET.SubElement(size, "width")
    height = ET.SubElement(size, "height")
    depth = ET.SubElement(size, "depth")

    image_path, w, h = fileInfo.getFileInfo(data)

    filename.text = image_path.split('/')[-1]
    width.text = str(w)
    height.text = str(h)
    depth.text = "3"

    # 寬與高的誤差值
    new_w = w / 100
    new_h = h / 100

    # 先尋找有多少個 table
    for item in data["label_info"]:
        if data["label_info"][item]["description"] == "table":
            coordinate = list(map(float, data["label_info"][item]["points"].split(",")))
            tableinfo.append(coordinate)

    item_group = classifyTable(data, tableinfo, new_w, new_h)

    # 根據每個 table進行處理
    for i in range(len(tableinfo)):
        xlist, ylist, xlist_max, ylist_max = tableOperation.getAllXY(data, item_group[i], w, h, new_w, new_h)
        table_struct, table_dict = tableOperation.getTableStruct(data, xlist, ylist, new_w, new_h, w, h)

        annotation = searchMergeCell(table_struct, xlist, ylist, annotation, i, xlist_max, ylist_max)

    tree = ET.ElementTree(annotation)
    tree.write(xml_file)
    normalization(xml_file)