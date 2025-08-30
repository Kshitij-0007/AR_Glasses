#!/usr/bin/env python3
"""
Test OCR precision with sample text images
"""
import cv2
import numpy as np
from ocr import OCRProcessor
import os

def create_test_image(text, font_size=40):
    """Create a test image with text"""
    # Create white background
    img = np.ones((100, 600, 3), dtype=np.uint8) * 255
    
    # Add text
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = font_size / 30
    color = (0, 0, 0)  # Black text
    thickness = 2
    
    # Get text size and center it
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    x = (img.shape[1] - text_size[0]) // 2
    y = (img.shape[0] + text_size[1]) // 2
    
    cv2.putText(img, text, (x, y), font, font_scale, color, thickness)
    return img

def test_ocr_precision():
    """Test OCR with various text samples"""
    ocr = OCRProcessor()
    
    test_texts = [
        "Hello World",
        "Python Programming",
        "Machine Learning",
        "Computer Vision",
        "Artificial Intelligence",
        "OpenCV Tesseract",
        "Real Time Processing",
        "Text Recognition",
        "123 Main Street",
        "Email: test@example.com"
    ]
    
    print("Testing OCR Precision...")
    print("=" * 50)
    
    total_tests = len(test_texts)
    correct_detections = 0
    
    for i, original_text in enumerate(test_texts):
        # Create test image
        test_img = create_test_image(original_text)
        
        # Process with OCR
        results = ocr.process(test_img)
        
        # Check results
        detected_text = ""
        confidence = 0
        
        if results:
            # Get the best result
            best_result = max(results, key=lambda x: x['confidence'])
            detected_text = best_result['text']
            confidence = best_result['confidence']
            
            # Check if detection is correct (allowing for minor differences)
            if original_text.lower().replace(" ", "") in detected_text.lower().replace(" ", ""):
                correct_detections += 1
                status = "✓ CORRECT"
            else:
                status = "✗ INCORRECT"
        else:
            status = "✗ NO DETECTION"
        
        print(f"Test {i+1:2d}: {original_text:25} -> {detected_text:25} ({confidence:2d}%) {status}")
        
        # Save test image for debugging
        cv2.imwrite(f"test_img_{i+1}.png", test_img)
    
    accuracy = (correct_detections / total_tests) * 100
    print("=" * 50)
    print(f"Accuracy: {correct_detections}/{total_tests} = {accuracy:.1f}%")
    
    if accuracy >= 90:
        print("🎉 EXCELLENT - OCR is working with high precision!")
    elif accuracy >= 70:
        print("👍 GOOD - OCR is working well")
    elif accuracy >= 50:
        print("⚠️  FAIR - OCR needs improvement")
    else:
        print("❌ POOR - OCR configuration needs major fixes")
    
    return accuracy

def test_live_camera():
    """Test OCR with live camera feed"""
    print("\nTesting with live camera...")
    print("Hold up text in front of camera. Press 'q' to quit.")
    
    cap = cv2.VideoCapture(0)
    ocr = OCRProcessor()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Process frame
        results = ocr.process(frame)
        
        # Draw results
        for result in results:
            text = result['text']
            bbox = result['bbox']
            conf = result['confidence']
            
            x, y, w, h = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{text} ({conf}%)", (x, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('OCR Precision Test - Press q to quit', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("OCR Precision Testing Tool")
    print("This will test the accuracy of text recognition")
    print()
    
    # Test with generated images
    accuracy = test_ocr_precision()
    
    # Ask user if they want to test with camera
    if accuracy >= 70:
        response = input("\nTest with live camera? (y/n): ").lower()
        if response == 'y':
            test_live_camera()
    else:
        print("\nSkipping camera test due to low accuracy.")
        print("Please check Tesseract installation and try again.")
