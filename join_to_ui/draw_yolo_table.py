import cv2

def drawline(file_input_path, pic_input_path, pic_output_path):
    """
    通過 yolo格式文件中的數值還原進行繪製，驗證結果
    :param file_input_path: yolo文件地址
    :param pic_input_path: yolo文件對應的圖片地址
    :param pic_output_path: 繪製完成的圖片地址
    :return: None
    """
    img = cv2.imread(pic_input_path)
    h, w, _ = img.shape

    with open(file_input_path, "r") as f:
        temps = f.readlines()

    for temp in temps:
        temp = temp.split()

        x_, y_, w_, h_ = eval(temp[1]), eval(temp[2]), eval(temp[3]), eval(temp[4])

        x1 = w * x_ - 0.5 * w * w_
        x2 = w * x_ + 0.5 * w * w_
        y1 = h * y_ - 0.5 * h * h_
        y2 = h * y_ + 0.5 * h * h_

        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 7)

    cv2.imwrite(pic_output_path, img)

if __name__ == "__main__":
    yolo_file = "images_0.txt"
    pic_input = "images_0.png"
    pic_output = "save_path.png"

    drawline(yolo_file, pic_input, pic_output)
