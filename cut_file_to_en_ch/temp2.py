# 判断是否包含中文字符的函数
def contains_chinese(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False

# 原始双语文件路径
input_file_path = 'output.txt'

# 中文文件和英文文件路径
chinese_file_path = 'chinese.txt'
english_file_path = 'english.txt'

# 打开双语文件
with open(input_file_path, 'r', encoding='utf-8') as input_file, \
        open(chinese_file_path, 'w', encoding='utf-8') as chinese_file, \
        open(english_file_path, 'w', encoding='utf-8') as english_file:

    for line in input_file:
        if contains_chinese(line):
            # 如果包含中文字符，写入中文文件
            chinese_file.write(line)
        else:
            # 否则，写入英文文件
            english_file.write(line)

print("分离完成")
