# Project: AR_Glasses
Lightweight AR-style text scanner + translator prototype (CPU-friendly, multithreaded).

## Features
- Camera capture (OpenCV)
- CPU OCR via Tesseract (pytesseract)
- Simple translation using `googletrans`
- Multithreaded pipeline: Capture -> OCR workers -> Translator -> Display
- Designed to run on CPU-only systems (desktop and Raspberry Pi)

## Files
- main.py
- capture.py
- ocr.py
- translate.py
- display.py
- requirements.txt

## Setup (Desktop)
1. Install Tesseract:
   - Ubuntu/Debian: `sudo apt update && sudo apt install -y tesseract-ocr libtesseract-dev`
   - Windows: install from https://github.com/tesseract-ocr/tesseract
2. Python deps:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
3. Run:
```
python main.py
```

## Setup (Raspberry Pi)
```
sudo apt update
sudo apt install -y tesseract-ocr libtesseract-dev libjpeg-dev zlib1g-dev
pip3 install -r requirements.txt
python3 main.py
```

## Git push (local)
```
git clone https://github.com/Kshitij-0007/AR_Glasses.git
cd AR_Glasses
# copy files into this folder, then:
git add .
git commit -m "Initial AR_Glasses prototype"
git push origin main
```
