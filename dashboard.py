"""
=============================================================
  Real-Time Analytics Dashboard
  Displays incident statistics, charts, and live metrics
  from the Zone Occupancy & Phone Detection system
=============================================================
"""
from flask import Flask, jsonify, request, send_from_directory
from datetime import datetime, timedelta
import sqlite3
import os

app = Flask(__name__, template_folder='.', static_folder='.')

DB_FILE = "detection_incidents.db"
SNAPSHOT_FOLDER = "phone_incidents"

def get_db():
    """Get database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def dashboard():
    """Render the main dashboard HTML."""
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        return f.read()


@app.route('/api/snapshot/<path:filename>')
def serve_snapshot(filename):
    """Serve incident snapshot images safely."""
    return send_from_directory(os.path.abspath(SNAPSHOT_FOLDER), filename)


@app.route('/api/incidents')
def get_incidents():
    """Get incidents with optional filtering."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get query parameters
    days = request.args.get('days', 1, type=int)
    min_confidence = request.args.get('min_confidence', 0, type=float)
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # Calculate date range
    since = datetime.now() - timedelta(days=days)
    
    # Query incidents
    cursor.execute("""
        SELECT * FROM incidents 
        WHERE timestamp > ? AND phone_confidence >= ?
        ORDER BY timestamp DESC
        LIMIT ? OFFSET ?
    """, (since.isoformat(), min_confidence, per_page, (page - 1) * per_page))
    
    incidents = [dict(row) for row in cursor.fetchall()]
    
    # Get total count for pagination
    cursor.execute("""
        SELECT COUNT(*) as count FROM incidents 
        WHERE timestamp > ? AND phone_confidence >= ?
    """, (since.isoformat(), min_confidence))
    
    total_count = cursor.fetchone()['count']
    conn.close()
    
    return jsonify({
        'incidents': incidents,
        'total': total_count,
        'page': page,
        'per_page': per_page,
        'total_pages': (total_count + per_page - 1) // per_page
    })


@app.route('/api/stats')
def get_stats():
    """Get overall statistics."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Total incidents
    cursor.execute("SELECT COUNT(*) as count FROM incidents")
    total_incidents = cursor.fetchone()['count']
    
    # Last 24 hours
    since_24h = datetime.now() - timedelta(hours=24)
    cursor.execute(
        "SELECT COUNT(*) as count FROM incidents WHERE timestamp > ?",
        (since_24h.isoformat(),)
    )
    incidents_24h = cursor.fetchone()['count']
    
    # Average confidence
    cursor.execute("SELECT AVG(phone_confidence) as avg_conf FROM incidents")
    avg_confidence = cursor.fetchone()['avg_conf'] or 0
    
    # Max people in zone
    cursor.execute("SELECT MAX(people_in_zone) as max_people FROM incidents")
    max_people = cursor.fetchone()['max_people'] or 0
    
    # High confidence incidents (>0.8)
    cursor.execute(
        "SELECT COUNT(*) as count FROM incidents WHERE phone_confidence > 0.8"
    )
    high_confidence = cursor.fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total_incidents': total_incidents,
        'incidents_24h': incidents_24h,
        'avg_confidence': round(avg_confidence, 3),
        'max_people': max_people,
        'high_confidence_count': high_confidence
    })


@app.route('/api/timeline')
def get_timeline():
    """Get hourly incident timeline for the last 7 days."""
    conn = get_db()
    cursor = conn.cursor()
    
    since = datetime.now() - timedelta(days=7)
    
    cursor.execute("""
        SELECT 
            DATE(timestamp) as date,
            strftime('%H', timestamp) as hour,
            COUNT(*) as incident_count,
            AVG(phone_confidence) as avg_confidence
        FROM incidents
        WHERE timestamp > ?
        GROUP BY date, hour
        ORDER BY timestamp ASC
    """, (since.isoformat(),))
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    # Format for chart
    labels = [f"{row['date']} {row['hour']}:00" for row in data]
    incident_counts = [row['incident_count'] for row in data]
    confidences = [round(row['avg_confidence'], 2) for row in data]
    
    return jsonify({
        'labels': labels,
        'incident_counts': incident_counts,
        'confidences': confidences
    })


@app.route('/api/confidence-distribution')
def get_confidence_distribution():
    """Get confidence score distribution."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Bin confidence scores
    bins = [
        (0.0, 0.2),
        (0.2, 0.4),
        (0.4, 0.6),
        (0.6, 0.8),
        (0.8, 1.0)
    ]
    
    distribution = {}
    for low, high in bins:
        cursor.execute(
            "SELECT COUNT(*) as count FROM incidents WHERE phone_confidence BETWEEN ? AND ?",
            (low, high)
        )
        count = cursor.fetchone()['count']
        distribution[f"{int(low*100)}-{int(high*100)}%"] = count
    
    conn.close()
    
    return jsonify(distribution)


@app.route('/api/peak-hours')
def get_peak_hours():
    """Get incidents by hour of day."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            strftime('%H', timestamp) as hour,
            COUNT(*) as incident_count
        FROM incidents
        GROUP BY hour
        ORDER BY hour ASC
    """)
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    hours = [row['hour'] + ':00' for row in data]
    counts = [row['incident_count'] for row in data]
    
    return jsonify({
        'hours': hours,
        'counts': counts
    })


@app.route('/api/daily-summary')
def get_daily_summary():
    """Get incidents per day for the last 30 days."""
    conn = get_db()
    cursor = conn.cursor()
    
    since = datetime.now() - timedelta(days=30)
    
    cursor.execute("""
        SELECT 
            DATE(timestamp) as date,
            COUNT(*) as incident_count,
            AVG(phone_confidence) as avg_confidence,
            MAX(people_in_zone) as max_people
        FROM incidents
        WHERE timestamp > ?
        GROUP BY date
        ORDER BY date ASC
    """, (since.isoformat(),))
    
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({
        'dates': [row['date'] for row in data],
        'incident_counts': [row['incident_count'] for row in data],
        'avg_confidences': [round(row['avg_confidence'], 2) for row in data],
        'max_people': [row['max_people'] for row in data]
    })


@app.route('/api/system-health')
def get_system_health():
    """Get system health indicators."""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if data is being written (last incident within 1 hour)
    cursor.execute(
        "SELECT MAX(timestamp) as last_incident FROM incidents"
    )
    result = cursor.fetchone()
    last_incident = result['last_incident']
    
    if last_incident:
        last_time = datetime.fromisoformat(last_incident)
        time_since = datetime.now() - last_time
        is_active = time_since.total_seconds() < 3600  # 1 hour
    else:
        is_active = False
    
    # Get incident rate (incidents per hour)
    since_24h = datetime.now() - timedelta(hours=24)
    cursor.execute(
        "SELECT COUNT(*) as count FROM incidents WHERE timestamp > ?",
        (since_24h.isoformat(),)
    )
    incidents_24h = cursor.fetchone()['count']
    incident_rate = round(incidents_24h / 24, 2)
    
    conn.close()
    
    return jsonify({
        'is_active': is_active,
        'last_incident': last_incident,
        'incident_rate_per_hour': incident_rate,
        'database_file': os.path.abspath(DB_FILE),
        'snapshots_folder': os.path.abspath(SNAPSHOT_FOLDER)
    })


if __name__ == '__main__':
    if not os.path.exists(DB_FILE):
        print(f"[WARNING] Database file '{DB_FILE}' not found.")
        print("[INFO] Start the detection script first to create the database.")
    
    print("[INFO] Starting Analytics Dashboard...")
    print("[INFO] Open your browser: http://localhost:5000")
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
