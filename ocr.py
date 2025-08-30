import easyocr
import cv2
import numpy as np

class OCRProcessor:
    def __init__(self):
        # Initialize EasyOCR reader (English by default)
        self.reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if available
        self.min_confidence = 0.5  # EasyOCR uses 0-1 scale
        
    def _preprocess(self, frame):
        """Light preprocessing for EasyOCR"""
        # EasyOCR works well with minimal preprocessing
        if len(frame.shape) == 3:
            # Convert to RGB (EasyOCR expects RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame
        
    def process(self, frame):
        """Process frame with EasyOCR"""
        try:
            # Preprocess frame
            processed = self._preprocess(frame)
            
            # Run EasyOCR
            results = self.reader.readtext(processed)
            
            # Convert to our format
            ocr_results = []
            for (bbox, text, confidence) in results:
                if confidence < self.min_confidence:
                    continue
                    
                if len(text.strip()) < 2:  # Skip single characters
                    continue
                
                # Convert bbox format
                x_coords = [point[0] for point in bbox]
                y_coords = [point[1] for point in bbox]
                x, y = int(min(x_coords)), int(min(y_coords))
                w, h = int(max(x_coords) - x), int(max(y_coords) - y)
                
                # Filter reasonable sizes
                if w < 20 or h < 10 or w > 500 or h > 100:
                    continue
                
                ocr_results.append({
                    'text': text.strip(),
                    'bbox': (x, y, w, h),
                    'confidence': int(confidence * 100)  # Convert to percentage
                })
                
            return ocr_results
            
        except Exception as e:
            print(f"EasyOCR Error: {e}")
            return []
