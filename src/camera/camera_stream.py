import cv2 
from src.detection.face_detector import detect_faces 

CAMERA_SOURCE = 1

def main():
    # cap = cv2.VideoCapture(CAMERA_SOURCE)
    cap = cv2.VideoCapture(CAMERA_SOURCE, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("error: could not open camera")
        return
    
    print("camera started press q to quit")

    while True:
        ret, frame = cap.read()
        if not ret: 
            print("error: failed to grab frame")
            break

        faces = detect_faces(frame)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x +w, y + h), (0, 255, 0), 2)
        
        cv2.imshow("camera feed", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()