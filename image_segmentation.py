import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_line_blocks(img):
    if img is None:
        print("Error: Image not found")
        return []

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    blocks = []
    lines = []
    for i in range(len(boxes['text'])):
        if int(boxes['conf'][i]) > 50:
            block_num = boxes['block_num'][i]
            line_num = boxes['line_num'][i]
            left = boxes['left'][i]
            top = boxes['top'][i]
            width = boxes['width'][i]
            height = boxes['height'][i]
            text = boxes['text'][i]

            if text == " " or text == '':
                continue
            if len(lines) == 0:
                lines.append([line_num, left, top, left + width, top + height, text])
                blocks.append([block_num, left, top, left + width, top + height, text])
                continue
            if blocks[-1][0] == block_num:
                if lines[-1][0] == line_num:
                    lines[-1][1] = min(lines[-1][1], left)
                    lines[-1][2] = min(lines[-1][2], top)
                    lines[-1][3] = max(lines[-1][3], left + width)
                    lines[-1][4] = max(lines[-1][4], top + height)
                    lines[-1][5] += " " + text
                else:
                    lines.append([line_num, left, top, left + width, top + height, text])
                blocks[-1][1] = min(blocks[-1][1], left)
                blocks[-1][2] = min(blocks[-1][2], top)
                blocks[-1][3] = max(blocks[-1][3], left + width)
                blocks[-1][4] = max(blocks[-1][4], top + height)
                blocks[-1][5] += " " + text

            else:
                lines.append([line_num, left, top, left + width, top + height, text])
                blocks.append([block_num, left, top, left + width, top + height, text])
    return lines, blocks

def check(lines):
    for i, line in enumerate(lines):
        if len(line) != 6:
            print(i)
    print(lines)
    print("No error")
def parse_blocks(boxes):
    blocks = []
    lines = []
    for i in range(len(boxes['text'])):
        if int(boxes['conf'][i]) > 50:
            block_num = boxes['block_num'][i]
            line_num = boxes['line_num'][i]
            left = boxes['left'][i]
            top = boxes['top'][i]
            width = boxes['width'][i]
            height = boxes['height'][i]
            text = boxes['text'][i]

            if text == " " or text == '':
                continue
            if len(lines) == 0:
                lines.append([line_num, left, top, left + width, top + height, text])
                blocks.append([block_num, left, top, left + width, top + height, text])
                continue
            if blocks[-1][0] == block_num:
                if lines[-1][0] == line_num:
                    lines[-1][1] = min(lines[-1][1], left)
                    lines[-1][2] = min(lines[-1][2], top)
                    lines[-1][3] = max(lines[-1][3], left + width)
                    lines[-1][4] = max(lines[-1][4], top + height)
                    lines[-1][5] += " " + text
                else:
                    lines.append([line_num, left, top, left + width, top + height, text])
                blocks[-1][1] = min(blocks[-1][1], left)
                blocks[-1][2] = min(blocks[-1][2], top)
                blocks[-1][3] = max(blocks[-1][3], left + width)
                blocks[-1][4] = max(blocks[-1][4], top + height)
                blocks[-1][5] += " " + text

            else:
                lines.append([line_num, left, top, left + width, top + height, text])
                blocks.append([block_num, left, top, left + width, top + height, text])

def parse_lines(boxes):
    lines = []
    # current_line = ''
    # line_start_coordinates = None
    # line_num_prev = None

    for i in range(len(boxes['text'])):
        if int(boxes['conf'][i]) > 50:
            line_num = boxes['line_num'][i]
            line_left = boxes['left'][i]
            line_top = boxes['top'][i]
            line_width = boxes['width'][i]
            line_height = boxes['height'][i]
            line_text = boxes['text'][i]

            if line_text == "" or line_text ==" ":
                continue

            line_exist = False
            for line in lines:
                if line[0] == line_num:
                    line_exist = True
                    line[1] = min(line[1], line_left)
                    line[2] = min(line[2], line_top)
                    line[3] = max(line[3], line_left + line_width)
                    line[4] = max(line[4], line_top + line_height)
                    line[5] += " " + line_text
                    break
            if not line_exist:
                lines.append([line_num, line_left, line_top, line_left + line_width, line_top + line_height, line_text])
    img = cv2.imread("D:\Project\InvoiceScrapping\Final\Example1.jpg")
    for line in lines:
        x1, y1, x2, y2 = line[1:5]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    print(lines)
    cv2.imwrite("sample.jpg", img)
        
    return lines


if __name__ == "__main__":
    img_path = 'sample2.png'
    # blocks = parse_blocks(cv2.imread(img_path))
    lines, blocks = parse_line_blocks(cv2.imread("D:\Project\InvoiceScrapping\Final\Example1.jpg"))
    check(blocks)
    # lines = parse_blocks(boxes)
    # for line_info in lines:
    #     line_coordinates, line_text = line_info
    #     x1, y1, x2, y2 = line_coordinates
    #     print(f"Line Text: {line_text}")
    #     print(f"Coordinates: ({x1}, {y1}), ({x2}, {y2})")
