import cv2
import json

img_path = "temp/images_0.png"
img = cv2.imread(img_path)

with open("temp/images_0.json", "r", encoding="utf-8") as f:
    data = json.load(f)

    info = []

    image_path = data["image_path"].split('\\')[-1]
    w = data["w"]
    h = data["h"]
    mode = data["mode"]


    for item in data["label_info"]:
        x, y, sub_info, link = [], [], {}, []
        id = item
        parent_node = data["label_info"][id]["parent_node"]
        description = data["label_info"][id]["description"]
        polygons = data["label_info"][id]["polygons"]
        recognition = data["label_info"][id]["recognition"]

        if description == "head":
            description = "header"

        coordinate = list(map(float, polygons.split(",")))
        for index in range(len(coordinate)):
            if index % 2 == 0:
                x.append(coordinate[index])
            else:
                y.append(coordinate[index])
        xmin = int(w * min(x))
        xmax = int(w * max(x))
        ymin = int(h * min(y))
        ymax = int(h * max(y))
        tl_point = (xmin, ymin)
        br_point = (xmax, ymax)
        cv2.rectangle(img, tl_point, br_point, (0, 0, 255), 2)

        save_path = "temp/images_1.png"
        cv2.imwrite(save_path, img)


