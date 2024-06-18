def replace_chars(text):
    return text.replace(',', '').replace('[', '').replace(']', '').replace("'", "")

def write_to_html(text):
    with open('output.html', 'w') as f:
        f.write(text)

input_text = input("請輸入一段文字: ")
formatted_text = replace_chars(input_text)
write_to_html(formatted_text)
print("已經將文字寫入output.html檔案中。")
