# 🚗 Automatic Vehicle Detection & Smart E-Challan Generator

An AI-powered traffic surveillance system that detects vehicles, identifies number plates, and automatically generates e-challans for traffic violations. This system aims to streamline traffic law enforcement by using real-time computer vision and OCR technology.

---

## 📌 Features

- 🔍 **Vehicle Detection:** Real-time detection using OpenCV and YOLO models.
- 📸 **Number Plate Recognition:** Extracts number plate text using EasyOCR.
- 🧠 **Violation Detection:** Detects no-entry violations, overspeeding, and helmet-less riders.
- 💼 **Smart E-Challan Generation:** Automatically generates and stores challans with vehicle and violation details.
- 💾 **Data Storage:** Violations, vehicle details, and payments stored in JSON and CSV formats.
- 🧾 **PDF Receipt Generator:** Generates downloadable challan receipts.
- 🔁 **Repeat Offense Tracking:** Increases fine for recurring offenders.
- 📹 **Live Camera Feed:** Real-time monitoring from connected CCTV or webcam.

---

## 🛠️ Tech Stack

| Component            | Technology       |
|---------------------|------------------|
| Backend Processing   | Python, OpenCV   |
| OCR Engine           | EasyOCR          |
| Object Detection     | YOLOv5 / Haar Cascades |
| Data Storage         | JSON, CSV        |
| Frontend             | HTML/CSS, Flask  |
| Deployment Ready     | Localhost, Vercel (for frontend) |

---

## 📂 Folder Structure

project-root/
│
├── camera_feed/              # Real-time video processing scripts
├── static/                   # Frontend assets (CSS, JS)
├── templates/                # HTML templates (Flask)
├── uploads/                  # Saved screenshots or violation videos
│
├── app.py                    # Main Flask application
├── vehicle_detection.py      # Object detection logic
├── plate_extractor.py        # EasyOCR-based plate recognition
├── challan_generator.py      # E-challan creation and saving
├── data.json                 # Stores vehicle and violation data
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation


---
🚀 How to Run
Clone the repository

bash
Copy
Edit
git clone https://github.com/Kishore276/Automatic-Vehicle-Detection-Smart-E-Challan-Generator-.git
cd Automatic-Vehicle-Detection-Smart-E-Challan-Generator-
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the application

bash
Copy
Edit
python app.py
Access the app in your browser

arduino
Copy
Edit
http://localhost:5000
👨‍💻 Developed By
Kishore Reddy
Passionate about AI, automation, and building digital solutions.
