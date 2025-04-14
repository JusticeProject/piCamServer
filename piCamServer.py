from flask import Flask, Response, render_template, request, jsonify
import cv2
from datetime import datetime

###################################################################################################

# Useful links:
# https://github.com/Dhairya1007/Raspberry-Pi-AI-Home-Security-System-Part-2/blob/master/stream_security_video.py
# https://docs.opencv.org/3.4/d8/dfe/classcv_1_1VideoCapture.html#a85b55cf6a4a50451367ba96b65218ba1
# https://stackoverflow.com/questions/69870399/what-is-the-difference-between-cv2-videocapture1-and-cv2-videocapture0

app = Flask(__name__)

# Global variable to store the latest status data
latest_status = {
    "timestamp": None,
    "msg": "",
    "value1": 0,
    "value2": 0
}

###################################################################################################

def generate_frames():
    # Use 0 when no other USB camera is connected, use 1 when USB camera is connected and need to use built-in camera.
    # It seems that openCV can only handle one camera - it deadlocks when trying to access the USB camera.
    # Maybe try GStreamer to handle other cameras.
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            print("Unable to read frame.")
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            frame = buffer.tobytes()
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

###################################################################################################

@app.route("/")
def index():
    return render_template("index.html")

###################################################################################################

@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )

###################################################################################################

@app.route("/new_command", methods=['POST'])
def new_command():
    global latest_status
    data = request.json

    for key in data.keys():
        latest_status[key] = data[key]

    latest_status["msg"] = "received new command: " + str(request.json)
    
    return jsonify({"status": "success"})

###################################################################################################

@app.route("/get_status")
def get_status():
    global latest_status
    latest_status["timestamp"] = datetime.now().strftime("%d %B %Y %H:%M:%S")
    return jsonify(latest_status)

###################################################################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6515)
