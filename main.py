import time
import threading
import queue
from capture import CaptureThread
from ocr import OCRProcessor
from translate import TranslationProcessor
from display import DisplayProcessor
import cv2
import config

class ARGlassesApp:
    def __init__(self, target_lang='hi', camera_src=0):
        self.capture = CaptureThread(src=camera_src, 
                                   width=config.CAMERA_WIDTH, 
                                   height=config.CAMERA_HEIGHT)
        self.ocr_processor = OCRProcessor()
        self.translation_processor = TranslationProcessor(target_lang)
        self.display_processor = DisplayProcessor()
        
        # Thread-safe queues
        self.frame_queue = queue.Queue(maxsize=config.MAX_QUEUE_SIZE)
        self.ocr_queue = queue.Queue(maxsize=config.MAX_QUEUE_SIZE)
        self.result_queue = queue.Queue(maxsize=config.MAX_QUEUE_SIZE)
        
        self.running = True
        self.current_results = []
        
    def start(self):
        self.capture.start()
        
        # Start processing threads
        threading.Thread(target=self._ocr_worker, daemon=True).start()
        threading.Thread(target=self._translation_worker, daemon=True).start()
        
        self._main_loop()
        
    def _ocr_worker(self):
        while self.running:
            try:
                frame = self.frame_queue.get(timeout=config.WORKER_TIMEOUT)
                results = self.ocr_processor.process(frame)
                if results:
                    try:
                        self.ocr_queue.put_nowait(results)
                    except queue.Full:
                        pass
            except queue.Empty:
                continue
                
    def _translation_worker(self):
        while self.running:
            try:
                ocr_results = self.ocr_queue.get(timeout=config.WORKER_TIMEOUT)
                translated = self.translation_processor.process(ocr_results)
                try:
                    self.result_queue.put_nowait(translated)
                except queue.Full:
                    pass
            except queue.Empty:
                continue
                
    def _main_loop(self):
        frame_skip = 0
        try:
            while self.running:
                frame = self.capture.read()
                if frame is None:
                    time.sleep(0.01)
                    continue
                
                # Process every Nth frame for OCR
                frame_skip += 1
                if frame_skip % config.OCR_FRAME_SKIP == 0:
                    try:
                        self.frame_queue.put_nowait(frame)
                    except queue.Full:
                        pass
                
                # Get latest results
                try:
                    self.current_results = self.result_queue.get_nowait()
                except queue.Empty:
                    pass
                
                # Display
                display_frame = self.display_processor.overlay(frame, self.current_results)
                cv2.imshow('AR Glasses - Press q to quit', display_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()
            
    def stop(self):
        self.running = False
        self.capture.stop()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    app = ARGlassesApp(target_lang='hi')
    app.start()
