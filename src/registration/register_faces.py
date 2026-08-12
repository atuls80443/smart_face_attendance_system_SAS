import cv2
import os 
from src.detection.face_detector import detect_faces

DATASET_DIR = "dataset"

def register_face(student_name):

    student_dir = os.path.join(DATASET_DIR, student_name)
    os.makedirs(student_dir, exist_ok=True)

    # cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    count = 0

    print("press s to save a image, q to quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        faces = detect_faces(frame)
        for (x, y, w, h) in faces:
            cv2. rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Register Face", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_crop = frame[y:y+h, x:x+w]
            count += 1
            file_path = os.path.join(student_dir, f"{count}.jpg")
            cv2.imwrite(file_path, face_crop)
            print(f"Saved: {file_path}")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Total images saved for {student_name}: {count}")

if __name__ == "__main__":
        name = input("Enter student name: ")
        register_face(name)