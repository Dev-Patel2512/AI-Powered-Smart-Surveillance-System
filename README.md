# Zone Occupancy & Phone Detection System with Analytics Dashboard

An intelligent real-time monitoring system that detects people in a defined zone and alerts when smartphones are detected. Includes a comprehensive web-based analytics dashboard.

## Features

✅ **Real-Time Detection**
- YOLOv8-based person and smartphone detection
- Configurable ROI zone with capacity limits
- Live FPS counter and visual alerts

✅ **Smart Alerting**
- Sound alerts for capacity violations and phone detection
- Native Windows notifications
- Orange danger alert when phones are detected
- Customizable alert thresholds

✅ **Incident Management**
- Auto-capture snapshots when phones detected
- CSV incident logging with timestamps
- SQLite database for efficient querying
- Organized snapshot folder structure

✅ **Analytics Dashboard**
- Real-time incident statistics
- Interactive charts and visualizations:
  - Timeline of incidents (hourly/daily)
  - Confidence score distribution
  - Peak hours analysis
  - 30-day summary trends
- Searchable incident history table with pagination
- Time range and confidence filtering
- System health indicator
- Live auto-refresh (every 30 seconds)

## Installation

### Prerequisites
- Python 3.8+
- Webcam access
- Windows OS (for native notifications)

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **First run will auto-download the YOLOv8 model** (~6 MB)

## Usage

### Starting the Detection System

```bash
python main.py
```

The script will:
1. Load the YOLOv8 model
2. Open your webcam
3. Start real-time detection
4. Create incident logs and snapshots
5. Print: `Dashboard will be available at: http://localhost:5000`

**Controls:**
- Press `Q` to quit the detection system

### Accessing the Analytics Dashboard

In a **separate terminal/PowerShell**, run:

```bash
python dashboard.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

The dashboard automatically connects to the SQLite database and displays:
- Live statistics
- Interactive charts
- Incident history
- System health status

## Configuration

Edit `main.py` to customize:

```python
MAX_CAPACITY       = 2          # Max people in zone
PERSON_CONF        = 0.40       # Detection confidence (0-1)
PHONE_CONF         = 0.35       # Phone detection confidence (0-1)
ALERT_COOLDOWN     = 1.5        # Seconds between alerts
PHOTO_COOLDOWN     = 7.0        # Seconds between snapshots
ROI_X1, ROI_Y1     = 150, 100   # Zone top-left corner
ROI_X2, ROI_Y2     = 500, 400   # Zone bottom-right corner
CAMERA_INDEX       = 0          # Webcam index (0=default)
```

## File Structure

```
Face_detection_project/
├── main.py                  # Main detection script
├── dashboard.py             # Flask web dashboard
├── dashboard.html           # Dashboard UI
├── detection_incidents.db   # SQLite database (auto-created)
├── incident_log.csv         # CSV incident log
├── phone_incidents/         # Folder for snapshots
├── requirements.txt         # Python dependencies
└── yolov8n.pt              # YOLOv8 model (auto-downloaded)
```

## Dashboard Features

### Statistics Cards
- **Total Incidents**: All recorded phone incidents
- **Last 24 Hours**: Recent incident count
- **Avg Confidence**: Average detection confidence score
- **High Confidence Count**: Incidents with >80% confidence

### Charts

1. **Incidents Over Time** (Line chart)
   - Shows hourly incident distribution
   - Last 7 days of data

2. **Confidence Distribution** (Doughnut chart)
   - Visualizes confidence score ranges (0-20%, 20-40%, etc.)

3. **Peak Hours** (Bar chart)
   - Incidents grouped by hour of day
   - Identifies when most phone usage occurs

4. **Daily Summary** (Bar chart)
   - Incidents per day for last 30 days
   - Trend analysis over time

### Incident History Table
- Searchable, paginated table of all incidents
- Filter by:
  - Time range (24h, 7d, 30d, 90d)
  - Confidence threshold (50%+, 70%+, 80%+, 90%+)
- View snapshot links for each incident
- Color-coded confidence badges

### System Health
- Real-time indicator (Green = Active, Red = Inactive)
- Last incident timestamp
- Incident rate per hour
- Database file location

## Database Schema

### incidents table
```sql
incident_id INTEGER PRIMARY KEY
timestamp DATETIME
date TEXT
time TEXT
people_in_zone INTEGER
phone_confidence REAL
snapshot_file TEXT
```

### hourly_stats table (for caching)
```sql
hour_start DATETIME PRIMARY KEY
incident_count INTEGER
avg_confidence REAL
max_people INTEGER
```

## Tips & Tricks

1. **Run both in parallel:**
   ```bash
   # Terminal 1: Start detection
   python main.py
   
   # Terminal 2: Start dashboard (after 30 seconds)
   python dashboard.py
   ```

2. **View live camera feed** while monitoring dashboard for real-time incident correlation

3. **Export data** by querying the SQLite database:
   ```bash
   # Use any SQLite client to query detection_incidents.db
   ```

4. **Adjust ROI** on-screen by editing coordinates in main.py and restarting

5. **Batch process snapshots** from the `phone_incidents/` folder

## Troubleshooting

**Dashboard shows "No incidents found"**
- Make sure the detection script (main.py) is running first
- Check that incidents have been recorded in the database
- Verify the database file exists: `detection_incidents.db`

**Webcam not detected**
- Change `CAMERA_INDEX` to 1, 2, etc. if you have multiple cameras
- Check Windows Device Manager for camera conflicts

**Alert sounds not working**
- Verify Windows sound output is enabled
- Check volume settings

**Dashboard port already in use**
- Change the port in `dashboard.py`: `app.run(port=5001)`
- Or kill the process using port 5000

## Performance Notes

- Detection: ~30-50 FPS on modern hardware
- Dashboard: Minimal overhead, queries run on SQLite (fast)
- Smooth operation with both scripts running simultaneously
- Auto-cleanup prevents log file bloat

## API Endpoints (for custom integrations)

```
GET /api/stats                   - Overall statistics
GET /api/incidents              - Paginated incident list
GET /api/timeline               - Hourly timeline data
GET /api/confidence-distribution - Confidence bins
GET /api/peak-hours             - Incidents by hour
GET /api/daily-summary          - Daily summary data
GET /api/system-health          - System status
```

## Future Enhancements

Possible additions:
- Email/SMS alerts for high-confidence detections
- Multi-zone support with separate configs
- Person tracking and re-identification
- Cloud backup of incidents
- Mobile app integration
- Custom alert rules engine
- Automated reports generation

## License

This project uses YOLOv8 (Ultralytics) and is provided as-is for monitoring and security purposes.

---

**Need help?** Check the console output of both scripts for detailed logging and error messages.
