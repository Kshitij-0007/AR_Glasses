import cv2
import threading
import time

class CaptureThread(threading.Thread):
    def __init__(self, src=0, width=640, height=480):
        super().__init__(daemon=True)
        self.cap = cv2.VideoCapture(src)
        
        # Optimized settings for Pi
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FPS, 15)  # Lower FPS for Pi
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer
        
        self.lock = threading.Lock()
        self.frame = None
        self.running = True
        self.last_frame_time = 0
        
    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue
                
            # Limit frame rate to reduce CPU load
            current_time = time.time()
            if current_time - self.last_frame_time < 1/15:  # 15 FPS max
                continue
                
            self.last_frame_time = current_time
            
            with self.lock:
                self.frame = frame
                
    def read(self):
        with self.lock:
            return self.frame.copy() if self.frame is not None else None
            
    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
