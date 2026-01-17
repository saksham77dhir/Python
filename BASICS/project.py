# Install dependencies if not already installed
# pip install ultralytics opencv-python pandas matplotlib seaborn

import cv2
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from ultralytics import YOLO

# Load YOLO model (pretrained)
model = YOLO("yolov8n.pt")   # lightweight YOLOv8 model

# Path to dataset folder (put your images/videos here)
dataset_path = "dataset/"   # Example: "dataset/" should contain .mp4, .jpg, etc.

# Collect all files (videos + images)
files = glob.glob(os.path.join(dataset_path, "*.*"))

logs = []   # master log for all files

for file_path in files:
    ext = os.path.splitext(file_path)[1].lower()  # file extension
    file_name = os.path.basename(file_path)

    # ----------- Case 1: Video -----------
    if ext in [".mp4", ".avi", ".mov"]:
        print(f"[VIDEO] Processing {file_name}...")
        cap = cv2.VideoCapture(file_path)
        frame_no = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_no += 1

            results = model(frame)

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    cls_id = int(box.cls[0])
                    label = model.names[cls_id]
                    conf = float(box.conf[0])

                    if label in ["car", "bus", "truck", "motorbike", "bicycle"]:
                        logs.append([file_name, frame_no, label, conf])

        cap.release()

    # ----------- Case 2: Image -----------
    elif ext in [".jpg", ".jpeg", ".png"]:
        print(f"[IMAGE] Processing {file_name}...")
        frame = cv2.imread(file_path)

        results = model(frame)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = float(box.conf[0])

                if label in ["car", "bus", "truck", "motorbike", "bicycle"]:
                    logs.append([file_name, None, label, conf])

# ----------- Save All Logs -----------
df = pd.DataFrame(logs, columns=["file_name", "frame", "vehicle_type", "confidence"])
df.to_csv("traffic_dataset_logs.csv", index=False)

print("\n✅ Processing complete! Logs saved to 'traffic_dataset_logs.csv'")
print(df.head())

# ----------- Simple Analytics -----------
plt.figure(figsize=(8,5))
sns.countplot(data=df, x="vehicle_type", order=df["vehicle_type"].value_counts().index)
plt.title("Vehicle Counts by Type")
plt.show()
