import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def draw(xml_file):
    """
    通過 wtw格式文件中的 startcol, endcol, startrow, endrow進行表格還原，驗證結果
    :param xml_file: 改寫成 wtw格式的 xml文件
    :return: html格式的表格資料
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    data = []
    first = True

    data.append("<table border=2>")

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        startcol = int(bndbox.find('startcol').text)
        endcol = int(bndbox.find('endcol').text)
        startrow = int(bndbox.find('startrow').text)
        endrow = int(bndbox.find('endrow').text)

        col = endcol - startcol
        row = endrow - startrow

        if startcol == 0 and first:
            data.append("<tr>")
        elif startcol == 0:
            data.append("</tr>")
            data.append("<tr>")

        # 根據是否為合併儲存格做調整
        if col == 0 and row == 0:
            data.append("<td></td>")
        elif col == 0:
            data.append(f"<td rowspan={row+1}></td>")
        elif row == 0:
            data.append(f"<td colspan={col+1}></td>")
        else:
            data.append(f"<td rowspan={row+1} colspan={col+1}></td>")

    data.append("</tr>")
    data.append("</table>")

    return data

if __name__ == "__main__":
    xml_file = "images_0.xml"

    data = draw(xml_file)
    data_string = "".join(str(element) for element in data)

    # 整理改寫好的資料
    soup = BeautifulSoup(data_string, "html.parser")

    with open("output1.html", "w") as file:
        file.write(str(soup))