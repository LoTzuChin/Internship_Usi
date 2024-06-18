def getFileInfo(content):
    """
    取得文件資訊
    :param content:原 json文件內容
    :return: 圖片地址、寬、高
    """
    image_path = content["image_path"].split('\\')[-1]
    w = content["w"]
    h = content["h"]

    return image_path, w, h

def getItemInfo(content, item):
    """
    取得物件資訊
    :param content: 原 json文件內容
    :param item: 物件編號
    :return: parent_node, description, points, recognition, shape
    """
    parent_node = content["label_info"][item]["parent_node"]
    description = content["label_info"][item]["description"]
    points = content["label_info"][item]["points"]
    recognition = content["label_info"][item]["recognition"]
    shape = content["label_info"][item]["shape"]

    return parent_node, description, points, recognition, shape

def getPolyCoordinate(polygons):
    """
    多邊形標註座標
    :param polygons: 物件 points的資料
    :return: x與 y座標的 list
    """
    x, y = [], []
    coordinate = list(map(float, polygons.split(",")))
    for index in range(len(coordinate)):
        if index % 2 == 0:
            x.append(coordinate[index])
        else:
            y.append(coordinate[index])

    return x, y

def getRectCoordinate(points):
    """
    方形標註座標(比值型式)
    :param points: 物件 points的資料
    :return: xy的 min和 max
    """
    coordinate = list(map(float, points.split(",")))

    xmin = coordinate[0]
    ymin = coordinate[1]
    xmax = coordinate[2]
    ymax = coordinate[3]

    return xmin, ymin, xmax, ymax


def getRectCoordinateToInt(points, w, h):
    """
    方形標註座標(整數型態)
    :param points: 物件 points的資料
    :return: xy的 min和 max
    """
    coordinate = list(map(float, points.split(",")))

    xmin = int(coordinate[0] * w)
    ymin = int(coordinate[1] * h)
    xmax = int(coordinate[2] * w)
    ymax = int(coordinate[3] * h)

    return xmin, ymin, xmax, ymax

