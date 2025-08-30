"""
Configuration settings for AR Glasses
Optimized for Raspberry Pi performance
"""

# Camera settings
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 15

# OCR settings
OCR_MIN_CONFIDENCE = 50  # EasyOCR percentage scale
OCR_FRAME_SKIP = 2  # Process every 2nd frame
OCR_MIN_TEXT_SIZE = (20, 10)  # Minimum width, height for text detection

# Threading settings
MAX_QUEUE_SIZE = 2
WORKER_TIMEOUT = 0.1

# Translation settings
TRANSLATION_CACHE_SIZE = 512
TRANSLATION_CACHE_TIMEOUT = 300  # 5 minutes

# Display settings
FONT_SCALE = 0.5
FONT_THICKNESS = 1
BBOX_COLOR = (0, 255, 0)  # Green
ORIGINAL_TEXT_COLOR = (0, 255, 0)  # Green
TRANSLATED_TEXT_COLOR = (0, 255, 255)  # Yellow

# Performance settings for Pi
import os
os.environ['OMP_THREAD_LIMIT'] = '2'
os.environ['OPENCV_VIDEOIO_PRIORITY_V4L2'] = '1'
