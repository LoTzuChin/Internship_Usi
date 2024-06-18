import json

def rewrite_text(input_file):
    imgid = 0
    index = 0
    xmin, xmax, ymin, ymax = 0, 0, 0, 0

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split('\t')

        orig_filename = parts[0]
        orig_filename = (orig_filename.split('/'))[-1]
        print(orig_filename)
        converted_data = {'filename': orig_filename, 'split': ' ', 'imgid': imgid, 'html': {'cell': []}}

        data = json.loads(parts[1])

        for item in data:
            xmin = item['points'][0][0]
            ymin = item['points'][0][1]
            # print(123)
            # print(x_list[len(x_list)-1])
            # print(y_list[len(y_list)-1])
            # print(ymax)
        # while(xmax < x_list[len(x_list)-1] and ymax < y_list[len(y_list)-1]):
            # print(123)

            for i in range(0, 4):
                # print(i)
                if xmin > int(item['points'][i][0]):
                    xmin = int(item['points'][i][0])
                    # print(xmin)
                if xmax < int(item['points'][i][0]):
                    xmax = int(item['points'][i][0])
            for j in range(0, 4):
                if ymin > int(item['points'][j][1]):
                    ymin = int(item['points'][j][1])
                if ymax < int(item['points'][j][1]):
                    ymax = int(item['points'][j][1])
            if abs(x_list[index] - xmin) <= 10:
                # print(index)
                bbox = [xmin, ymin, xmax, ymax]
                print(bbox)
                token = list(item['transcription'])
                cell = {'tokens': token, 'bbox': bbox}
            else:
                cell = {'tokens': []}
            converted_data['html']['cell'].append(cell)
            index += 1
            index = index % len(x_list)

        print(converted_data)

        return converted_data


def save_as_jsonl(revise_file, output_file):
    with open (output_file, 'w', encoding='utf-8') as f:
        json.dump(revise_file, f)

def read_file(input_file):

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split('\t')

        data = json.loads(parts[1])

        for item in data:
            should_add_xmin = all(abs(x - int(item['points'][0][0])) > 10 for x in x_list)
            if should_add_xmin:
                x_list.append(item['points'][0][0])

            should_add_ymin = all(abs(y - int(item['points'][0][1])) > 5 for y in y_list)
            if should_add_ymin:
                y_list.append(item['points'][0][1])

def find_x_y(input_file):

    xmin, xmax, ymin, ymax = 0, 0, 0, 0

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split('\t')

        data = json.loads(parts[1])

        for item in data:
            xmin = item['points'][0][0]
            ymin = item['points'][0][1]
            for i in range(0, 4):
                if xmin > int(item['points'][i][0]):
                    xmin = int(item['points'][i][0])
                    # print(xmin)
                if xmax < int(item['points'][i][0]):
                    xmax = int(item['points'][i][0])
            for j in range(0, 4):
                if ymin > int(item['points'][j][1]):
                    ymin = int(item['points'][j][1])
                if ymax < int(item['points'][j][1]):
                    ymax = int(item['points'][j][1])

            should_add_xmin = all(abs(x - xmin) > 10 for x in x_list)
            if should_add_xmin:
                x_list.append(xmin)

            should_add_ymin = all(abs(y - ymin) > 5 for y in y_list)
            if should_add_ymin:
                y_list.append(ymin)

    return xmin, xmax, ymin, ymax


if __name__ == "__main__":
    input_file = "新增資料夾/Label.txt"
    output_file = "output.jsonl"
    x_list = []
    y_list = []

    min_x, max_x, min_y, max_y = find_x_y(input_file)
    print(x_list)
    rewritten_data = rewrite_text(input_file)
    save_as_jsonl(rewritten_data, output_file)

