from flask import Flask, render_template, Response, request, jsonify
import cv2
import face_recognition
import numpy as np
import pickle
import os

app = Flask(__name__)
REGISTER_MODE = False
CURRENT_USER = ""
FACE_SAMPLES = []
if os.path.exists('faces.db'):
    with open('faces.db', 'rb') as f:
        KNOWN_FACES = pickle.load(f)
else:
    KNOWN_FACES = {}
def gen_frames():
    global REGISTER_MODE, CURRENT_USER, FACE_SAMPLES, KNOWN_FACES
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)  
    while True:
        success, frame = camera.read()
        if not success:
            break
        if REGISTER_MODE:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            if face_locations:
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, f"Capturing {len(FACE_SAMPLES)+1}/10",
                            (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                encoding = face_recognition.face_encodings(rgb_frame, [face_locations[0]])[0]
                FACE_SAMPLES.append(encoding)
                if len(FACE_SAMPLES) >= 10:
                    KNOWN_FACES[CURRENT_USER] = FACE_SAMPLES
                    with open('faces.db', 'wb') as f:
                        pickle.dump(KNOWN_FACES, f)
                    REGISTER_MODE = False
                    CURRENT_USER = ""
                    FACE_SAMPLES = []
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()
def recognize_frames():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        success, frame = camera.read()
        if not success:
            break
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            confidence = 0
            min_distance = float('inf')
            matched_name = None
            for known_name, encodings in KNOWN_FACES.items():
                distances = face_recognition.face_distance(encodings, face_encoding)
                if len(distances) == 0:
                    continue
                current_min = np.min(distances)
                if current_min < min_distance:
                    min_distance = current_min
                    matched_name = known_name
            if min_distance < 0.45:
                name = matched_name
                confidence = int((1 - min_distance) * 100)
            else:
                name = "Unknown"
                confidence = 0
            label = f"{name} ({confidence}%)"
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/recognize_feed')
def recognize_feed():
    return Response(recognize_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/register', methods=['GET', 'POST'])
def register():
    global REGISTER_MODE, CURRENT_USER, FACE_SAMPLES
    if request.method == 'POST':
        CURRENT_USER = request.form['username']
        REGISTER_MODE = True
        FACE_SAMPLES = []
    return render_template('register.html')
@app.route('/registration_status')
def registration_status():
    return jsonify({'status': 'complete' if not REGISTER_MODE else 'processing'})
@app.route('/recognize')
def recognize():
    return render_template('recognize.html')
if __name__ == '__main__':
    app.run(debug=True)
