import cv2 

CAMERA_SOURCE = 0

def main():
    cap = cv2.VideoCapture(CAMERA_SOURCE)

    if not cap.isOpened():
        print("error: could not open camera")
        return
    
    print("camera started press q to quit")

    while True:
        ret, frame = cap.read()
        if not ret: 
            print("error: failed to grab frame")
            break
        
        cv2.imshow("camera feed", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break 

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()