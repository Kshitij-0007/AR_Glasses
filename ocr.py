import pytesseract
import cv2
import numpy as np
from functools import lru_cache

class OCRProcessor:
    def __init__(self):
        # Optimized config for Pi
        self.config = "--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 "
        self.min_confidence = 40
        
    @lru_cache(maxsize=32)
    def _get_kernel(self, size):
        return cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
        
    def _preprocess(self, frame):
        # Resize for consistent processing
        h, w = frame.shape[:2]
        if w > 640:
            scale = 640 / w
            frame = cv2.resize(frame, (640, int(h * scale)))
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Enhanced preprocessing for better accuracy
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        
        # Gaussian blur to reduce noise
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        
        # Adaptive threshold
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Morphological operations to clean up
        kernel = self._get_kernel(2)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        
        return binary
        
    def process(self, frame):
        processed = self._preprocess(frame)
        
        try:
            data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT, 
                                           config=self.config)
            
            results = []
            n_boxes = len(data['level'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                if not text:
                    continue
                    
                conf = int(data['conf'][i]) if str(data['conf'][i]).isdigit() else 0
                if conf < self.min_confidence:
                    continue
                    
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                
                # Filter out very small detections
                if w < 20 or h < 10:
                    continue
                    
                results.append({
                    'text': text,
                    'bbox': (x, y, w, h),
                    'confidence': conf
                })
                
            return results
            
        except Exception as e:
            print(f"OCR Error: {e}")
            return []
