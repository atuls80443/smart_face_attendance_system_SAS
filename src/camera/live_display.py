import cv2
import threading
from flask import Flask, Response, request, jsonify

app = Flask(__name__)
camera = cv2.VideoCapture(0)  

# camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # smaller frame = faster everything downstream
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

latest_result = {"name": None, "box": None}

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        # ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 60])
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/update_result', methods=['POST'])
def update_result():
    data = request.get_json()
    latest_result["name"] = data.get("name")
    latest_result["box"] = data.get("box")
    return jsonify({"status": "ok"})

def run_server():
    app.run(host='0.0.0.0', port=5000)

threading.Thread(target=run_server, daemon=True).start()

print("Server running. Opening live window... press 'q' to quit.")

while True:
    success, frame = camera.read()
    if not success:
        break

    if latest_result["name"] and latest_result["box"]:
        x, y, w, h = latest_result["box"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, latest_result["name"], (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Live Attendance View", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()