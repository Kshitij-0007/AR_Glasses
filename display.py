import cv2
import numpy as np

class DisplayProcessor:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 0.5
        self.thickness = 1
        
    def _get_text_size(self, text, font_scale=None):
        if font_scale is None:
            font_scale = self.font_scale
        return cv2.getTextSize(text, self.font, font_scale, self.thickness)[0]
        
    def _draw_text_with_background(self, img, text, pos, color, bg_color):
        x, y = pos
        text_size = self._get_text_size(text)
        
        # Draw background rectangle
        cv2.rectangle(img, (x-2, y-text_size[1]-4), 
                     (x+text_size[0]+2, y+4), bg_color, -1)
        
        # Draw text
        cv2.putText(img, text, (x, y), self.font, self.font_scale, color, self.thickness)
        
    def overlay(self, frame, results):
        if not results:
            return frame
            
        output = frame.copy()
        
        for result in results:
            bbox = result['bbox']
            x, y, w, h = bbox
            confidence = result['confidence']
            original = result['original']
            translated = result['translated']
            
            # Draw bounding box
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Draw original text with confidence
            orig_text = f"{original} ({confidence}%)"
            self._draw_text_with_background(output, orig_text, (x, y-10), 
                                          (0, 255, 0), (0, 0, 0))
            
            # Draw translated text
            if translated != original:
                self._draw_text_with_background(output, translated, (x, y+h+20), 
                                              (0, 255, 255), (0, 0, 0))
                
        return output
