import json
from PIL import Image

def rewrite_text(input_file):
    imgid = 0
    idx_x = 0
    idx_y = 0

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split('\t')

        orig_filename = parts[0]
        orig_filename = (orig_filename.split('/'))[-1]
        converted_data = {"filename": orig_filename, "split": " ", "imgid": imgid, "html": {"cell": []}, "structure": {"tokens":[]}}

        data = json.loads(parts[1])

        for item in data:
            check = True
            x_index, y_index = 0, 0
            x_control, y_control = True, True
            the_first = True
            x_index_tab, y_index_tab = 0, 0

            xmin, xmax, ymin, ymax = sort(item)

            while(check):
                if abs(x_list[x_index] - xmin) < table_w:
                    if abs(y_list[y_index] - ymin) < table_h:
                        bbox = [xmin, ymin, xmax, ymax]
                        token = list(item['transcription'])
                        table[y_index][x_index] = f'{{"tokens": {token}, "bbox": {bbox}}}'
                        check = False
                    else:
                        y_index += 1
                        y_index = y_index % len(y_list)
                else:
                    x_index += 1
                    x_index = x_index % len(x_list)


            while x_control:
                x_index_tab += 1
                if not x_index_tab % len(x_list) == 0:
                    if xmax > x_list[x_index_tab] + 1:
                        continue
                    else:
                        x_control = False
                else:
                    x_control = False

            while y_control:
                y_index_tab += 1
                if not y_index_tab % len(y_list) == 0:
                    if ymax > y_list[y_index_tab] + 1:
                        continue
                    else:
                        y_control = False
                else:
                    y_control = False


            for i in range(x_index, x_index_tab):
                for j in range(y_index, y_index_tab):
                    if the_first:
                        table_struct[j][i] = 0
                        idx_x = i
                        idx_y = j
                        the_first = False
                    else:
                        table_struct[idx_y][idx_x] = 3
                        if(i > idx_x):
                            table_struct[j][i] = 1
                        elif(j > idx_y):
                            table_struct[j][i] = 2
        for row in table:

            for cell_data_str in row:
                cell_data = eval(cell_data_str)
                converted_data["html"]["cell"].append(cell_data)


        return converted_data


def table_html(converted_data):
    """
    通過解讀表格結構，將其轉為xml格式
    :param converted_data: 要寫進文件中的資料
    :return: 新增完成之converted_data
    """
    converted_data["structure"]["tokens"].append("<tbody>")
    for y in range(len(table_struct)):
        converted_data["structure"]["tokens"].append("<tr>")
        for x in range(len(table_struct[y])):
            col, row = 1, 1
            if table_struct[y][x] == 0:
                content = "<td>" + "</td>"
                converted_data["structure"]["tokens"].append(content)
            elif table_struct[y][x] == 3:
                col = colspan_dfs(y, x, col, True)
                row = rowspan_dfs(y, x, row, True)
                if (col > 1 and row > 1):
                    content = "<td" + " rowspan=\"" + str(row) + "\"" + " colspan=\"" + str(col) + "\"" + ">" + "</td>"
                elif(col > 1):
                    content = "<td" + " colspan= \"" + str(col) + "\"" + ">" + "</td>"
                elif(row > 1):
                    content = "<td" + " rowspan= \"" + str(row) + "\"" + ">" + "</td>"
                else:
                    content = "<td>" + "</td>"
                converted_data["structure"]["tokens"].append(content)
            else:
                pass
        converted_data["structure"]["tokens"].append("</tr>")
    converted_data["structure"]["tokens"].append("</tbody>")
    return converted_data


def colspan_dfs(i, j, col, check_col = False):
    """
    搜索該格合併了多少行
    :param i: 被搜尋格的位置
    :param j: 被搜尋格的位置
    :param col: 紀錄合併行的數量
    :param check_col: 第一次進來時會是 True，避免誤判
    :return: 返回 col，即為合併行之數量
    """
    if (i >= len(table_struct) or j >= len(table_struct[0]) or table_struct[i][j] == 0 or table_struct[i][j] == 2):
        return col
    elif (table_struct[i][j] == 1):
        col += 1
        return colspan_dfs(i, j + 1, col)  # right
    else:
        if check_col:
            return colspan_dfs(i, j + 1, col)  # right
        else:
            return col


def rowspan_dfs(i, j, row, check_row = False):
    """
    搜索該格合併了多少列
    :param i: 被搜尋格的位置
    :param j: 被搜尋格的位置
    :param row: 記錄合併列的數量
    :param check_row: 第一次進來時會是 True，避免誤判
    :return: 返回 row，即合併列之數量
    """
    if (i >= len(table_struct) or j >= len(table_struct[0]) or table_struct[i][j] == 0 or table_struct[i][j] == 1):
        return row
    elif (table_struct[i][j] == 2):
        row += 1
        return rowspan_dfs(i + 1, j, row)  # down
    else:
        if check_row:
            return rowspan_dfs(i + 1, j, row)  # down
        else:
            return row


def save_as_jsonl(revise_file, output_file):
    with open (output_file, 'w', encoding='utf-8') as f:
        json.dump(revise_file, f)


def find_x_y(input_file, w, h):

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split('\t')

        data = json.loads(parts[1])

        for item in data:
            xmin, xmax, ymin, ymax = sort(item)

            should_add_xmin = all(abs(x - xmin) > w for x in x_list)
            if should_add_xmin:
                x_list.append(xmin)
            else:
                for x_idx in range(len(x_list)):
                    if abs(x_list[x_idx] - xmin) < w and xmin > x_list[x_idx]:
                        x_list[x_idx] = xmin
            x_list.sort()

            should_add_ymin = all(abs(y - ymin) > h for y in y_list)
            print(should_add_ymin)
            if should_add_ymin:
                y_list.append(ymin)
                print(ymin)
            else:
                for y_idx in range(len(y_list)):
                    print(y_idx)
                    if abs(y_list[y_idx] - ymin) < h and ymin > y_list[y_idx]:
                        y_list[y_idx] = ymin
            y_list.sort()
            print(y_list)


def sort(item):
    xmin = item['points'][0][0]
    ymin = item['points'][0][1]
    abs_xmin, abs_xmax, abs_ymin, abs_ymax = xmin, 0, ymin, 0
    ymax,xmax = 0, 0
    for i in range(0, 4):
        if xmin > int(item['points'][i][0]):
            xmin = int(item['points'][i][0])
        if xmax < int(item['points'][i][0]):
            xmax = int(item['points'][i][0])
    for j in range(0, 4):
        if ymin > int(item['points'][j][1]):
            ymin = int(item['points'][j][1])
        if ymax < int(item['points'][j][1]):
            ymax = int(item['points'][j][1])


    return xmin, xmax, ymin, ymax


def pic_w_h():
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split('\t')

        orig_filename = parts[0]
        orig_filename = (orig_filename.split('/'))[-1]
        pic_path = orig_filename

        img = Image.open(pic_path)
        imgSize = img.size
        w = img.width
        h = img.height

        return w, h




if __name__ == "__main__":
    input_file = "label.txt"
    output_file = "output.jsonl"
    x_list = []
    y_list = []

    table_w, table_h = pic_w_h()

    table_w /= 100
    table_h /= 100

    find_x_y(input_file, table_w, table_h)

    print(x_list)
    print(y_list)

    table = [None] * len(y_list)
    for i in range(len(y_list)):
        table[i] = ['{"tokens": []}'] * len(x_list)

    table_struct = [None] * len(y_list)
    for i in range(len(y_list)):
        table_struct[i] = [0] * len(x_list)



    print(table_w)
    print(table_h)

    rewritten_data = rewrite_text(input_file)
    print(table_struct)
    rewritten_data = table_html(rewritten_data)
    save_as_jsonl(rewritten_data, output_file)