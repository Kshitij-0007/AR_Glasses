#!/usr/bin/env python3
"""
Test EasyOCR precision with sample text images
"""
import cv2
import numpy as np
from ocr import OCRProcessor

def create_test_image(text, font_size=40):
    """Create a test image with text"""
    img = np.ones((100, 600, 3), dtype=np.uint8) * 255
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = font_size / 30
    color = (0, 0, 0)
    thickness = 2
    
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    x = (img.shape[1] - text_size[0]) // 2
    y = (img.shape[0] + text_size[1]) // 2
    
    cv2.putText(img, text, (x, y), font, font_scale, color, thickness)
    return img

def test_easyocr_precision():
    """Test EasyOCR with various text samples"""
    print("Initializing EasyOCR...")
    ocr = OCRProcessor()
    
    test_texts = [
        "Hello World",
        "Python Programming", 
        "Machine Learning",
        "Computer Vision",
        "Real Time Processing",
        "Text Recognition",
        "123 Main Street",
        "OpenCV EasyOCR"
    ]
    
    print("Testing EasyOCR Precision...")
    print("=" * 60)
    
    correct_detections = 0
    
    for i, original_text in enumerate(test_texts):
        test_img = create_test_image(original_text)
        results = ocr.process(test_img)
        
        detected_text = ""
        confidence = 0
        
        if results:
            best_result = max(results, key=lambda x: x['confidence'])
            detected_text = best_result['text']
            confidence = best_result['confidence']
            
            if original_text.lower().replace(" ", "") in detected_text.lower().replace(" ", ""):
                correct_detections += 1
                status = "✓ CORRECT"
            else:
                status = "✗ INCORRECT"
        else:
            status = "✗ NO DETECTION"
        
        print(f"Test {i+1}: {original_text:20} -> {detected_text:20} ({confidence:2d}%) {status}")
    
    accuracy = (correct_detections / len(test_texts)) * 100
    print("=" * 60)
    print(f"EasyOCR Accuracy: {correct_detections}/{len(test_texts)} = {accuracy:.1f}%")
    
    if accuracy >= 95:
        print("🎉 EXCELLENT - EasyOCR is working perfectly!")
    elif accuracy >= 80:
        print("👍 VERY GOOD - EasyOCR is highly accurate")
    else:
        print("⚠️  Check EasyOCR installation")

if __name__ == "__main__":
    test_easyocr_precision()
