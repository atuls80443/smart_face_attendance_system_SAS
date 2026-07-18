# Smart Face Attendance System (PYNQ-Z2)

AI-based face recognition attendance system that detects and recognizes student faces in real time, and automatically marks attendance — deployed and running on a **PYNQ-Z2 FPGA board**.

## Overview

The system captures live video (phone camera or laptop webcam), detects faces, recognizes registered students using a trained ML model, and logs attendance to a CSV file — with duplicate-entry prevention (one mark per student per day).

Stage 1 (current): Fixed-position camera, students walk up to register attendance. Core logic runs on the PYNQ-Z2 board, receiving a live video stream over Ethernet.

## Features

- Live camera feed input (webcam / phone IP camera)
- Real-time face detection (Haar Cascade)
- Student face registration (build your own dataset)
- Face recognition model training (LBPH algorithm)
- Automatic attendance marking to CSV (duplicate-proof)
- Runs on PYNQ-Z2 board via Ethernet-streamed camera feed

## Tech Stack

- Python, OpenCV (opencv-contrib-python)
- NumPy, Pandas
- Flask (camera streaming server)
- PYNQ-Z2 (Zynq-7000 SoC board)
- Jupyter Notebook (on-board execution)
- Git & GitHub (feature branch + PR workflow)

## Project Structure
SAS/
├── src/
│   ├── camera/          # camera streaming (local + Flask server for PYNQ)
│   ├── detection/        # face detection logic
│   ├── registration/     # face registration + model training
│   └── recognition/       # real-time recognition + attendance marking
├── models/               # trained model + cascade file
├── dataset/               # registered student face images
├── attendance/            # daily attendance CSV logs
├── pynq_notebooks/        # notebooks run directly on PYNQ-Z2
└── requirements.txt

## How to Run (Laptop Prototype)

```bash
git clone https://github.com/atuls80443/smart_face_attendance_system_SAS.git
cd smart_face_attendance_system_SAS
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 1. Register a student's face
python -m src.registration.register_faces

# 2. Train the recognition model
python -m src.registration.train_model

# 3. Run real-time recognition + attendance marking
python -m src.recognition.recognize
```

## How to Run (PYNQ-Z2 Board)

1. Connect PYNQ-Z2 to laptop via Ethernet, power via USB
2. On laptop, start the camera stream server: `python src\camera\camera_server.py`
3. Open PYNQ-Z2 Jupyter at `http://192.168.2.1:9090`
4. Upload trained model files (`models/`) to the board
5. Run `pynq_notebooks/recognize_pynq.ipynb` — it reads the laptop's live stream, recognizes faces, and marks attendance

## Development Status

In development — Stage 1 (fixed-camera prototype) complete and running on PYNQ-Z2 hardware.

## License

Developed for educational purposes.