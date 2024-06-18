import os
import cv2
import numpy as np

def edit_image(input_image_path, output_image_path, brightness=1.0, exposure=1.0, contrast=1.0, shadow=1.0, highlight=1.0, saturation=1.0):
    # 读取图像
    image = cv2.imread(input_image_path)

    # 调整对比度
    image = cv2.convertScaleAbs(image, alpha=contrast, beta=0)

    # 调整曝光度
    image = cv2.convertScaleAbs(image, alpha=exposure, beta=0)



    # 增强陰影
    shadow_enhanced = cv2.blur(image, (5, 5))
    image = cv2.addWeighted(image, shadow, shadow_enhanced, 1 - shadow, -110)

    # 调整亮度
    image = cv2.convertScaleAbs(image, alpha=brightness, beta=0)

    # 增强亮部
    image = cv2.convertScaleAbs(image, alpha=highlight, beta=0)

    # 调整飽和度
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = np.clip(hsv[:,:,1] * saturation, 0, 255)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # 保存编辑后的图像
    cv2.imwrite(output_image_path, image)

def process_images(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有图像文件
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # 定义参数列表
    parameters = [
        (1.8, 0.7, 1.0, 2.0, 1.5, 0.6)  # (brightness, exposure, contrast, shadow, highlight, saturation)
    ]

    # 处理每张图像
    for image_file in image_files:
        input_image_path = os.path.join(input_folder, image_file)

        # 处理每组参数
        for i, (brightness, exposure, contrast, shadow, highlight, saturation) in enumerate(parameters):
            output_image_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_{i + 1}.jpg")
            edit_image(input_image_path, output_image_path, brightness, exposure, contrast, shadow, highlight, saturation)

if __name__ == "__main__":
    input_folder = "high"
    output_folder = "0506"

    process_images(input_folder, output_folder)
