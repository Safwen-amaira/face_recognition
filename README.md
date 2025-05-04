# Face Recognition Web App with Flask

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9.0-orange)](https://opencv.org/)

A real-time face recognition web application built with Flask and OpenCV. Register users through the web interface and recognize them using your webcam.

## Features

- 📷 Real-time face detection and recognition
- 👤 User registration with multiple face samples
- 💾 Local storage of face encodings
- 🌐 Web-based interface
- 🎯 Multi-sample registration for improved accuracy

## Installation

### Prerequisites
- Python 3.8+
- Webcam

1. **Clone the repository**

```bash
git clone https://github.com/Safwen-amaira/face-recognition.git
cd face-recognition
```
2. **Create and activate virtual environment**

```bash

python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies** 


```bash
pip install -r requirements.txt
```

## Using The application

1. **run the server**
```bash
python app.py
```
2. **Access the web interface**

http://localhost:5000

3. **Register new users** 

    - Navigate to /register

    - Enter username and follow on-screen instructions

    - Position face clearly in webcam view
 
    - the system will capture 10 face samples

4. **Recignize faces**

    - Go to /recognize

    - View real-time recognition results

    - Recognized names will appear over detected faces

## Project Structure

```bash

├── app.py              # Main application entry point
├── requirements.txt    # Project dependencies
├── faces.db            # Face encodings database
├── templates/          # HTML templates
│   ├── index.html      # Home page
│   ├── register.html   # Registration page
│   ├── recognize.html  # Recognition page
│   └── register_waiting.html # Registration status
└── static/             # Static assets (CSS/JS/images)

``` 

## Technical Stack 

    - Backend: Flask

    - Face Recognition: face-recognition library

    - Computer Vision: OpenCV

    - Data Storage: Pickle

    - Web Interface: HTML5, CSS3

## Note 
    This project serves as a proof-of-concept to demonstrate my ability to implement an intelligent agent within a short timeframe. While the current version is a basic implementation without any IA code assistant, it still requires further refinement and enhancements. The goal is to explore how this concept can be effectively applied in real-world scenarios and develop it into a more robust solution.


## Troubleshooting


    - Webcam not detected: Ensure no other applications are using the camera

    - Installation issues: Verify Python version and virtual environment activation

    - Recognition errors: Ensure proper lighting and front-facing position during registration

