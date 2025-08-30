# AR Glasses - Optimized for Raspberry Pi

Real-time text recognition and translation system optimized for Raspberry Pi performance.

## Key Optimizations

### Performance Improvements
- **Reduced Resolution**: 640x480 for optimal Pi performance
- **Frame Skipping**: Processes every 3rd frame for OCR
- **Multithreading**: Separate threads for capture, OCR, and translation
- **Queue Management**: Non-blocking queues prevent bottlenecks
- **Memory Optimization**: LRU caching and efficient preprocessing

### Accuracy Improvements
- **Enhanced Preprocessing**: CLAHE, Gaussian blur, morphological operations
- **Character Whitelist**: Filters out noise characters
- **Confidence Filtering**: Minimum 40% confidence threshold
- **Size Filtering**: Removes very small text detections
- **Optimized Tesseract Config**: OEM 3, PSM 6 for better recognition

## Setup Instructions

### For Raspberry Pi:
```bash
# Run the setup script
python3 setup_pi.py

# Or manual setup:
sudo apt update
sudo apt install -y tesseract-ocr tesseract-ocr-eng
pip3 install -r requirements.txt

# Enable camera and increase GPU memory
sudo raspi-config
# Navigate to: Interface Options > Camera > Enable
# Navigate to: Advanced Options > Memory Split > 128
```

### For other systems:
```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 main.py
```

Press 'q' to quit.

## Configuration

Edit `config.py` to adjust:
- Camera resolution and FPS
- OCR confidence thresholds
- Frame processing intervals
- Translation cache settings

## Performance Tips for Pi

1. **Increase GPU Memory**: Set to 128MB minimum
2. **Use Fast SD Card**: Class 10 or better
3. **Proper Cooling**: Prevent thermal throttling
4. **Close Unnecessary Services**: Free up CPU/memory
5. **Use Lite OS**: Raspberry Pi OS Lite for headless operation

## Troubleshooting

### Low Frame Rate
- Reduce `CAMERA_WIDTH` and `CAMERA_HEIGHT` in config.py
- Increase `OCR_FRAME_SKIP` value
- Lower `CAMERA_FPS`

### Poor OCR Accuracy
- Ensure good lighting conditions
- Adjust `OCR_MIN_CONFIDENCE` threshold
- Check camera focus
- Modify preprocessing parameters in `ocr.py`

### Memory Issues
- Reduce queue sizes in config.py
- Lower translation cache size
- Close other applications

## Architecture

```
Camera Thread → Frame Queue → OCR Thread → OCR Queue → Translation Thread → Result Queue → Display
```

Each component runs independently with non-blocking communication for optimal performance.
