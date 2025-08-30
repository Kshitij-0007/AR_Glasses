import pytesseract
import cv2
import numpy as np
from functools import lru_cache

class OCRProcessor:
    def __init__(self):
        # High precision config for better accuracy
        self.config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;: '
        self.min_confidence = 60  # Higher threshold
        
    def _enhance_image(self, image):
        """Advanced preprocessing for maximum OCR accuracy"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
            
        # Resize for better OCR (tesseract works best at 300 DPI equivalent)
        height, width = gray.shape
        if height < 100:
            scale = 3.0
            gray = cv2.resize(gray, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_CUBIC)
        
        # Noise reduction
        denoised = cv2.fastNlMeansDenoising(gray)
        
        # Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        
        # Sharpening kernel
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        
        # Adaptive thresholding for clean binary image
        binary = cv2.adaptiveThreshold(sharpened, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Morphological operations to clean up
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cleaned
        
    def process(self, frame):
        """Process frame with high-precision OCR"""
        try:
            # Enhanced preprocessing
            processed = self._enhance_image(frame)
            
            # Multiple OCR attempts with different PSM modes for better accuracy
            configs = [
                r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;: ',
                r'--oem 3 --psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;: ',
                r'--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?;: '
            ]
            
            best_results = []
            
            for config in configs:
                try:
                    data = pytesseract.image_to_data(processed, output_type=pytesseract.Output.DICT, 
                                                   config=config)
                    
                    results = []
                    n_boxes = len(data['level'])
                    
                    for i in range(n_boxes):
                        text = data['text'][i].strip()
                        if not text or len(text) < 2:  # Skip single characters
                            continue
                            
                        conf = int(data['conf'][i]) if str(data['conf'][i]).isdigit() else 0
                        if conf < self.min_confidence:
                            continue
                            
                        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                        
                        # Filter out very small or very large detections
                        if w < 30 or h < 15 or w > 500 or h > 100:
                            continue
                            
                        # Additional text validation
                        if self._is_valid_text(text):
                            results.append({
                                'text': text,
                                'bbox': (x, y, w, h),
                                'confidence': conf
                            })
                    
                    if results:
                        best_results = results
                        break
                        
                except Exception:
                    continue
                    
            return best_results
            
        except Exception as e:
            print(f"OCR Error: {e}")
            return []
            
    def _is_valid_text(self, text):
        """Validate if detected text is meaningful"""
        # Remove common OCR artifacts
        if len(text) < 2:
            return False
            
        # Check if text contains mostly valid characters
        valid_chars = sum(1 for c in text if c.isalnum() or c in '.,!?;: ')
        if valid_chars / len(text) < 0.7:
            return False
            
        # Reject strings with too many repeated characters
        if len(set(text)) < len(text) * 0.3:
            return False
            
        return True
