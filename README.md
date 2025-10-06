# Automatic Vehicle Detection & Smart E-Challan Generator

**Repository:** https://github.com/Kishore276/Automatic-Vehicle-Detection-Smart-E-Challan-Generator-.git

## Overview
This project is a complete Traffic Violation Management System that uses computer vision and machine learning to detect vehicle license plates, generate electronic challans (e-challans), and manage payments through a modern web interface.

## Features
- **Automatic Vehicle Detection** using YOLO and OpenCV
- **License Plate Recognition** with EasyOCR
- **E-Challan Generation** and management
- **Admin Dashboard** with real-time statistics and analytics
- **User and Admin Authentication**
- **Email Notifications** for new challans
- **Video Upload and Live Camera Detection**
- **Settings Page** for system configuration
- **Data Export and Management**
- **Role-based Access Control**

## Technologies Used
- Python, Flask, OpenCV, EasyOCR, PyTesseract
- Bootstrap 5, Font Awesome, Chart.js, SweetAlert2
- YOLOv3 (yolov3.weights, yolov3.cfg, coco.names)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Kishore276/Automatic-Vehicle-Detection-Smart-E-Challan-Generator-.git
cd Automatic-Vehicle-Detection-Smart-E-Challan-Generator-
```

### 2. Install Dependencies
Make sure you have Python 3.8+ installed, then install the required packages:
```bash
pip install -r requirements.txt
```

**Required Dependencies:**
- opencv-python==4.8.0.74
- numpy==1.24.3
- pytesseract==0.3.10
- Pillow==10.0.0
- imutils==0.5.4
- scikit-image==0.21.0
- matplotlib==3.7.2
- Flask
- easyocr

### 3. Prerequisites
- **Tesseract OCR:** Install Tesseract for additional OCR support
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`

### 4. Model Files
The repository includes pre-trained models:
- YOLOv3 weights (`yolov3.weights`) - Already included
- YOLO configuration (`yolov3.cfg`) - Already included
- COCO class names (`coco.names`) - Already included
- Text detection models in `model/` folder

### 5. Run the Application
Start the Flask development server:
```bash
python server.py
```

### 6. Access the Application
Open your web browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

## Usage
- **Admin Login:** Username: `admin`, Password: `admin123`
- **Dashboard:** View, filter, and manage all challans
- **Upload Video:** Upload MP4 files for detection
- **Statistics:** View analytics and charts (admin only)
- **Settings:** Configure detection, email, and system options
- **Developed By / Guided By:** View project team and mentor

## Project Directory Structure
```
Moving-Vehicle-Registration-Plate-Detection-main/
├── server.py                    # Main Flask web server
├── camera.py                    # Real-time vehicle detection module
├── mailgun.py                   # Email notification service
├── requirements.txt             # Python dependencies
├── data.json                    # Challan records database
├── users.json                   # User authentication data
├── switch.txt                   # Camera detection toggle
├── yolov3.weights              # YOLO neural network weights
├── yolov3.cfg                  # YOLO configuration file
├── coco.names                  # COCO dataset class labels
├── output.avi                  # Video output file
├── LICENSE                     # Project license
├── README.md                   # Project documentation
├── model/                      # Machine learning models
│   ├── craft_mlt_25k.pth      # Text detection model
│   └── english_g2.pth          # English text recognition model
├── templates/                  # HTML templates
│   ├── index.html              # Main dashboard
│   ├── login.html              # Authentication page
│   ├── about_project.html      # Project information
│   ├── technology_used.html    # Technology stack
│   ├── developed_by.html       # Development team
│   ├── guided_by.html          # Project mentor
│   ├── upload_video.html       # Video upload interface
│   ├── statistics.html         # Analytics dashboard
│   └── settings.html           # System configuration
├── uploads/                    # Uploaded video files
│   └── [timestamp]/            # Timestamped upload folders
└── __pycache__/                # Python cache files
    ├── mailgun.cpython-311.pyc
    └── mailgun.cpython-312.pyc
```

## Credits
- Developed by: G.Yuva Kishore Reddy
- Guided by: Dr. S. P. Balakannan

---
<<<<<<< HEAD
For any issues or contributions, please open an issue or pull request.
=======
For any issues or contributions, please open an issue or pull request.
>>>>>>> 51c83a94fde8c2ef8e1c673c8b1929c611086c81
