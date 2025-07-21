# Automatic Vehicle Detection & Smart E-Challan Generator

An AI-powered traffic surveillance system that detects vehicles, identifies number plates, and automatically generates e-challans for traffic violations. This system uses real-time computer vision and OCR to streamline traffic law enforcement.

## Features

- Real-time vehicle detection using OpenCV
- Number plate recognition with EasyOCR
- No-entry & helmet violation detection
- Automatic e-challan generation
- Data storage in JSON & CSV formats
- PDF receipt generation for fines
- Repeat violation tracking
- Live CCTV/webcam feed integration

## Tech Stack

Backend: Python, Flask  
Detection: OpenCV, YOLO  
OCR: EasyOCR  
Storage: JSON, CSV  
Frontend: HTML/CSS, Bootstrap  
Deployment: Localhost, Vercel  

## Folder Structure

project-root/
├── camera_feed/             # Real-time video processing
├── static/                  # Frontend assets (CSS, JS)
├── templates/               # HTML templates for Flask
├── uploads/                 # Saved violation screenshots or videos
├── app.py                   # Main Flask app
├── vehicle_detection.py     # Object detection logic
├── plate_extractor.py       # Number plate recognition using EasyOCR
├── challan_generator.py     # E-challan creation logic
├── data.json                # Stores vehicle & violation data
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

## How to Run

1. Clone the Repository

git clone https://github.com/Kishore276/Automatic-Vehicle-Detection-Smart-E-Challan-Generator-.git  
cd Automatic-Vehicle-Detection-Smart-E-Challan-Generator-

2. Install Dependencies

pip install -r requirements.txt

3. Run the Application

python app.py

## Future Enhancements

- Admin login & dashboard
- Cloud deployment (e.g., AWS, Azure)
- SMS/email notification to violators
- Vehicle type classification (bike, car, truck, etc.)
- Analytics dashboard for violation trends

## Developed By

G.Yuva Kishore Reddy  
Passionate about AI, automation, and building impactful tech solutions.

## Contact

Email: g.yuvakishorereddy@gmail.com  
Instagram: https://instagram.com/g.yuvakishorereddy  
WhatsApp Channel: https://whatsapp.com/channel/0029Vb3la9V7NoZtA1GUI00d

Star this repo if you found it helpful!
