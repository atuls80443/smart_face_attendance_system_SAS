import cv2
import os
import numpy as np
import pickle

DATASET_DIR = "dataset"
MODEL_PATH = os.path.join("models", "face_recognizer.yml")
LABELS_PATH = os.path.join("models", "labels.pickle")

def train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  

    faces = []       
    labels = []      
    label_map = {}   
    current_id = 0

    for student_name in os.listdir(DATASET_DIR):
        student_dir = os.path.join(DATASET_DIR, student_name)
        if not os.path.isdir(student_dir):
            continue

        if student_name not in label_map:
            label_map[student_name] = current_id
            current_id += 1
        label_id = label_map[student_name]


        for img_name in os.listdir(student_dir):
            img_path = os.path.join(student_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  
            if img is None:
                continue

            faces.append(img)
            labels.append(label_id)

    recognizer.train(faces, np.array(labels))

    recognizer.save(MODEL_PATH)


    with open(LABELS_PATH, "wb") as f:
        pickle.dump(label_map, f)

    print(f"Training complete. {len(faces)} images used across {len(label_map)} student(s).")
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train()