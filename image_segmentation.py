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


if __name__ == "__main__":
    img_path = 'sample2.png'
    # blocks = parse_blocks(cv2.imread(img_path))
    lines, blocks = parse_line_blocks(cv2.imread("D:\Project\InvoiceScrapping\Final\Example1.jpg"))
    # lines = parse_blocks(boxes)
    # for line_info in lines:
    #     line_coordinates, line_text = line_info
    #     x1, y1, x2, y2 = line_coordinates
    #     print(f"Line Text: {line_text}")
    #     print(f"Coordinates: ({x1}, {y1}), ({x2}, {y2})")
