import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_line_blocks(img):
    if img is None:
        print("Error: Image not found")
        return []

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    blocks = parse_blocks(img, boxes)
    lines = parse_lines(img, boxes)
    return lines, blocks

    
def parse_blocks(img, boxes):
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

def parse_lines(img, boxes):
    lines = []
    current_line = ''
    line_start_coordinates = None
    line_num_prev = None

    for i in range(len(boxes['text'])):
        text = boxes['text'][i].strip()
        line_num = boxes['line_num'][i]
        x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
        line_coordinates = (x, y, x + w, y + h)

        if line_num != line_num_prev and line_num_prev is not None:
            lines.append((line_start_coordinates, current_line.strip()))
            current_line = ''
            line_start_coordinates = None

        if text:
            if line_start_coordinates is None:
                line_start_coordinates = line_coordinates
            current_line += text + ' '

        line_num_prev = line_num

    if current_line.strip():
        lines.append((line_start_coordinates, current_line.strip()))

    filtered_lines = [(coords, text) for coords, text in lines if coords is not None and text.strip()]
    
    return filtered_lines


if __name__ == "__main__":
    img_path = 'sample2.png'
    blocks = parse_blocks(cv2.imread(img_path))
    lines = parse_lines(cv2.imread(img_path))
    for line_info in lines:
        line_coordinates, line_text = line_info
        x1, y1, x2, y2 = line_coordinates
        print(f"Line Text: {line_text}")
        print(f"Coordinates: ({x1}, {y1}), ({x2}, {y2})")
