# Smart Face Attendance System (PYNQ-Z2)

AI-based face recognition attendance system that detects and recognizes student faces in real time, and automatically marks attendance — deployed and running on a **PYNQ-Z2 FPGA board**, with hardware LED feedback on the board itself.

## Overview

The system captures live video (4K USB camera, with laptop webcam as fallback), detects faces, recognizes registered students using a trained ML model, and logs attendance to a CSV file — with duplicate-entry prevention (one mark per student per day) and a short silent verification delay to prevent false or double detections.

Fixed-position camera, students walk up to mark attendance. Core recognition logic runs on the PYNQ-Z2 board, which receives a live video stream from the laptop over Ethernet, recognizes faces, sends results back for live on-screen display, and blinks its onboard LEDs to physically confirm a mark — directly on the hardware, not just on screen.

## Features

- Live camera feed input (4K USB camera / laptop webcam)
- Real-time face detection (Haar Cascade)
- Only the largest detected face is processed per frame, preventing one person from being mistakenly logged as two
- **Lighting-robust recognition** — histogram equalization applied during registration, training, and recognition; dataset includes images captured across multiple real lighting conditions (e.g. home and academy) under the same student identity
- **Fixed-size face crops (200x200)** — every face image is resized consistently across registration, training, and recognition for reliable matching regardless of camera or frame size
- Student face registration (build your own multi-student dataset)
- Face recognition model training (LBPH algorithm)
- **Silent verification delay** — a face must be recognized continuously for ~1.5 seconds before attendance is marked.
- On-screen **"[Name] - Attendance Marked!"** confirmation, held on screen as long as the student remains in frame
- **Onboard LED blink** on the PYNQ-Z2 itself when attendance is marked, giving a hardware-level confirmation independent of the screen
- Automatic attendance marking to CSV (duplicate-proof, one entry per student per day)
- Runs on PYNQ-Z2 board via Ethernet-streamed camera feed
- **Live two-way display**: laptop shows a live camera window while the board performs recognition and sends results back in real time
- **Background frame-reader thread on the board** — always processes the most recent frame and discards any backlog, preventing stale/delayed recognition results
- Personal data (face images, trained model, attendance logs) excluded from version control via `.gitignore`

## Tech Stack

- Python, OpenCV (opencv-contrib-python)
- NumPy, Pandas
- Flask (camera streaming server + result reporting endpoint)
- Threading & Requests (background, non-blocking communication between board and laptop)
- PYNQ (`BaseOverlay`) — onboard LED control via the board's FPGA base overlay
- PYNQ-Z2 (Zynq-7020 SoC board — dual-core ARM Cortex-A9 processor + FPGA fabric)
- Jupyter Notebook (on-board execution)
- Git & GitHub (feature branch + Pull Request workflow)

## Project Structure
SAS/
├── src/
│ ├── camera/ # camera streaming (local webcam/4K USB camera, Flask server, live display)
│ ├── detection/ # face detection logic
│ ├── registration/ # face registration + model training
│ └── recognition/ # real-time recognition, verification, and attendance marking
├── models/ # trained model + cascade file (ignored by git)
├── dataset/ # registered student face images, multi-lighting (ignored by git)
├── attendance/ # daily attendance CSV logs (ignored by git)
├── pynq_notebooks/ # notebooks run directly on PYNQ-Z2, including LED control
└── requirements.txt

## How to Run (Laptop Prototype)

```bash
git clone https://github.com/atuls80443/smart_face_attendance_system_SAS.git
cd smart_face_attendance_system_SAS
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 1. Register a student's face (repeat for each student, ideally in multiple lighting conditions)
python -m src.registration.register_faces

# 2. Train the recognition model (run once after registering/updating all students)
python -m src.registration.train_model

# 3. Run real-time recognition + attendance marking
python -m src.recognition.recognize
```

**Note:** Camera index depends on your setup — verify with a quick test script if switching cameras or USB ports, since Windows' DirectShow backend can order cameras differently than expected.

## How to Run (PYNQ-Z2 Board)

1. Connect PYNQ-Z2 to laptop via Ethernet, power via USB
2. On the laptop, start the live camera server: `python src\camera\live_display.py`
3. Open PYNQ-Z2 Jupyter at `http://192.168.2.1:9090`
4. Upload the trained model files (`face_recognizer.yml`, `labels.pickle`, and the cascade `.xml`) to the board's `attendance_system` folder — re-upload whenever the model is retrained
5. Open `pynq_notebooks/recognize_pynq.ipynb` and run **Kernel → Restart & Run All** — it loads the LED overlay, connects a background thread to always read the latest camera frame, recognizes faces after a short silent verification delay, marks attendance, blinks the onboard LEDs, and sends results back for live display on the laptop
6. Click the ■ (interrupt) button in Jupyter to stop recognition

**Note:** The PYNQ-Z2 has no internet access or battery-backed clock, so its date can reset after a reboot. If attendance logs show the wrong date, set the correct date on the board via a Jupyter terminal: `sudo date -s "YYYY-MM-DD HH:MM:SS"`

## License

Developed for educational purposes.