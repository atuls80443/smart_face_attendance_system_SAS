import cv2
import os
import pickle
import csv
import time
from datetime import datetime
from src.detection.face_detector import detect_faces

MODEL_PATH = os.path.join("models", "face_recognizer.yml")
LABELS_PATH = os.path.join("models", "labels.pickle")
ATTENDANCE_DIR = "attendance"
CONFIDENCE_THRESHOLD = 55       # lower = stricter match
VERIFY_SECONDS = 3              # face must be seen continuously this long before marking

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
    cap = cv2.VideoCapture(1)

    # tracks which face we're currently verifying, and since when
    candidate_name = None
    candidate_since = None

    print("Recognition started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detect_faces(frame)

        if len(faces) > 0:
            faces = [max(faces, key=lambda f: f[2] * f[3])]
        else:
            candidate_name = None
            candidate_since = None

        for (x, y, w, h) in faces:
            face_crop = gray[y:y+h, x:x+w]
            face_crop = cv2.equalizeHist(face_crop) # match the lighting normalization used during training
            label_id, confidence = recognizer.predict(face_crop)

            if confidence < CONFIDENCE_THRESHOLD:
                name = id_to_name.get(label_id, "Unknown")
            else:
                name = "Unknown"

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if name == "Unknown":
                candidate_name = None
                candidate_since = None
                cv2.putText(frame, "Unknown", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                continue

            # new/different face detected -> restart the verification timer
            if name != candidate_name:
                candidate_name = name
                candidate_since = time.time()

            elapsed = time.time() - candidate_since

            if elapsed >= VERIFY_SECONDS:
                # seen continuously long enough -> safe to mark
                cv2.putText(frame, f"{name} - Verified", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                marked = mark_attendance(name)
                if marked:
                    print(f"Attendance marked: {name}")
            else:
                # still counting down, show progress on screen
                # remaining = VERIFY_SECONDS - elapsed
                # cv2.putText(frame, f"Verifying {name}... {remaining:.1f}s", (x, y - 10),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 165, 255), 2)
                pass

        cv2.imshow("Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()