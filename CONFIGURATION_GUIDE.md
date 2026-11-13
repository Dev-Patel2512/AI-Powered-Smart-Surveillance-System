# ⚙️ Configuration Reference Guide

Complete reference for all configurable settings in the Face Detection system.

## 📝 Detection System Configuration (main.py)

### Zone & Capacity Settings

```python
MAX_CAPACITY = 2
```
**Purpose**: Maximum allowed people in the ROI zone  
**Range**: 1-100  
**Effect**: Alert triggered when count exceeds this  
**Example**:
- `MAX_CAPACITY = 1` - Single occupancy mode
- `MAX_CAPACITY = 5` - Small group mode

### Camera Configuration

```python
CAMERA_INDEX = 0
```
**Purpose**: Which camera to use if multiple connected  
**Range**: 0, 1, 2, ... (depends on system)  
**Common values**:
- `0` - Default/built-in webcam
- `1` - External USB camera
- `2` - Second external camera  

**How to find your camera index**:
```python
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Camera {i} available")
```

### ROI Zone Configuration

```python
ROI_X1, ROI_Y1 = 150, 100   # Top-left corner
ROI_X2, ROI_Y2 = 500, 400   # Bottom-right corner
```
**Purpose**: Define the monitored zone  
**Units**: Pixels (0,0 = top-left)  
**Effect**: Only detections within this box trigger alerts  

**How to set coordinates**:
1. Run main.py
2. Note pixel coordinates you want to monitor
3. Update ROI_X1, ROI_Y1 (top-left)
4. Update ROI_X2, ROI_Y2 (bottom-right)
5. Restart main.py

**Visual Guide**:
```
    (0,0) ─────────────→ X
     │
     │   ROI_X1, ROI_Y1
     │    ┌────────────┐
     │    │   ZONE     │
     │    │   (active) │
     │    └────────────┘
     │  ROI_X2, ROI_Y2
     ↓
     Y
```

### Detection Confidence Thresholds

```python
PERSON_CONF = 0.40
PHONE_CONF = 0.35
```

**Range**: 0.0 - 1.0 (where 1.0 = 100% confidence)

**Person Detection**:
- `0.40` - **DEFAULT** (balanced)
- `0.30` - More sensitive (catches more people)
- `0.50` - More strict (fewer false positives)
- `0.70` - Very strict (only clear detections)

**Phone Detection**:
- `0.35` - **DEFAULT** (more sensitive)
- `0.25` - Catch all phones (many false positives)
- `0.50` - Conservative (fewer false positives)
- `0.70` - Very strict

**Effect of lowering threshold**:
- More detections (higher sensitivity)
- More false positives possible
- More alerts

**Effect of raising threshold**:
- Fewer detections (lower sensitivity)
- More false negatives possible
- Fewer false alarms

### Alert Configuration

```python
ALERT_COOLDOWN = 1.5        # Seconds between sound alerts
PHOTO_COOLDOWN = 7.0        # Seconds between captures
```

**ALERT_COOLDOWN**:
- Prevents alert spam
- Range: 0.5 - 10 seconds
- `1.5` - **DEFAULT** (good balance)
- `0.5` - Alert every detection
- `10.0` - One alert per 10 seconds max

**PHOTO_COOLDOWN**:
- Prevents duplicate snapshot saves
- Range: 1 - 60 seconds
- `7.0` - **DEFAULT** (good balance)
- `1.0` - Capture every incident
- `30.0` - Only 2 captures per minute

### File & Folder Configuration

```python
SNAPSHOT_FOLDER = "phone_incidents"
LOG_FILE = "incident_log.csv"
DB_FILE = "detection_incidents.db"
FLASH_DURATION = 2.5
```

**SNAPSHOT_FOLDER**: Where phone detection images are saved  
**LOG_FILE**: CSV file with incident records  
**DB_FILE**: SQLite database file  
**FLASH_DURATION**: How long "SNAPSHOT SAVED!" shows on screen (seconds)

### Color Configuration (BGR format)

```python
C_GREEN  = (0,   200,   0)     # Zone normal
C_RED    = (0,   0,   220)     # Critical alert
C_ORANGE = (0,   140, 255)     # Phone detected
C_WHITE  = (255, 255, 255)     # Text
C_YELLOW = (0,   255, 255)     # Status
C_PHONE  = (0,   100, 255)     # Phone box
C_DARK   = (20,  20,  20)      # Background
C_CYAN   = (255, 220,   0)     # Flash message
```

**Note**: OpenCV uses BGR (Blue, Green, Red), not RGB!

---

## 🌐 Dashboard Configuration (dashboard.py)

### Server Settings

```python
DB_FILE = "detection_incidents.db"
SNAPSHOT_FOLDER = "phone_incidents"
```

**DB_FILE**: Must match the file used by main.py  
**SNAPSHOT_FOLDER**: Must match folder used by main.py

### Flask Server Configuration

```python
app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
```

**debug**: Set to `False` for production  
**host**: 
- `'127.0.0.1'` - Local only
- `'0.0.0.0'` - Network accessible
- `'localhost'` - Local only (same as 127.0.0.1)

**port**: HTTP port number  
- `5000` - **DEFAULT**
- `8000` - Alternative
- `3000` - Alternative

**threaded**: Allow multiple simultaneous requests

### Changing Port Example

To use port 5001 instead:
```python
# Change this line at the bottom:
app.run(debug=False, host='0.0.0.0', port=5001, threaded=True)

# Then access: http://localhost:5001
```

---

## 📊 Dashboard Display Configuration

### Auto-Refresh Interval

In `dashboard.html`, search for:
```javascript
// Auto-refresh every 30 seconds
setInterval(() => {
    loadStats();
    loadIncidents();
    loadSystemHealth();
}, 30000);  // 30000 milliseconds = 30 seconds
```

**To change to 60 seconds**:
```javascript
}, 60000);  // 60 seconds
```

### Chart Update Rate

Charts update when:
- Dashboard loads
- Refresh button clicked
- Stats update (every 30 seconds)
- Incident filter changes

### Incidents Per Page

In `dashboard.py`, find:
```python
per_page = 20
```

**Change to show different number per page**:
```python
per_page = 50  # Show 50 incidents per page
```

---

## 🗄️ Database Configuration

### SQLite Database Tuning

The database is created in main.py. To optimize for your use case:

**For many queries (default)**:
```python
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
```

**For high-performance (add synchronous mode)**:
```python
conn.execute("PRAGMA synchronous = OFF")  # Faster writes
```

**For reliability (add journaling)**:
```python
conn.execute("PRAGMA journal_mode = WAL")  # Better concurrency
```

---

## 📋 Preset Configurations

### Configuration Presets

**High Sensitivity Mode** (catch everything)
```python
MAX_CAPACITY = 1
PERSON_CONF = 0.25
PHONE_CONF = 0.20
ALERT_COOLDOWN = 0.5
PHOTO_COOLDOWN = 2.0
```

**Balanced Mode** (default - recommended)
```python
MAX_CAPACITY = 2
PERSON_CONF = 0.40
PHONE_CONF = 0.35
ALERT_COOLDOWN = 1.5
PHOTO_COOLDOWN = 7.0
```

**Conservative Mode** (high threshold)
```python
MAX_CAPACITY = 5
PERSON_CONF = 0.60
PHONE_CONF = 0.55
ALERT_COOLDOWN = 3.0
PHOTO_COOLDOWN = 15.0
```

**Single Person Strict Mode**
```python
MAX_CAPACITY = 1
PERSON_CONF = 0.70
PHONE_CONF = 0.60
ALERT_COOLDOWN = 1.0
PHOTO_COOLDOWN = 5.0
```

---

## 🔄 Adjusting at Runtime

### Without Restarting

You can't change detection parameters without restarting main.py.

**However**, you can:
- Change dashboard filters (no restart needed)
- Change dashboard auto-refresh interval (edit HTML)
- Change dashboard port (restart dashboard only)

### With Restart

Edit main.py, then:
```bash
# Stop current detection (press Q)
# Edit configuration
python main.py
# Dashboard auto-reconnects
```

---

## 📐 Common Configuration Scenarios

### Scenario 1: Narrow Corridor Monitoring

```python
MAX_CAPACITY = 2
PERSON_CONF = 0.45
PHONE_CONF = 0.40
ROI_X1, ROI_Y1 = 200, 50      # Narrow, vertical zone
ROI_X2, ROI_Y2 = 440, 470
```

### Scenario 2: Large Parking Lot

```python
MAX_CAPACITY = 50
PERSON_CONF = 0.50             # Higher threshold for distance
PHONE_CONF = 0.45
ROI_X1, ROI_Y1 = 0, 0          # Full screen coverage
ROI_X2, ROI_Y2 = 1920, 1080
```

### Scenario 3: Private Office

```python
MAX_CAPACITY = 3
PERSON_CONF = 0.35             # Sensitive for small space
PHONE_CONF = 0.30              # Catch all phones
ALERT_COOLDOWN = 2.0           # Fewer alerts
PHOTO_COOLDOWN = 5.0           # More captures
```

### Scenario 4: High-Security Entrance

```python
MAX_CAPACITY = 1
PERSON_CONF = 0.60             # Very strict person detection
PHONE_CONF = 0.50              # Strict phone detection
ALERT_COOLDOWN = 1.0           # Alert on every violation
PHOTO_COOLDOWN = 2.0           # Capture frequently
```

---

## ✅ Configuration Validation

Run after changing config:

```bash
python validate_setup.py
```

This checks:
- Python version
- All required files
- All dependencies installed
- Database integrity
- Config file format

---

## 🔍 Performance Tuning

### To Improve Speed

```python
PERSON_CONF = 0.50             # Higher threshold = faster
PHONE_CONF = 0.50              # Fewer detections = faster
# Smaller ROI zone = faster
ROI_X1, ROI_Y1 = 300, 200
ROI_X2, ROI_Y2 = 600, 400
```

### To Improve Accuracy

```python
PERSON_CONF = 0.30             # Lower threshold = more checks
PHONE_CONF = 0.25              # Catch all phones
# Larger ROI zone = more coverage
ROI_X1, ROI_Y1 = 0, 0
ROI_X2, ROI_Y2 = 1280, 720
```

---

## 🆘 Configuration Troubleshooting

**"Too many false alerts"**
→ Increase thresholds: PERSON_CONF=0.50, PHONE_CONF=0.45

**"Missing real detections"**
→ Decrease thresholds: PERSON_CONF=0.30, PHONE_CONF=0.25

**"Wrong zone being monitored"**
→ Adjust ROI coordinates

**"Dashboard won't load"**
→ Check port not in use, change if needed

**"System too slow"**
→ Increase confidence thresholds

**"Snapshots folder full"**
→ Increase PHOTO_COOLDOWN to save fewer

---

## 📖 Reference Table

| Setting | Range | Default | Effect |
|---------|-------|---------|--------|
| MAX_CAPACITY | 1-100 | 2 | Alert threshold |
| PERSON_CONF | 0-1 | 0.40 | Detection sensitivity |
| PHONE_CONF | 0-1 | 0.35 | Phone detection sensitivity |
| CAMERA_INDEX | 0+ | 0 | Which camera to use |
| ALERT_COOLDOWN | 0.5-10 | 1.5 | Seconds between alerts |
| PHOTO_COOLDOWN | 1-60 | 7.0 | Seconds between captures |
| FLASH_DURATION | 1-5 | 2.5 | Message display time |
| Dashboard PORT | 1024-65535 | 5000 | HTTP port |
| Auto-refresh | 5000+ ms | 30000 | Update interval |
| Incidents/page | 1-100 | 20 | Dashboard pagination |

---

## 💾 Saving Your Config

Create a `config.py` file for easy management:

```python
# config.py
# Detection Configuration
MAX_CAPACITY = 2
PERSON_CONF = 0.40
PHONE_CONF = 0.35
ROI_X1, ROI_Y1 = 150, 100
ROI_X2, ROI_Y2 = 500, 400
CAMERA_INDEX = 0
ALERT_COOLDOWN = 1.5
PHOTO_COOLDOWN = 7.0

# Dashboard Configuration
DASHBOARD_PORT = 5000
REFRESH_INTERVAL = 30000  # milliseconds
```

Then in main.py:
```python
from config import *
```

---

**For questions about configuration, refer to README.md or run validate_setup.py**
