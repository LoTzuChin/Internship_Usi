import os
from PIL import Image, ImageEnhance

def edit_image(input_image_path, output_image_path, brightness=1.0, saturation=1.0, exposure=1.0, contrast=1.0):
    # 打开图像文件
    image = Image.open(input_image_path)

    # 调整亮度
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness)

    # 调整饱和度
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation)

    # 调整曝光度
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(exposure)

    # 调整对比度
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast)

    # 保存编辑后的图像
    image.save(output_image_path)

def process_images(input_folder, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有图像文件
    image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

    # 定义参数列表
    parameters = [
        (1.3, 0.8, 1.0, 0.7),
        (1.6, 0.7, 1.0, 0.7),
        (0.9, 0.7, 0.6, 1.2),
        (0.7, 0.8, 0.6, 1.2),
        (1.2, 0.7, 0.6, 1.2)
    ]

    # 处理每张图像
    for image_file in image_files:
        input_image_path = os.path.join(input_folder, image_file)

        # 处理每组参数
        for i, (brightness, saturation, exposure, contrast) in enumerate(parameters):
            output_image_path = os.path.join(output_folder, f"{os.path.splitext(image_file)[0]}_{i + 1}.jpg")
            edit_image(input_image_path, output_image_path, brightness, saturation, exposure, contrast)

if __name__ == "__main__":
    input_folder = "GT_IMAGES"
    output_folder = "0504"

    process_images(input_folder, output_folder)