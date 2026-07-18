import cv2 
import os 
import pickle 
import csv 
from datetime import datetime 
from src.detection.face_detector import detect_faces 

MODEL_PATH = os.path.join("models", "face_recognizer.yml")
LABELS_PATH = os.path.join("models", "labels.pickle")
ATTENDANCE_DIR = "attendance"
CONFIDENCE_THRESHOLD = 70

def load_model():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_PATH)

    with open(LABELS_PATH, "rb") as f:
        label_map = pickle.load(f)

    id_to_name = {v: k for k, v in label_map.items()}
    return recognizer, id_to_name

def get_today_file():
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(ATTENDANCE_DIR, f"{today}.csv")

def already_marked(name, file_path):
    if not os.path.exists(file_path):
        return False
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0] == name:
                return True
    return False

def mark_attendance(name):
    file_path = get_today_file()

    if already_marked(name, file_path):
        return False
    
    file_exists = os.path.exists(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Time"])
        writer.writerow([name, datetime.now().strftime("%H:%M:%S")])
    return True

def main():
    recognizer, id_to_name = load_model()
    cap = cv2.VideoCapture(0)
    print("recognition started press q to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(frame)
        for (x, y, w, h) in faces:
            face_crop = gray[y:y+h, x:x+w]
            label_id, confidence = recognizer.predict(face_crop)

            if confidence < CONFIDENCE_THRESHOLD:
                name = id_to_name.get(label_id, "Unknown")
            else:
                name = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            if name != "Unknown":
                marked = mark_attendance(name)
                if marked:
                    print(f"Attendance marked: {name}")

        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
    