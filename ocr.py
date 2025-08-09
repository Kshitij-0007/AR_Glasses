import pytesseract
import cv2
import numpy as np

# Preprocessing helper for cpu-friendly OCR
def preprocess_for_ocr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Bilateral to preserve edges
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    # Adaptive threshold
    th = cv2.adaptiveThreshold(filtered, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY, 11, 2)
    return th

# OCR function: returns list of (text, bbox)
def ocr_detect(frame, lang='eng'):
    img = preprocess_for_ocr(frame)
    # pytesseract data output
    config = "--oem 1 --psm 6"
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, lang=lang, config=config)
    texts = []
    n_boxes = len(data['level'])
    for i in range(n_boxes):
        text = data['text'][i].strip()
        conf = int(data['conf'][i]) if data['conf'][i].isdigit() else -1
        if text and conf > 30:
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            texts.append((text, (x, y, w, h), conf))
    return texts