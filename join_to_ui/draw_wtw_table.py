import cv2
import xml.etree.ElementTree as ET

def draw_line(xml_file, img_path, save_path):
    """
    通過 wtw格式文件中的 xmin, ymin, xmax, ymax進行繪製，驗證結果
    :param xml_file: 改寫為 xml的文件
    :param img_path: 圖片地址
    :return: None
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    img = cv2.imread(img_path)

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        tl_point = (xmin, ymin)
        br_point = (xmax, ymax)
        cv2.rectangle(img, tl_point, br_point, (0, 0, 255), 7)


        cv2.imwrite(save_path, img)

if __name__ == "__main__":
    img = "images_0.png"
    xml_file = "images_0.xml"
    output_img = "images_0_wtw.png"

    draw_line(xml_file, img, output_img)
