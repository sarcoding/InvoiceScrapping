import cv2
import pytesseract
import re
import numpy as np
from image_segmentation import parse_line_blocks

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

path = "D:\Project\InvoiceScrapping\sample4.jpg"
keywords = {
    "to": ["Billing Address", "Bill to", "Billed to", "To"],
    "amt": ["Amount", "Amount Due", "Total Payable", "Total Due Amount"],
    "gstno": ["GSTIN", "GST Number", "GST No"]
}
valid_currencies = ['$', '€', '₹']

def extract_amount(img, lines):
    amt_keys_pattern = "|".join(re.escape(key) for key in keywords["amt"])
    pattern_amt = rf".*({amt_keys_pattern})\s+([$€])?\s*((\d{{1,3}}(?:,\d{{3}})*)(\.\d{{2}})?)"
    
    for i in range(len(lines)-1, 0, -1):
        match_amt = re.match(pattern_amt, lines[i][5], re.IGNORECASE)
        if match_amt:
            # amount_text = lines[i][1]
            currency = match_amt.group(2) if match_amt.group(2) in valid_currencies else '₹'
            amount = float(match_amt.group(3).replace(',', ''))
            x1, y1, x2, y2 = lines[i][1:5]
            cv2.putText(img, "Amount", (x1, y2-25), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            return currency, amount
    
    return '₹', 0

def extract_gst_num(img, lines):
    gst_num_keys_pattern = "|".join(re.escape(key) for key in keywords["gstno"])
    pattern_gst_num = rf".*?({gst_num_keys_pattern})\s*([;:])?\s*(\w+)"
    gst_numbers = []

    for line in lines:
        match_gst_num = re.match(pattern_gst_num, line[5], re.IGNORECASE)
        if match_gst_num:
            gst_numbers.append(match_gst_num.group(3))
            x1, y1, x2, y2 = line[1: 5]
            cv2.putText(img, "GSTIN", (x1, y2-25), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return gst_numbers[:2]

def extract_to(img, blocks):
    to_keys_pattern = "|".join(re.escape(key) for key in keywords["to"])
    pattern_to = rf"\b({to_keys_pattern})\b"
    for i in range(len(blocks)):
        match_to = re.match(pattern_to, blocks[i][5], re.IGNORECASE)
        if match_to:
            left, top, right, bottom = blocks[i+1][1:5]
            cv2.putText(img, "To", (left, top-5), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            # print("____"*20)
            # print(i, len(blocks))
            return blocks[i+1][5]
    
    return "Not Found"

def extract_info(img=None):
    img = np.array(img)
    lines, blocks = parse_line_blocks(img=img)
    
    
    to_text = extract_to(img, blocks)
    amount_currency, amount_value = extract_amount(img, lines)
    gst_numbers = extract_gst_num(img, lines)
    return img, {'to': to_text, 'amt_currency': amount_currency, 'amt_value': amount_value, 'gst_numbers': gst_numbers}

if __name__ == "__main__":
    _, info = extract_info(img = cv2.imread("D:\Project\InvoiceScrapping\Final\Example1.jpg"))
    print(info)
    # print(f"TO: {info['to']}, Amount Currency: {info['amt_currency']}, Amount Value: {info['amt_value']}, GSTINs: {info['gst_numbers']}")
