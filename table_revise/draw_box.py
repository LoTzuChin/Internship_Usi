import cv2
import xml.etree.ElementTree as ET

def draw_line(xml_file, img_path):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    img = cv2.imread(img_path)

    for obj in root.findall('object'):
        bndbox = obj.find('bndbox')
        name = obj.find('name')
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)

        tl_point = (xmin, ymin)
        br_point = (xmax, ymax)
        cv2.rectangle(img, tl_point, br_point, (0, 0, 255), 7)

        save_path = "save/images_0.png"
        cv2.imwrite(save_path, img)

img = "images_0.png"
xml_file = "images_0.xml"

draw_line(xml_file, img)
