import os
import shutil

def move_images_to_ok_folder(root_dir):
    # 遍歷目錄中的所有項目
    for root, dirs, files in os.walk(root_dir):
        # 檢查是否有名為'OK'的子資料夾
        if 'OK' in dirs:
            ok_folder = os.path.join(root, 'OK')
            # 找到同一層級的圖片文件
            images = [os.path.join(root, name) for name in files if name.endswith(('.jpg', '.jpeg', '.png'))]
            # 將圖片移動到'OK'子資料夾
            for image in images:
                shutil.move(image, ok_folder)
                print(f'Moved {image} to {ok_folder}')

# 指定根目錄路徑
root_dir = 'test'

# 呼叫函式開始移動圖片
move_images_to_ok_folder(root_dir)