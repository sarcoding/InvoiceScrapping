import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def draw_boxes(img_path, blocks):
    img = cv2.imread(img_path)
    if img is None:
        print("Error: Image not found")
        return

    for block in blocks:
        left, top, right, bottom = block[2:6]
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)  # Green rectangle

    cv2.imshow('Bounding Boxes', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def parse_blocks(img):
    if img is None:
        print("Error: Image not found")
        return []

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img_rgb, output_type=pytesseract.Output.DICT)

    blocks = []
    for i in range(len(boxes['text'])):
        if int(boxes['conf'][i]) > 50:
            block_num = boxes['block_num'][i]
            left = boxes['left'][i]
            top = boxes['top'][i]
            width = boxes['width'][i]
            height = boxes['height'][i]
            text = boxes['text'][i]

            if text == " " or text == '':
                continue

            block_exists = False
            for block in blocks:
                if block[0] == block_num:
                    block_exists = True
                    block[2] = min(block[2], left)
                    block[3] = min(block[3], top)
                    block[4] = max(block[4], left + width)
                    block[5] = max(block[5], top + height)
                    block[6] = block[6] + " " + text if len(block) > 6 else text
                    break

            if not block_exists:
                blocks.append([block_num, text, left, top, left + width, top + height, text])
    return blocks

def parse_lines(img):
    lines = []
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img_rgb, output_type=pytesseract.Output.DICT)

    current_line = ''
    line_start_coordinates = None

    for i in range(len(boxes['text'])):
        text = boxes['text'][i].strip()
        line_num = boxes['line_num'][i]

        if text:
            if line_start_coordinates is None:
                x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
                line_start_coordinates = (x, y, x + w, y + h)
            current_line += text + ' '
        elif current_line.strip():
            lines.append((line_start_coordinates, current_line.strip()))
            current_line = ''
            line_start_coordinates = None
    if current_line.strip():
        lines.append((line_start_coordinates, current_line.strip()))

    return lines

if __name__ == "__main__":
    img_path = 'sample2.png'
    blocks = parse_blocks(cv2.imread(img_path))
    lines = parse_lines(cv2.imread(img_path))
    for line_info in lines:
        line_coordinates, line_text = line_info
        x1, y1, x2, y2 = line_coordinates
        print(f"Line Text: {line_text}")
        print(f"Coordinates: ({x1}, {y1}), ({x2}, {y2})")
