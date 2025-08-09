import time
from capture import CaptureThread
from ocr import ocr_detect
from translate import translate_text
from display import overlay_results
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2

def main(target_lang='hi'):
    cap_thread = CaptureThread(src=0, width=1280, height=720)
    cap_thread.start()

    ocr_pool = ThreadPoolExecutor(max_workers=2)
    translate_pool = ThreadPoolExecutor(max_workers=2)

    last_run = 0
    ocr_interval = 0.5  # seconds between OCR runs

    try:
        while True:
            frame = cap_thread.read()
            if frame is None:
                time.sleep(0.01)
                continue

            now = time.time()
            ocr_results = []
            translations = []
            # Run OCR at a fixed interval to save CPU
            if now - last_run >= ocr_interval:
                last_run = now
                # submit OCR job
                future = ocr_pool.submit(ocr_detect, frame)
                ocr_results = future.result()

                # submit translation jobs for each detected text
                trans_futures = [translate_pool.submit(translate_text, t[0], target_lang) for t in ocr_results]
                for f in trans_futures:
                    translations.append(f.result())

            # overlay on the latest frame
            out = overlay_results(frame, ocr_results, translations)
            cv2.imshow('AR_Glasses - press q to quit', out)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cap_thread.stop()
        ocr_pool.shutdown(wait=False)
        translate_pool.shutdown(wait=False)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    # change 'hi' to any language code like 'en', 'es', 'fr', etc.
    main(target_lang='hi')
