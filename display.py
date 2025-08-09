import cv2

def overlay_results(frame, ocr_results, translations=None):
    out = frame.copy()
    for idx, (text, (x, y, w, h), conf) in enumerate(ocr_results):
        # draw bbox
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 255, 0), 2)
        label = f"{text} ({conf}%)"
        cv2.putText(out, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
        if translations and idx < len(translations):
            t = translations[idx]
            cv2.putText(out, t, (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,0), 2)
    return out