import os
os.environ["KMP_DUPLICATE_LIB_OK"]= 'TRUE'
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for
import json
import cv2
import easyocr
from datetime import datetime
import random
import mailgun
import subprocess
import hashlib
import shutil

# Define the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, 'static')
app = Flask(__name__)

# Configure upload folders
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Threshold for OCR confidence
threshold = 0.25
reader = easyocr.Reader(['en'], gpu=False)

# Global variable to store the camera subprocess
camera_process = None

# User management functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create initial admin user if file doesn't exist
        initial_users = {
            "users": [{
                "username": "admin",
                "password": hash_password("admin123"),
                "email": "admin@system.com",
                "role": "admin",
                "created_at": datetime.utcnow().isoformat(),
                "last_login": None
            }]
        }
        with open('users.json', 'w') as f:
            json.dump(initial_users, f, indent=4)
        return initial_users

def save_users(users_data):
    with open('users.json', 'w') as f:
        json.dump(users_data, f, indent=4)

def find_user(username):
    users_data = load_users()
    for user in users_data['users']:
        if user['username'] == username:
            return user
    return None

def deleteItem(vehicleNo):
    items = []
    with open('data.json', 'r') as f:
        items = json.load(f)

    for i in range(len(items)):
        if items[i]['vehicleNo'] == vehicleNo:
            print('deleting', items[i])
            del items[i]
            break

    with open('data.json', 'w') as f:
        json.dump(items, f, indent=4)

def payTheChallan(vehicleNo, amount=None):
    with open('data.json', 'r') as f:
        items = json.load(f)

    for item in items:
        if item['vehicleNo'] == vehicleNo:
            item['paid'] = True
            item['paid_amount'] = amount if amount else item['charge']
            item['payment_date'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            break

    with open('data.json', 'w') as f:
        json.dump(items, f, indent=4)

def getItemsList():
    try:
        with open('data.json', 'r') as f:
            items = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        items = []
        with open('data.json', 'w') as f:
            json.dump(items, f, indent=4)
    return items

def getRandomCharge():
    charges = [100, 200, 300, 400, 500]
    return charges[random.randint(0, len(charges) - 1)]

def check(vehicleNo, score):
    if vehicleNo.startswith(('MH', 'MP', 'AP', 'TN', 'TS')) and len(vehicleNo) >= 8:
        with open('data.json', 'r') as f:
            data = json.load(f)

        if not any(d['vehicleNo'] == vehicleNo for d in data):
            print("New vehicle detected:", vehicleNo, score)
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            charge = getRandomCharge()
            data.append({'vehicleNo': vehicleNo, 'time': now, 'charge': charge, 'paid': False})

            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)

            print("Sending Email notification...")
            mailgun.mail("New challan generated",
                         f"Hello, Your vehicle {vehicleNo} has been detected at {now}. "
                         f"Please pay the challan of Rs. {charge} to avoid legal action.")
        else:
            print("Vehicle already recorded.")

def getSwitchValue():
    with open('switch.txt', 'r') as f:
        return int(f.read().strip())

def readVideo(filepath):
    cam = cv2.VideoCapture(filepath)
    print("Processing:", filepath)

    while cam.isOpened():
        ret, frame = cam.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (350, 300))
        text_ = reader.readtext(frame)

        for bbox, text, score in text_:
            if score > threshold:
                try:
                    cv2.putText(frame, text, bbox[0], cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
                except:
                    pass

                if getSwitchValue() == 1:
                    check(text, score)
                else:
                    print("Switch is OFF")

        cv2.imshow("video", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/upload_video.html')
def uploadvideo():
    return render_template('upload_video.html')

@app.route('/about_project.html')
def aboutproject():
    return render_template('about_project.html')

@app.route('/guided_by.html')
def guidedetails():
    return render_template('guided_by.html')

@app.route('/technology_used.html')
def technology():
    return render_template('technology_used.html')

@app.route('/developed_by.html')
def developby():
    return render_template('developed_by.html')

@app.route('/add-challan', methods=['POST'])
def addChallan():
    data = request.get_json()
    vehicleNo = data.get('vehicleNo')
    charge = data.get('charge', getRandomCharge())
    
    if not vehicleNo:
        return jsonify({'error': 'Vehicle number is required'}), 400
        
    items = getItemsList()
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    items.append({
        'vehicleNo': vehicleNo,
        'time': now,
        'charge': charge,
        'paid': False
    })
    
    with open('data.json', 'w') as f:
        json.dump(items, f, indent=4)
        
    return jsonify({'msg': 'Challan added successfully'})

@app.route('/<path:path>')
def serve_static(path):
    if os.path.isdir(os.path.join(static_path, path)):
        path = os.path.join(path, 'index.html')
    return send_from_directory(static_path, path)

@app.route('/getItems')
def getItemsJson():
    return jsonify(getItemsList())

@app.route('/getSwitch')
def getSwitch():
    try:
        with open('switch.txt', 'r') as f:
            return jsonify({'switch': int(f.read())})
    except FileNotFoundError:
        with open('switch.txt', 'w') as f:
            f.write('0')
        return jsonify({'switch': 0})

@app.route('/setSwitch', methods=['POST'])
def setSwitch():
    global camera_process
    reqjson = request.get_json()
    switch_val = reqjson['switch']
    
    try:
        if switch_val == 1:  # Start Detection
            if camera_process is None:  # Only start if not already running
                camera_process = subprocess.Popen(['python', 'camera.py'])
                return jsonify({'msg': 'Camera detection started', 'status': 'success'})
            else:
                return jsonify({'msg': 'Camera detection is already running', 'status': 'warning'})
        else:  # Stop Detection
            if camera_process is not None:
                camera_process.terminate()
                camera_process = None
                return jsonify({'msg': 'Camera detection stopped', 'status': 'success'})
            else:
                return jsonify({'msg': 'Camera detection is not running', 'status': 'warning'})
    except Exception as e:
        return jsonify({'msg': f'Error: {str(e)}', 'status': 'error'})

@app.route('/deleteItem', methods=['POST'])
def deleteFromJson():
    reqjson = request.get_json()
    vehicleNo = reqjson['vehicleNo']
    deleteItem(vehicleNo)
    return jsonify({'msg': 'ok'})

@app.route('/pay-challan', methods=['POST'])
def payChallan():
    reqjson = request.get_json()
    vehicleNo = reqjson['vehicleNo']
    amount = reqjson.get('amount')  # Optional amount parameter
    payTheChallan(vehicleNo, amount)
    return jsonify({'msg': 'ok'})

@app.route('/predict-video', methods=['POST'])
def predictVideo():
    if 'vidfile' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
        
    video_file = request.files['vidfile']
    if video_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if video_file:
        # Create a timestamp-based directory for this upload
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], timestamp)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the video file
        filename = f"video_{timestamp}.mp4"
        filepath = os.path.join(upload_dir, filename)
        video_file.save(filepath)
        
        try:
            readVideo(filepath)
            return jsonify({'msg': 'Video processed successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Keep the video file in uploads folder
            pass

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not all([username, password, email]):
        return jsonify({"error": "Missing required fields"}), 400

    users_data = load_users()
    
    # Check if username already exists
    if any(user['username'] == username for user in users_data['users']):
        return jsonify({"error": "Username already exists"}), 400

    # Create new user with hashed password
    new_user = {
        "username": username,
        "password": hash_password(password),
        "email": email,
        "role": "user",
        "created_at": datetime.utcnow().isoformat(),
        "last_login": None
    }

    users_data['users'].append(new_user)
    save_users(users_data)

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return jsonify({"error": "Missing credentials"}), 400

    users_data = load_users()
    user = next((user for user in users_data['users'] 
                 if user['username'] == username and 
                 user['password'] == hash_password(password)), None)
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # Update last login time
    for u in users_data['users']:
        if u['username'] == username:
            u['last_login'] = datetime.utcnow().isoformat()
            break
    save_users(users_data)

    return jsonify({
        "message": "Login successful",
        "user": {
            "username": user['username'],
            "email": user['email'],
            "role": user['role']
        }
    }), 200

@app.route('/statistics.html')
def statistics():
    return render_template('statistics.html')

@app.route('/settings.html')
def settings():
    return render_template('settings.html')

@app.route('/get-stats')
def getStats():
    items = getItemsList()
    
    total_violations = len(items)
    paid_challans = len([item for item in items if item.get('paid', False)])
    pending_challans = total_violations - paid_challans
    total_revenue = sum([item.get('charge', 0) for item in items if item.get('paid', False)])
    
    # Calculate monthly data for charts
    monthly_data = {}
    for item in items:
        try:
            date_str = item.get('time', '')
            if '/' in date_str:
                month = date_str.split('/')[1]
                year = date_str.split('/')[2].split(' ')[0]
                month_key = f"{month}/{year}"
                monthly_data[month_key] = monthly_data.get(month_key, 0) + 1
        except:
            continue
    
    return jsonify({
        'totalViolations': total_violations,
        'paidChallans': paid_challans,
        'pendingChallans': pending_challans,
        'totalRevenue': total_revenue,
        'monthlyData': monthly_data
    })

if __name__ == '__main__':
    # Create data.json if it doesn't exist
    if not os.path.exists('data.json'):
        with open('data.json', 'w') as f:
            json.dump([], f)
            
    # Create switch.txt if it doesn't exist
    if not os.path.exists('switch.txt'):
        with open('switch.txt', 'w') as f:
            f.write('0')
            
    app.run(debug=True)