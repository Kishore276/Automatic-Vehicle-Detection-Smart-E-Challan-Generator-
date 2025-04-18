# import os
# import cv2
# import easyocr
# from datetime import datetime
# import random
# import json
# import numpy as np
#
# # Initialize EasyOCR
# reader = easyocr.Reader(['en'], gpu=False)
#
# # Load YOLO for vehicle detection and classification
# net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# with open("coco.names", "r") as f:
#     classes = f.read().strip().split("\n")
#
# # Define vehicle types (from COCO dataset)
# vehicle_classes = ["car", "truck", "bus", "motorcycle"]
#
# # Initialize video capture
# cam = cv2.VideoCapture(0)
# cv2.namedWindow("cam")
#
# # Threshold for OCR confidence
# threshold = 0.25
#
# # Camera calibration parameters (adjust based on your camera)
# focal_length = 1.0  # Focal length in pixels
# known_width = 2.0  # Known width of a vehicle in meters (for reference)
#
# # Full paths to data.json and switch.txt
# data_file_path = r"C:\codes\Exsel Sfe side\Moving-Vehicle-Registration-Plate-Detection-main\data.json"
# switch_file_path = r"C:\codes\Exsel Sfe side\Moving-Vehicle-Registration-Plate-Detection-main\switch.txt"
#
# # Session-specific list to track processed vehicles
# processed_vehicles = []
#
#
# def estimate_dimensions(width_pixels):
#     return (known_width * focal_length) / width_pixels
#
#
# def extract_number_plate(roi):
#     # Preprocess the ROI
#     gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#     _, binary_roi = cv2.threshold(gray_roi, 128, 255, cv2.THRESH_BINARY)
#     cv2.imshow("Binary ROI", binary_roi)
#     cv2.waitKey(1)
#
#     # Perform OCR on the preprocessed ROI
#     result = reader.readtext(binary_roi)
#     print("OCR result:", result)  # Debugging: Print OCR result
#     if result:
#         text = result[0][1]  # Extract the text from the first result
#         confidence = result[0][2]  # Extract the confidence score
#         if confidence > threshold:  # Filter based on confidence threshold
#             print(f"Extracted text: {text}, Confidence: {confidence}")
#             return text.strip()
#     return ""
#
#
# def getRandomCharge():
#     return random.choice([100, 200, 300, 400, 500])
#
#
# def check(vehicleNo, score):
#     # List of all Indian state codes
#     valid_prefixes = (
#         'AP', 'AR', 'AS', 'BR', 'CG', 'GA', 'GJ', 'HR', 'HP', 'JH', 'KA', 'KL', 'MP', 'MH', 'MN', 'ML',
#         'MZ', 'NL', 'OD', 'PB', 'RJ', 'SK', 'TN', 'TS', 'TR', 'UP', 'UK', 'WB', 'AN', 'CH', 'DD', 'DL',
#         'JK', 'LA', 'LD', 'PY', 'UK', 'UP'
#     )
#
#     # Check if the vehicle number starts with a valid state code and has a minimum length
#     if any(vehicleNo.startswith(prefix) for prefix in valid_prefixes) and len(vehicleNo) >= 8:
#         try:
#             # Load existing data
#             if os.path.exists(data_file_path):
#                 with open(data_file_path, 'r') as f:
#                     data = json.load(f)
#             else:
#                 data = []
#
#             # Check if the vehicle number already exists in the session
#             if vehicleNo not in processed_vehicles:
#                 print("New vehicle detected:", vehicleNo, score)
#                 now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
#                 charge = getRandomCharge()
#                 data.append({
#                     'vehicleNo': vehicleNo,
#                     'time': now,
#                     'charge': charge,
#                     'paid': False
#                 })
#
#                 # Save updated data
#                 with open(data_file_path, 'w') as f:
#                     json.dump(data, f, indent=4)
#                     print("Data saved to data.json")
#
#                 # Add the vehicle to the session-specific list
#                 processed_vehicles.append(vehicleNo)
#             else:
#                 print("Vehicle already processed in this session.")
#         except Exception as e:
#             print(f"Error in check function: {e}")
#     else:
#         print(f"Invalid vehicle number: {vehicleNo}")
#
#
# def getSwitchValue():
#     if os.path.exists(switch_file_path):
#         with open(switch_file_path, 'r') as f:
#             return int(f.read().strip())
#     else:
#         return 0
#
#
# def start_cam():
#     while True:
#         ret, frame = cam.read()
#         print("Frame captured:", ret)  # Debugging: Print frame capture status
#
#         if not ret:
#             continue
#
#         height, width, _ = frame.shape
#
#         # YOLO object detection
#         blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
#         net.setInput(blob)
#         layer_names = net.getLayerNames()
#         unconnected_layers = net.getUnconnectedOutLayers()
#
#         if isinstance(unconnected_layers, np.ndarray):
#             output_layers = [layer_names[i - 1] for i in unconnected_layers.flatten()]
#         else:
#             output_layers = [layer_names[unconnected_layers - 1]]
#
#         detections = net.forward(output_layers)
#         print("Detections:", len(detections))  # Debugging: Print number of detections
#
#         # Process YOLO detections
#         boxes = []
#         confidences = []
#         class_ids = []
#         for out in detections:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#                 if confidence > 0.5 and classes[class_id] in vehicle_classes:  # Filter for vehicles
#                     center_x = int(detection[0] * width)
#                     center_y = int(detection[1] * height)
#                     w = int(detection[2] * width)
#                     h = int(detection[3] * height)
#                     x = int(center_x - w / 2)
#                     y = int(center_y - h / 2)
#
#                     boxes.append([x, y, w, h])
#                     confidences.append(float(confidence))
#                     class_ids.append(class_id)
#
#         # Non-maximum suppression
#         indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
#
#         # Draw bounding boxes and extract number plates
#         if isinstance(indices, np.ndarray):
#             for i in indices.flatten():
#                 x, y, w, h = boxes[i]
#
#                 # Draw bounding box
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#
#                 # Extract number plate (ROI)
#                 roi = frame[y:y + h, x:x + w]
#                 print("ROI extracted:", roi.shape if 'roi' in locals() else "No ROI")  # Debugging: Print ROI status
#                 cv2.imshow("ROI", roi)
#                 cv2.waitKey(1)
#
#                 number_plate_text = extract_number_plate(roi)
#
#                 # Display information
#                 if number_plate_text:
#                     label = f"Plate: {number_plate_text}"
#                     cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#
#                     # Check if the switch is on and process the number plate
#                     print("Switch value:", getSwitchValue())  # Debugging: Print switch status
#                     if getSwitchValue() == 1:
#                         check(number_plate_text, 1.0)  # Assuming high confidence for simplicity
#                     else:
#                         print("Switch is off")
#
#         # Display the frame
#         cv2.imshow("cam", frame)
#
#         k = cv2.waitKey(1)
#         if k == ord('q'):
#             print("q pressed, quitting...")
#             break
#
#     cam.release()
#     cv2.destroyAllWindows()
#
#
# if __name__ == '__main__':
#     start_cam()


# # # # import os
# # # # import json
# # # # import cv2
# # # # import easyocr
# # # # import random
# # # # import numpy as np
# # # # from datetime import datetime
# # # # import mailgun
# # # # import matplotlib.pyplot as plt  # Added for display if OpenCV GUI fails
# # # #
# # # # # Fix for OpenCV GUI error
# # # # os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# # # #
# # # # # Initialize EasyOCR
# # # # reader = easyocr.Reader(['en'], gpu=False)
# # # #
# # # # # Open webcam
# # # # cam = cv2.VideoCapture(0)
# # # #
# # # # # Threshold for text detection confidence
# # # # threshold = 0.25
# # # #
# # # #
# # # # def getRandomCharge():
# # # #     """Returns a random fine charge."""
# # # #     charges = [100, 200, 300, 400, 500]
# # # #     return random.choice(charges)
# # # #
# # # #
# # # # def check(vehicleNo, score):
# # # #     """Checks if the vehicle number is already recorded, and if not, adds it to data.json."""
# # # #
# # # #     if vehicleNo.startswith('MH') and len(vehicleNo) >= 8:
# # # #         try:
# # # #             with open('data.json', 'r') as f:
# # # #                 data = json.load(f)
# # # #         except (FileNotFoundError, json.JSONDecodeError):
# # # #             data = []
# # # #
# # # #         if not any(d['vehicleNo'] == vehicleNo for d in data):
# # # #             print(f"New vehicle {vehicleNo} detected. Adding to file...")
# # # #             now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# # # #             charge = getRandomCharge()
# # # #
# # # #             data.append({'vehicleNo': vehicleNo, 'time': now, 'charge': charge, 'paid': False})
# # # #
# # # #             with open('data.json', 'w') as f:
# # # #                 json.dump(data, f, indent=4)
# # # #
# # # #             print("Sending Email...")
# # # #             mailgun.mail(
# # # #                 "New Challan Generated",
# # # #                 f"Hello, Your vehicle {vehicleNo} has been detected at {now}. "
# # # #                 f"Please pay the fine of Rs. {charge} to avoid legal action."
# # # #             )
# # # #         else:
# # # #             print(f"Vehicle {vehicleNo} already recorded.")
# # # #
# # # #
# # # # def getSwitchValue():
# # # #     """Reads the switch value from switch.txt."""
# # # #     try:
# # # #         with open('switch.txt', 'r') as f:
# # # #             return int(f.read().strip())
# # # #     except (FileNotFoundError, ValueError):
# # # #         return 0  # Default to 'off' if file not found or invalid
# # # #
# # # #
# # # # def display_frame(frame):
# # # #     """Displays frame using OpenCV or Matplotlib if OpenCV GUI fails."""
# # # #     try:
# # # #         cv2.imshow("Camera", frame)
# # # #     except cv2.error:
# # # #         plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
# # # #         plt.axis('off')
# # # #         plt.show()
# # # #
# # # #
# # # # def start_cam():
# # # #     """Starts the webcam and processes frames for license plate detection."""
# # # #     while True:
# # # #         ret, frame = cam.read()
# # # #         if not ret:
# # # #             continue
# # # #
# # # #         frame = cv2.resize(frame, (350, 300))
# # # #
# # # #         text_ = reader.readtext(frame)
# # # #
# # # #         for _, (bbox, text, score) in enumerate(text_):
# # # #             if score > threshold:
# # # #                 try:
# # # #                     cv2.putText(frame, text, tuple(map(int, bbox[0])),
# # # #                                 cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
# # # #                 except Exception:
# # # #                     pass
# # # #
# # # #                 if getSwitchValue() == 1:
# # # #                     check(text, score)
# # # #                 else:
# # # #                     print("Switch is off")
# # # #
# # # #         display_frame(frame)
# # # #
# # # #         if cv2.waitKey(1) & 0xFF == ord('q'):
# # # #             print("Quitting...")
# # # #             break
# # # #
# # # #     cam.release()
# # # #     cv2.destroyAllWindows()
# # # #
# # # #
# # # # if __name__ == '__main__':
# # # #     start_cam()
# # #
# # # # import os
# # # # import json
# # # # import cv2
# # # # import easyocr
# # # # import random
# # # # import numpy as np
# # # # from datetime import datetime
# # # # import mailgun
# # # # import matplotlib.pyplot as plt  # Fallback for display
# # # #
# # # # # Fix for OpenCV GUI error
# # # # os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# # # #
# # # # # Initialize EasyOCR
# # # # reader = easyocr.Reader(['en'], gpu=False)
# # # #
# # # # # Open webcam
# # # # cam = cv2.VideoCapture(0)
# # # #
# # # # # Define video writer (saves as output.avi)
# # # # frame_width = int(cam.get(3))
# # # # frame_height = int(cam.get(4))
# # # # fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # # # video_writer = cv2.VideoWriter("output.avi", fourcc, 10, (frame_width, frame_height))
# # # #
# # # # # Threshold for text detection confidence
# # # # threshold = 0.25
# # # #
# # # #
# # # # def getRandomCharge():
# # # #     """Returns a random fine charge."""
# # # #     charges = [100, 200, 300, 400, 500]
# # # #     return random.choice(charges)
# # # #
# # # #
# # # # def check(vehicleNo, score):
# # # #     """Checks if the vehicle number is already recorded, and if not, adds it to data.json."""
# # # #
# # # #     if vehicleNo.startswith('MH') and len(vehicleNo) >= 8:
# # # #         try:
# # # #             with open('data.json', 'r') as f:
# # # #                 data = json.load(f)
# # # #         except (FileNotFoundError, json.JSONDecodeError):
# # # #             data = []
# # # #
# # # #         if not any(d['vehicleNo'] == vehicleNo for d in data):
# # # #             print(f"New vehicle {vehicleNo} detected. Adding to file...")
# # # #             now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# # # #             charge = getRandomCharge()
# # # #
# # # #             data.append({'vehicleNo': vehicleNo, 'time': now, 'charge': charge, 'paid': False})
# # # #
# # # #             with open('data.json', 'w') as f:
# # # #                 json.dump(data, f, indent=4)
# # # #
# # # #             print("Sending Email...")
# # # #             mailgun.mail(
# # # #                 "New Challan Generated",
# # # #                 f"Hello, Your vehicle {vehicleNo} has been detected at {now}. "
# # # #                 f"Please pay the fine of Rs. {charge} to avoid legal action."
# # # #             )
# # # #         else:
# # # #             print(f"Vehicle {vehicleNo} already recorded.")
# # # #
# # # #
# # # # def getSwitchValue():
# # # #     """Reads the switch value from switch.txt."""
# # # #     try:
# # # #         with open('switch.txt', 'r') as f:
# # # #             return int(f.read().strip())
# # # #     except (FileNotFoundError, ValueError):
# # # #         return 0  # Default to 'off' if file not found or invalid
# # # #
# # # #
# # # # def display_frame(frame):
# # # #     """Displays frame using OpenCV or Matplotlib if OpenCV GUI fails."""
# # # #     try:
# # # #         cv2.imshow("Camera", frame)
# # # #     except cv2.error:
# # # #         plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
# # # #         plt.axis('off')
# # # #         plt.show()
# # # #
# # # #
# # # # def start_cam():
# # # #     """Starts the webcam, records video, and detects license plates."""
# # # #     while True:
# # # #         ret, frame = cam.read()
# # # #         if not ret:
# # # #             continue
# # # #
# # # #         frame = cv2.resize(frame, (640, 480))
# # # #
# # # #         # Detect text
# # # #         text_ = reader.readtext(frame)
# # # #
# # # #         for _, (bbox, text, score) in enumerate(text_):
# # # #             if score > threshold:
# # # #                 try:
# # # #                     cv2.putText(frame, text, tuple(map(int, bbox[0])),
# # # #                                 cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
# # # #                 except Exception:
# # # #                     pass
# # # #
# # # #                 if getSwitchValue() == 1:
# # # #                     check(text, score)
# # # #                 else:
# # # #                     print("Switch is off")
# # # #
# # # #         # Write frame to video file
# # # #         video_writer.write(frame)
# # # #
# # # #         # Display frame
# # # #         display_frame(frame)
# # # #
# # # #         if cv2.waitKey(1) & 0xFF == ord('q'):
# # # #             print("Quitting...")
# # # #             break
# # # #
# # # #     cam.release()
# # # #     video_writer.release()
# # # #     cv2.destroyAllWindows()
# # # #
# # # #
# # # # if __name__ == '__main__':
# # # #     start_cam()
# # #
# # #
# # # import os
# # # import json
# # # import cv2
# # # import easyocr
# # # import random
# # # import numpy as np
# # # from datetime import datetime
# # # import mailgun
# # # import matplotlib.pyplot as plt  # Fallback for display
# # #
# # # # Fix for OpenCV GUI error
# # # os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
# # #
# # # # Initialize EasyOCR
# # # reader = easyocr.Reader(['en'], gpu=False)
# # #
# # # # Open webcam
# # # cam = cv2.VideoCapture(0)
# # #
# # # # Define video writer (saves as output.avi)
# # # frame_width = int(cam.get(3))
# # # frame_height = int(cam.get(4))
# # # fourcc = cv2.VideoWriter_fourcc(*'XVID')
# # # video_writer = cv2.VideoWriter("output.avi", fourcc, 10, (frame_width, frame_height))
# # #
# # # # Threshold for text detection confidence
# # # threshold = 0.25
# # #
# # # def getRandomCharge():
# # #     """Returns a random fine charge."""
# # #     charges = [100, 200, 300, 400, 500]
# # #     return random.choice(charges)
# # #
# # # def check(vehicleNo, score):
# # #     """Checks if the vehicle number is already recorded, and if not, adds it to data.json."""
# # #     if vehicleNo.startswith('MH') and len(vehicleNo) >= 8:
# # #         try:
# # #             with open('data.json', 'r') as f:
# # #                 data = json.load(f)
# # #         except (FileNotFoundError, json.JSONDecodeError):
# # #             data = []
# # #
# # #         if not any(d['vehicleNo'] == vehicleNo for d in data):
# # #             print(f"New vehicle {vehicleNo} detected. Adding to file...")
# # #             now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# # #             charge = getRandomCharge()
# # #
# # #             data.append({'vehicleNo': vehicleNo, 'time': now, 'charge': charge, 'paid': False})
# # #
# # #             with open('data.json', 'w') as f:
# # #                 json.dump(data, f, indent=4)
# # #
# # #             print("Sending Email...")
# # #             mailgun.mail(
# # #                 "New Challan Generated",
# # #                 f"Hello, Your vehicle {vehicleNo} has been detected at {now}. "
# # #                 f"Please pay the fine of Rs. {charge} to avoid legal action."
# # #             )
# # #         else:
# # #             print(f"Vehicle {vehicleNo} already recorded.")
# # #
# # # def getSwitchValue():
# # #     """Reads the switch value from switch.txt."""
# # #     try:
# # #         with open('switch.txt', 'r') as f:
# # #             return int(f.read().strip())
# # #     except (FileNotFoundError, ValueError):
# # #         return 0  # Default to 'off' if file not found or invalid
# # #
# # # def display_frame(frame):
# # #     """Displays frame using OpenCV or Matplotlib if OpenCV GUI fails."""
# # #     try:
# # #         cv2.imshow("Camera", frame)
# # #     except cv2.error:
# # #         plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
# # #         plt.axis('off')
# # #         plt.show()
# # #
# # # def start_cam():
# # #     """Starts the webcam, records video, and detects license plates."""
# # #     while True:
# # #         ret, frame = cam.read()
# # #         if not ret:
# # #             continue
# # #
# # #         frame = cv2.resize(frame, (640, 480))
# # #
# # #         # Detect text
# # #         text_ = reader.readtext(frame)
# # #
# # #         for _, (bbox, text, score) in enumerate(text_):
# # #             if score > threshold:
# # #                 try:
# # #                     cv2.putText(frame, text, tuple(map(int, bbox[0])),
# # #                                 cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
# # #                 except Exception:
# # #                     pass
# # #
# # #                 if getSwitchValue() == 1:
# # #                     check(text, score)
# # #                 else:
# # #                     print("Switch is off")
# # #
# # #         # Write frame to video file
# # #         video_writer.write(frame)
# # #
# # #         # Display frame
# # #         display_frame(frame)
# # #
# # #         if cv2.waitKey(1) & 0xFF == ord('q'):
# # #             print("Quitting...")
# # #             break
# # #
# # #     cam.release()
# # #     video_writer.release()
# # #     cv2.destroyAllWindows()
# # #
# # # if __name__ == '__main__':
# # #     start_cam()
# #
# #
# # import cv2
# # import numpy as np
# # import pytesseract
# # import json
# # import os
# # from datetime import datetime
# # import time
# #
# #
# # # Load YOLO Model
# # def load_yolo():
# #     net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# #     with open("coco.names", "r") as f:
# #         classes = [line.strip() for line in f]
# #     return net, classes
# #
# #
# # # Extract License Plate Text
# # def extract_license_plate(image):
# #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# #     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# #     config = '--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
# #     text = pytesseract.image_to_string(thresh, config=config)
# #     return text.strip()
# #
# #
# # # Save Data to JSON
# # def save_violation(data):
# #     file_path = "data.json"
# #     if os.path.exists(file_path):
# #         with open(file_path, "r") as file:
# #             violations = json.load(file)
# #     else:
# #         violations = []
# #
# #     violations.append(data)
# #     with open(file_path, "w") as file:
# #         json.dump(violations, file, indent=4)
# #
# #
# # # Main Function
# # def main():
# #     net, classes = load_yolo()
# #     cap = cv2.VideoCapture(0)  # Use webcam
# #
# #     while True:
# #         with open("switch.txt", "r") as file:
# #             if file.read().strip() == "0":
# #                 print("Detection turned off.")
# #                 break
# #
# #         ret, frame = cap.read()
# #         if not ret:
# #             break
# #
# #         height, width = frame.shape[:2]
# #         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
# #         net.setInput(blob)
# #         layer_names = net.getUnconnectedOutLayersNames()
# #         outs = net.forward(layer_names)
# #
# #         for out in outs:
# #             for detection in out:
# #                 scores = detection[5:]
# #                 class_id = np.argmax(scores)
# #                 confidence = scores[class_id]
# #
# #                 if confidence > 0.5 and classes[class_id] in ["car", "truck", "bus", "motorcycle"]:
# #                     box = detection[0:4] * np.array([width, height, width, height])
# #                     (x, y, w, h) = box.astype("int")
# #                     x, y = max(0, x), max(0, y)
# #
# #                     # Extract license plate
# #                     license_plate = extract_license_plate(frame[y:y + h, x:x + w])
# #
# #                     # Save violation
# #                     violation_data = {
# #                         "vehicleNo": license_plate,
# #                         "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
# #                         "charge": 200,  # Example charge
# #                         "paid": False
# #                     }
# #                     save_violation(violation_data)
# #
# #         time.sleep(1)  # Small delay to reduce CPU usage
# #
# #     cap.release()
# #     print("Detection stopped.")
# #
# #
# # if __name__ == "__main__":
# #     main()
#
#
# import cv2
# import numpy as np
# import pytesseract
# import json
# import os
# from datetime import datetime
# import time
#
# # Load YOLO Model
# def load_yolo():
#     net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
#     with open("coco.names", "r") as f:
#         classes = [line.strip() for line in f]
#     return net, classes
#
# # Extract License Plate Text
# def extract_license_plate(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#     config = '--psm 8 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#     text = pytesseract.image_to_string(thresh, config=config)
#     return text.strip()
#
# # Save Data to JSON
# def save_violation(data):
#     file_path = "data.json"
#     if os.path.exists(file_path):
#         with open(file_path, "r") as file:
#             violations = json.load(file)
#     else:
#         violations = []
#
#     violations.append(data)
#     with open(file_path, "w") as file:
#         json.dump(violations, file, indent=4)
#
# # Main Function
# def main():
#     net, classes = load_yolo()
#     cap = cv2.VideoCapture(0)  # Open webcam
#
#     if not cap.isOpened():
#         print("Error: Could not open camera.")
#         return
#
#     while True:
#         with open("switch.txt", "r") as file:
#             if file.read().strip() == "0":
#                 print("Detection turned off.")
#                 break
#
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: Could not read frame.")
#             break
#
#         height, width = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
#         net.setInput(blob)
#         layer_names = net.getUnconnectedOutLayersNames()
#         outs = net.forward(layer_names)
#
#         for out in outs:
#             for detection in out:
#                 scores = detection[5:]
#                 class_id = np.argmax(scores)
#                 confidence = scores[class_id]
#
#                 if confidence > 0.5 and classes[class_id] in ["car", "truck", "bus", "motorcycle"]:
#                     box = detection[0:4] * np.array([width, height, width, height])
#                     (x, y, w, h) = box.astype("int")
#                     x, y = max(0, x), max(0, y)
#
#                     # Extract license plate
#                     license_plate = extract_license_plate(frame[y:y + h, x:x + w])
#
#                     # Save violation
#                     violation_data = {
#                         "vehicleNo": license_plate,
#                         "time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
#                         "charge": 200,  # Example charge
#                         "paid": False
#                     }
#                     save_violation(violation_data)
#
#         time.sleep(1)  # Small delay to reduce CPU usage
#
#     cap.release()
#     print("Detection stopped.")
#
# if __name__ == "__main__":
#     main()



import os
import json
import cv2
import easyocr
import random
import numpy as np
from datetime import datetime
import mailgun
import matplotlib.pyplot as plt  # Fallback for display

# Fix for OpenCV GUI error
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

# Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# Open webcam
cam = cv2.VideoCapture(0)

# Define video writer (saves as output.avi)
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter("output.avi", fourcc, 10, (frame_width, frame_height))

# Threshold for text detection confidence
threshold = 0.5


def getRandomCharge():
    """Returns a random fine charge."""
    charges = [100, 200, 300, 400, 500]
    return random.choice(charges)


def check(vehicleNo, score):
    """Checks if the vehicle number is already recorded, and if not, adds it to data.json."""

    if vehicleNo.startswith(('MH', 'KA', 'AP', 'KL', 'TS', 'MP', 'RJ', 'HR', 'TN', 'AS', )) and len(vehicleNo) >= 8:
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        if not any(d['vehicleNo'] == vehicleNo for d in data):
            print(f"New vehicle {vehicleNo} detected. Adding to file...")
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            charge = getRandomCharge()

            data.append({'vehicleNo': vehicleNo, 'time': now, 'charge': charge, 'paid': False})

            with open('data.json', 'w') as f:
                json.dump(data, f, indent=4)

            print("Sending Email...")
            mailgun.mail(
                "New Challan Generated",
                f"Hello, Your vehicle {vehicleNo} has been detected at {now}. "
                f"Please pay the fine of Rs. {charge} to avoid legal action."
            )
        else:
            print(f"Vehicle {vehicleNo} already recorded.")


def getSwitchValue():
    """Reads the switch value from switch.txt."""
    try:
        with open('switch.txt', 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0  # Default to 'off' if file not found or invalid


def display_frame(frame):
    """Displays frame using OpenCV or Matplotlib if OpenCV GUI fails."""
    try:
        cv2.imshow("Camera", frame)
    except cv2.error:
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()


def start_cam():
    """Starts the webcam, records video, and detects license plates."""
    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        frame = cv2.resize(frame, (640, 480))

        # Detect text
        text_ = reader.readtext(frame)

        for _, (bbox, text, score) in enumerate(text_):
            if score > threshold:
                try:
                    cv2.putText(frame, text, tuple(map(int, bbox[0])),
                                cv2.FONT_HERSHEY_COMPLEX, 0.65, (255, 0, 0), 2)
                except Exception:
                    pass

                if getSwitchValue() == 1:
                    check(text, score)
                else:
                    print("Switch is off")

        # Write frame to video file
        video_writer.write(frame)

        # Display frame
        display_frame(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break

    cam.release()
    video_writer.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_cam()
