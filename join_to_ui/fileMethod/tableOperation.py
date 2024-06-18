from fileMethod import fileInfo

def getTableStruct(content, x_list, y_list, w_residual, h_residual, w, h):
    """
    通過 x軸上的點及 y軸上的點分析表格結構，重現出來
    :param content: 原 json文件中內容
    :param x_list: x軸上的所有節點
    :param y_list: y軸上的所有節點
    :param w_residual: 寬的誤差值
    :param h_residual: 高的誤差值
    :param w:
    :param h:
    :return: 紀錄是否為合併儲存格的 dict
    """

    idx_x, idx_y = 0, 0

    # 用於存放 item id與之對應的是否有合併儲存格的資訊
    table_dict = {}

    # 創建 table_struct的 list，預設全為0，表示沒有合併儲存格
    table_struct = [None] * len(y_list)
    for i in range(len(y_list)):
        table_struct[i] = [0] * len(x_list)

    for item in content["label_info"]:
        if content["label_info"][item]['description'] == 'table':
            pass
        else:
            x_index, y_index, x_index_tab, y_index_tab= 0, 0, 0, 0
            x_control, y_control, the_first, check = True, True, True, True


            # 取得該 item xy的 min & max值
            xmin, ymin, xmax, ymax = fileInfo.getRectCoordinateToInt(content["label_info"][item]["points"], w, h)


            # 尋找該 item x & y的 min值在 x_list和 y_list中的索引值
            while (check):
                if abs(x_list[x_index] - xmin) < w_residual:
                    if abs(y_list[y_index] - ymin) < h_residual:
                        check = False
                    else:
                        y_index += 1
                        y_index = y_index % len(y_list)
                else:
                    x_index += 1
                    x_index = x_index % len(x_list)


            # 尋找該 item x的 max值在 x_list中的索引值
            while x_control:
                x_index_tab += 1
                if not x_index_tab % len(x_list) == 0:
                    if xmax > x_list[x_index_tab] + w_residual:
                        continue
                    else:
                        x_control = False
                else:
                    x_control = False


            # 尋找該 item y的 max值在 y_list中的索引值
            while y_control:
                y_index_tab += 1
                if not y_index_tab % len(y_list) == 0:
                    if ymax > y_list[y_index_tab] + h_residual:
                        continue
                    else:
                        y_control = False
                else:
                    y_control = False


            # 通過 xy min, max的索引值判斷是否為合併儲存格，並記錄在 table_dict中
            # 0 為正常格，即非合併儲存格
            # 3 為合併儲存格
            # 1 表示 3 往右合併的儲存格
            # 2 表示 3 往下合併的儲存格
            for i in range(x_index, x_index_tab):
                for j in range(y_index, y_index_tab):
                    if the_first:
                        table_struct[j][i] = 0
                        table_dict[item] = 0
                        idx_x = i
                        idx_y = j
                        the_first = False
                    else:
                        table_struct[idx_y][idx_x] = 3
                        table_dict[item] = 3
                        if(i > idx_x):
                            table_struct[j][i] = 1
                        elif(j > idx_y):
                            table_struct[j][i] = 2

    return table_struct, table_dict


def getAllXY(content, group, w, h, w_residual, h_residual):
    """
    尋找該表在 x與 y方向的節點，並存在列表中
    :param content: 原 json文件內容
    :param w: 圖片的寬
    :param h: 圖片的高
    :param w_residual: 寬的誤差值
    :param h_residual: 高的誤差值
    :return: x與 y節點的列表
    """

    x_list, y_list = [], []
    x_max, y_max = 0, 0

    # 遍歷所有 item
    for item in group:
        if content["label_info"][item]["shape"] == "Rect":

            # 尋找 item xy的 min和 max值
            xmin, ymin, xmax, ymax = fileInfo.getRectCoordinateToInt(content["label_info"][item]["points"], w, h)

            # 通過 x的 min值建構x軸的節點
            should_add_xmin = all(abs(x - xmin) > w_residual for x in x_list)
            if should_add_xmin:
                x_list.append(xmin)
            else:
                for x_idx in range(len(x_list)):
                    if abs(x_list[x_idx] - xmin) < w_residual and xmin > x_list[x_idx]:
                        x_list[x_idx] = xmin
            x_list.sort()

            # 通過 y的 min值建構x軸的節點
            should_add_ymin = all(abs(y - ymin) > h_residual for y in y_list)
            if should_add_ymin:
                y_list.append(ymin)
            else:
                for y_idx in range(len(y_list)):
                    if abs(y_list[y_idx] - ymin) < h_residual and ymin > y_list[y_idx]:
                        y_list[y_idx] = ymin
            y_list.sort()

            if x_max < xmax:
                x_max = xmax

            if y_max < ymax:
                y_max = ymax

    return x_list, y_list, x_max, y_max