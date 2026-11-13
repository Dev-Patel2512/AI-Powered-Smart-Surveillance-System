# AI-Powered Smart Surveillance System

### Intelligent Video Monitoring, Object Detection & Real-Time Incident Analytics

An AI-powered smart surveillance system developed using Python, OpenCV, YOLOv8, Flask, and SQLite. The system provides real-time person detection, mobile phone detection, zone occupancy monitoring, automated incident logging, snapshot capturing, and an interactive analytics dashboard.

It also includes a separate Hikvision RTSP camera-based face detection and people-counting utility.

---

## 1. Project Overview

The AI-Powered Smart Surveillance System is designed to improve traditional video surveillance through artificial intelligence and computer vision.

The system processes live camera feeds, detects objects, monitors predefined surveillance zones, and records relevant incidents automatically.

It provides a centralized dashboard to visualize incident information, monitor detection statistics, analyze historical records, and access captured snapshots.

The project consists of two main computer vision modules:

**Module 1: AI-Based Smart Surveillance System**
- Real-time person detection.
- Mobile phone detection.
- Zone occupancy monitoring.
- Incident detection and logging.
- Automatic snapshot capturing.
- SQLite database integration.
- Interactive Flask dashboard.

**Module 2: Hikvision Camera Face Detection**
- RTSP camera integration.
- Real-time face detection.
- Face bounding box visualization.
- Live face counting.
- Camera reconnection handling.

---

## 2. Project Objectives

The primary objectives of this project are:

1. To develop an AI-based video surveillance solution.
2. To implement real-time object detection using YOLOv8.
3. To detect people and mobile phones from camera feeds.
4. To monitor occupancy within a predefined region.
5. To identify and record relevant surveillance incidents.
6. To capture snapshots for incident documentation.
7. To maintain structured incident records using SQLite.
8. To develop an interactive web-based monitoring dashboard.
9. To visualize surveillance data through charts and analytics.
10. To integrate IP cameras through RTSP streaming.

---

## 3. Key Features

### 3.1 Real-Time Object Detection
- Uses the YOLOv8 object detection model.
- Detects people and mobile phones.
- Processes live camera frames.
- Displays detection bounding boxes.
- Uses configurable confidence thresholds.

### 3.2 Zone Occupancy Monitoring
- Supports a configurable Region of Interest (ROI).
- Monitors people inside the predefined zone.
- Compares occupancy against a configured capacity limit.
- Helps identify occupancy-related incidents.

### 3.3 Mobile Phone Detection
- Detects mobile phones using the object detection model.
- Evaluates phone detection in relation to people.
- Supports configurable confirmation timing.
- Uses cooldown settings to reduce repeated alerts.

### 3.4 Automated Incident Logging
- Records detected incidents.
- Stores incident information in SQLite.
- Maintains CSV-based incident records.
- Captures incident snapshots.
- Supports historical incident analysis.

### 3.5 Interactive Analytics Dashboard
- Provides a web-based monitoring interface.
- Displays incident statistics.
- Shows incident timelines.
- Visualizes confidence distributions.
- Displays peak incident hours.
- Provides daily incident summaries.
- Supports incident filtering and pagination.
- Displays captured snapshots.

### 3.6 Hikvision Camera Integration
- Supports RTSP camera streaming.
- Uses OpenCV DNN for face detection.
- Displays face detection bounding boxes.
- Provides live face counting.
- Includes camera reconnection handling.

---

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| YOLOv8 | Object detection |
| OpenCV | Image and video processing |
| OpenCV DNN | Face detection |
| Flask | Web application backend |
| SQLite | Incident database |
| CSV | Incident record export |
| HTML5 | Dashboard structure |
| CSS3 | Dashboard styling |
| JavaScript | Dashboard interactions |
| Bootstrap | Responsive interface |
| Chart.js | Data visualization |
| RTSP | IP camera streaming |

---

## 5. System Architecture

The project follows a modular architecture consisting of camera input, detection processing, incident management, database storage, and dashboard visualization.

### Main Surveillance Workflow

1. Camera Input
2. Video Frame Acquisition
3. Image Processing Using OpenCV
4. YOLOv8 Object Detection
5. Person and Mobile Phone Detection
6. Region of Interest Monitoring
7. Incident Condition Evaluation
8. Incident Logging
9. Snapshot Capturing
10. SQLite and CSV Storage
11. Flask Dashboard
12. Analytics and Visualization

### Architecture Diagram

```text
             CAMERA INPUT
                   |
                   v
          VIDEO FRAME CAPTURE
                   |
                   v
             OPENCV PROCESSING
                   |
                   v
             YOLOv8 MODEL
                   |
                   v
          OBJECT DETECTION
                   |
          +--------+--------+
          |                 |
          v                 v
     PERSON DETECTION   PHONE DETECTION
          |                 |
          +--------+--------+
                   |
                   v
          ZONE MONITORING
                   |
                   v
          INCIDENT EVALUATION
                   |
                   v
          INCIDENT MANAGEMENT
                   |
          +--------+--------+
          |                 |
          v                 v
       SQLITE             CSV
          |                 |
          +--------+--------+
                   |
                   v
            FLASK DASHBOARD
                   |
                   v
          ANALYTICS & REPORTS
```

---

## 6. Project Folder Structure

```text
AI-Powered-Smart-Surveillance-System/
│
├── main.py
│   └── Main AI detection application
│
├── dashboard.py
│   └── Flask dashboard backend
│
├── dashboard.html
│   └── Dashboard frontend interface
│
├── cam.py
│   └── Hikvision RTSP face detection utility
│
├── setup_dirs.py
│   └── Creates required project directories
│
├── validate_setup.py
│   └── Validates project setup
│
├── test_server.py
│   └── Snapshot serving test server
│
├── requirements.txt
│   └── Python dependencies
│
├── yolov8n.pt
│   └── YOLOv8 model weights
│
├── deploy.prototxt
│   └── OpenCV DNN model configuration
│
├── res10_300x300_ssd_iter_140000.caffemodel
│   └── Face detection model weights
│
├── START.bat
│   └── Windows startup script
│
├── START.ps1
│   └── PowerShell startup script
│
├── detection_incidents.db
│   └── SQLite incident database (runtime)
│
├── incident_log.csv
│   └── Incident records (runtime)
│
├── phone_incidents/
│   └── Captured incident snapshots
│
└── README.md
    └── Project documentation
```

---

## 7. System Requirements

### Hardware Requirements

- Computer or laptop.
- Webcam or compatible IP camera.
- Minimum 8 GB RAM recommended.
- Multi-core processor.
- Sufficient storage for snapshots and incident records.

### Software Requirements

- Python 3.8 or later, subject to dependency compatibility.
- Windows, Linux, or compatible operating system.
- OpenCV.
- Ultralytics YOLOv8.
- Flask.
- SQLite.
- Required Python dependencies.

---

## 8. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Powered-Smart-Surveillance-System.git
```

### Step 2: Navigate to the Project

```bash
cd AI-Powered-Smart-Surveillance-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

For PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

For Linux:

```bash
source .venv/bin/activate
```

### Step 5: Install Dependencies

```bash
python -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

If NumPy is not included in the installed dependencies:

```bash
pip install numpy
```

### Step 6: Validate the Installation

```bash
python validate_setup.py
```

---

## 9. Configuration

The application provides configurable parameters for camera input, object detection, occupancy monitoring, and incident handling.

### Main Application Configuration

The following settings are defined in `main.py`:

| Parameter | Description |
|---|---|
| MAX_CAPACITY | Maximum occupancy limit |
| CAMERA_INDEX | Camera device index |
| ROI_X1 | ROI top-left X coordinate |
| ROI_Y1 | ROI top-left Y coordinate |
| ROI_X2 | ROI bottom-right X coordinate |
| ROI_Y2 | ROI bottom-right Y coordinate |
| PERSON_CONF | Person detection confidence |
| PHONE_CONF | Phone detection confidence |
| PHONE_CONFIRM_SECONDS | Phone confirmation duration |
| ALERT_COOLDOWN | Alert cooldown duration |
| PHOTO_COOLDOWN | Snapshot cooldown duration |
| SNAPSHOT_FOLDER | Snapshot storage directory |

Modify these values according to the camera resolution and surveillance requirements.

### Dashboard Configuration

The dashboard uses the following default resources:

- Database: `detection_incidents.db`
- Snapshot directory: `phone_incidents`
- Default port: `5000`

### RTSP Camera Configuration

The Hikvision camera utility uses RTSP streaming.

Configure the following according to your camera:

- Camera IP address.
- RTSP stream path.
- Username and password.
- Detection confidence.
- Camera reconnection settings.

Never publish actual camera credentials or private network details.

---

## 10. How to Run the Project

### A. Run the Main AI Detection Application

Open the terminal and execute:

```bash
python main.py
```

The application starts the configured camera and performs real-time object detection and monitoring.

### B. Start the Dashboard

Open a second terminal.

Activate the same virtual environment and execute:

```bash
python dashboard.py
```

### C. Open the Dashboard

Open your browser and navigate to:

```text
http://127.0.0.1:5000
```

The dashboard displays available incident records and analytics.

**Important:** Keep the main detection application and dashboard running separately.

### D. Run the Hikvision Face Detection Utility

Configure the RTSP connection in `cam.py` and execute:

```bash
python cam.py
```

This utility runs independently of the main YOLOv8 application.

---

## 11. Dashboard Modules

The Flask dashboard provides a centralized interface for monitoring incident information.

### 11.1 Overview Statistics
Displays overall incident statistics and monitoring information.

### 11.2 Incident Timeline
Visualizes incidents across different time periods.

### 11.3 Confidence Distribution
Displays the distribution of recorded detection confidence scores.

### 11.4 Peak Hours Analysis
Shows incident activity according to the recorded hour.

### 11.5 Daily Summary
Provides daily incident statistics.

### 11.6 Incident Management
Provides access to recorded incidents with filtering and pagination.

### 11.7 Snapshot Viewer
Allows users to view saved incident images.

### 11.8 System Health
Displays available application and monitoring status information.

---

## 12. API Endpoints

The Flask application provides the following endpoints:

| Endpoint | Description |
|---|---|
| `/` | Main dashboard page |
| `/api/stats` | Overall incident statistics |
| `/api/incidents` | Incident records and pagination |
| `/api/timeline` | Incident timeline data |
| `/api/confidence-distribution` | Confidence distribution |
| `/api/peak-hours` | Peak incident hours |
| `/api/daily-summary` | Daily incident statistics |
| `/api/system-health` | System health information |
| `/api/snapshot/<filename>` | Retrieves an incident snapshot |

Refer to `dashboard.py` for the exact request parameters and response structures.

---

## 13. Database Management

The project uses SQLite for structured incident storage.

### Database File

```text
detection_incidents.db
```

### CSV File

```text
incident_log.csv
```

### Snapshot Directory

```text
phone_incidents/
```

These resources are used for storing and accessing incident-related information.

The dashboard reads the recorded incident data to generate statistics, charts, and historical reports.

---

## 14. Testing and Validation

The project includes setup validation and a small server testing utility.

### Validate Project Setup

```bash
python validate_setup.py
```

### Run the Test Server

```bash
python test_server.py
```

### Recommended Manual Testing

1. Verify camera connectivity.
2. Check person detection.
3. Check mobile phone detection.
4. Verify occupancy monitoring.
5. Verify incident generation.
6. Check snapshot capturing.
7. Verify CSV incident records.
8. Verify SQLite database updates.
9. Start the Flask dashboard.
10. Verify dashboard statistics and charts.
11. Test incident filtering.
12. Verify snapshot accessibility.

---

## 15. Troubleshooting

| Issue | Possible Solution |
|---|---|
| Camera not detected | Verify camera index and permissions |
| RTSP connection failed | Verify IP address, stream URL, and credentials |
| Model file missing | Check model file location |
| Python package missing | Install dependencies |
| Dashboard not opening | Check Flask server and port |
| No incidents displayed | Verify detection process and database path |
| Snapshots unavailable | Verify snapshot directory |
| Incorrect detections | Adjust confidence thresholds and camera positioning |

---

## 16. Privacy and Security

This project processes camera feeds and may store surveillance snapshots.

The following practices are recommended:

- Obtain appropriate permission before monitoring.
- Follow applicable privacy and surveillance regulations.
- Secure camera credentials.
- Restrict access to incident records.
- Protect stored snapshots.
- Avoid publishing sensitive information.
- Implement authentication before exposing the dashboard remotely.
- Use HTTPS for secure remote access.
- Establish appropriate data retention policies.
- Review automated detections through human oversight.

---

## 17. Future Enhancements

Potential future improvements include:

1. Multi-camera monitoring.
2. Advanced face recognition with appropriate safeguards.
3. Real-time email notifications.
4. WhatsApp alert integration.
5. Cloud-based incident storage.
6. Advanced analytics and reporting.
7. Role-based dashboard authentication.
8. Real-time remote monitoring.
9. Automated incident report generation.
10. Improved model accuracy and performance evaluation.

---

## 18. Project Applications

The system can be adapted for:

- Smart office surveillance.
- Workplace monitoring.
- Restricted-zone monitoring.
- Occupancy management.
- Security monitoring.
- Industrial monitoring.
- IP camera surveillance.
- Research and computer vision applications.

These are potential application areas, not claims of certified or production-ready deployment.

---

## 19. Limitations

- Detection performance depends on camera quality and environmental conditions.
- Poor lighting and camera angles can affect detection accuracy.
- False positives and false negatives may occur.
- Processing performance depends on available hardware.
- RTSP streaming depends on network connectivity.
- The two detection modules operate independently.
- Production deployment requires additional security and access controls.

---

## 20. License

No license has been specified for this project.

A suitable open-source license can be added after confirming ownership and redistribution permissions for the source code and included model assets.

---

## 21. Acknowledgements

This project uses the following open-source technologies:

- Ultralytics YOLOv8
- OpenCV
- Flask
- SQLite
- Bootstrap
- Chart.js
- Python

Special thanks to the developers and communities behind these technologies.

---

## 22. Author

**Developed as an AI and Computer Vision Project.**

**Project Name:** AI-Powered Smart Surveillance System

**Domain:** Artificial Intelligence | Machine Learning | Computer Vision | Deep Learning

**Primary Language:** Python

**Repository:** AI-Powered-Smart-Surveillance-System

---

### Conclusion

The AI-Powered Smart Surveillance System demonstrates the integration of computer vision, deep learning, real-time video processing, database management, and web-based analytics.

By combining YOLOv8 object detection, OpenCV image processing, Flask dashboard development, and SQLite storage, the project provides a modular foundation for intelligent video surveillance and incident monitoring.

**AI-Powered Smart Surveillance — Intelligent Detection, Monitoring, and Analytics.**
