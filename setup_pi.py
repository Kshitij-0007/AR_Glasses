#!/usr/bin/env python3
"""
Setup script for optimizing AR Glasses on Raspberry Pi
"""
import os
import subprocess
import sys

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def setup_tesseract():
    """Install and configure Tesseract for Pi"""
    print("Setting up Tesseract...")
    
    # Install tesseract
    if not run_command("sudo apt update"):
        print("Failed to update package list")
        return False
        
    if not run_command("sudo apt install -y tesseract-ocr tesseract-ocr-eng"):
        print("Failed to install Tesseract")
        return False
        
    # Set environment variable for better performance
    os.environ['OMP_THREAD_LIMIT'] = '2'
    
    print("Tesseract setup complete")
    return True

def optimize_pi_settings():
    """Optimize Pi settings for better performance"""
    print("Optimizing Pi settings...")
    
    # Increase GPU memory split
    if run_command("sudo raspi-config nonint do_memory_split 128"):
        print("GPU memory split set to 128MB")
    
    # Enable camera
    if run_command("sudo raspi-config nonint do_camera 0"):
        print("Camera enabled")
        
    print("Pi optimization complete")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("Failed to install dependencies")
        return False
        
    print("Dependencies installed")
    return True

def main():
    print("Setting up AR Glasses for Raspberry Pi...")
    
    if not setup_tesseract():
        print("Tesseract setup failed")
        return
        
    if not install_dependencies():
        print("Dependency installation failed")
        return
        
    optimize_pi_settings()
    
    print("\nSetup complete! You may need to reboot for all changes to take effect.")
    print("Run: python3 main.py")

if __name__ == "__main__":
    main()
