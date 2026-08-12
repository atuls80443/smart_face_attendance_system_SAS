import cv2
import time

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# what the camera driver reports it's set to
print("Reported FPS:", cap.get(cv2.CAP_PROP_FPS))

# measure actual frames captured in 5 seconds
frame_count = 0
start = time.time()

while time.time() - start < 5:
    ret, frame = cap.read()
    if ret:
        frame_count += 1

elapsed = time.time() - start
print(f"Actual frames captured: {frame_count} in {elapsed:.1f} sec")
print(f"Actual FPS: {frame_count / elapsed:.1f}")

cap.release()