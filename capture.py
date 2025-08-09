import cv2
import threading

class CaptureThread(threading.Thread):
    def __init__(self, src=0, width=1280, height=720):
        super().__init__(daemon=True)
        self.cap = cv2.VideoCapture(src)
        # try to set resolution; may fail on some cameras
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.lock = threading.Lock()
        self.frame = None
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            with self.lock:
                self.frame = frame.copy()

    def read(self):
        with self.lock:
            return None if self.frame is None else self.frame.copy()

    def stop(self):
        self.running = False
        self.cap.release()
