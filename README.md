# Smart Face Attendance System (PYNQ-Z2)

AI-based face recognition attendance system that detects and recognizes student faces in real time, and automatically marks attendance — deployed and running on a **PYNQ-Z2 FPGA board**.

## Overview

The system captures live video (laptop webcam, with phone-camera support built in), detects faces, recognizes registered students using a trained ML model, and logs attendance to a CSV file — with duplicate-entry prevention (one mark per student per day) and a short verification delay to prevent false or double detections.

Stage 1 (current): Fixed-position camera, students walk up to mark attendance. Core recognition logic runs on the PYNQ-Z2 board, which receives a live video stream from the laptop over Ethernet and sends recognition results back for live on-screen display.

## Features

- Live camera feed input (laptop webcam / phone IP camera)
- Real-time face detection (Haar Cascade)
- Only the largest detected face is processed per frame, preventing one person from being mistakenly logged as two
- Student face registration (build your own multi-student dataset)
- Face recognition model training (LBPH algorithm)
- **Verification delay** — a face must be recognized continuously for a few seconds before attendance is marked, reducing false positives
- On-screen **"Attendance Marked!"** confirmation so a student knows their attendance registered
- Automatic attendance marking to CSV (duplicate-proof, one entry per student per day)
- Runs on PYNQ-Z2 board via Ethernet-streamed camera feed
- **Live two-way display**: laptop shows a live camera window while the board performs recognition and sends results back in real time
- Personal data (face images, trained model, attendance logs) excluded from version control via `.gitignore`

## Tech Stack

- Python, OpenCV (opencv-contrib-python)
- NumPy, Pandas
- Flask (camera streaming server + result reporting endpoint)
- Threading & Requests (background, non-blocking communication between board and laptop)
- Matplotlib (on-board camera feed visualization inside Jupyter)
- PYNQ-Z2 (Zynq-7000 SoC board)
- Jupyter Notebook (on-board execution)
- Git & GitHub (feature branch + Pull Request workflow)

## Project Structure
SAS/
├── src/
│ ├── camera/ # camera streaming (local webcam, Flask server, live display)
│ ├── detection/ # face detection logic
│ ├── registration/ # face registration + model training
│ └── recognition/ # real-time recognition, verification, and attendance marking
├── models/ # trained model + cascade file (ignored by git)
├── dataset/ # registered student face images (ignored by git)
├── attendance/ # daily attendance CSV logs (ignored by git)
├── pynq_notebooks/ # notebooks run directly on PYNQ-Z2
└── requirements.txt

## How to Run (Laptop Prototype)

```bash
git clone https://github.com/atuls80443/smart_face_attendance_system_SAS.git
cd smart_face_attendance_system_SAS
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 1. Register a student's face (repeat for each student)
python -m src.registration.register_faces

# 2. Train the recognition model (run once after registering all students)
python -m src.registration.train_model

# 3. Run real-time recognition + attendance marking
python -m src.recognition.recognize
```

## How to Run (PYNQ-Z2 Board)

1. Connect PYNQ-Z2 to laptop via Ethernet, power via USB
2. On the laptop, start the live camera server: `python src\camera\live_display.py`
3. Open PYNQ-Z2 Jupyter at `http://192.168.2.1:9090`
4. Upload the trained model files (`face_recognizer.yml`, `labels.pickle`, and the cascade `.xml`) to the board's `attendance_system` folder — re-upload whenever the model is retrained
5. Open `pynq_notebooks/recognize_pynq.ipynb` and run **Kernel → Restart & Run All** — it reads the laptop's live stream, recognizes faces after a short verification delay, marks attendance, and sends results back for live display on the laptop
6. Click the ■ (interrupt) button in Jupyter to stop recognition

**Note:** The PYNQ-Z2 has no internet access or battery-backed clock, so its date can reset after a reboot. If attendance logs show the wrong date, set the correct date on the board via a Jupyter terminal: `sudo date -s "YYYY-MM-DD HH:MM:SS"`

## Development Status

Stage 1 complete: fixed-camera prototype tested with multiple registered students, running end-to-end on PYNQ-Z2 hardware with live two-way display and false-positive protection via verification delay.

## License

Developed for educational purposes.