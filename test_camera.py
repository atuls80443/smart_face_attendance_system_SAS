# import cv2

# # request 4K resolution explicitly on indexes 0 and 1
# for i in range(2):
#     cap = cv2.VideoCapture(i)
#     if cap.isOpened():
#         cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
#         cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
#         ret, frame = cap.read()
#         if ret:
#             print(f"Index {i}: resolution = {frame.shape[1]}x{frame.shape[0]}")
#         cap.release()

import cv2

# test using DirectShow backend specifically, same as the project files use
for i in range(4):
    cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
        ret, frame = cap.read()
        if ret:
            print(f"Index {i}: resolution = {frame.shape[1]}x{frame.shape[0]}")
        cap.release()
    else:
        print(f"Index {i}: Not available")