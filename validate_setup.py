#!/usr/bin/env python3
"""
Validation script to check if the enhanced detection system is set up correctly
Run this before starting the main detection and dashboard applications
"""

import os
import sys
import sqlite3
from pathlib import Path

print("=" * 60)
print("  Zone Occupancy Detection System - Setup Validator")
print("=" * 60)
print()

errors = []
warnings = []
success_count = 0

# Check 1: Python version
print("[CHECK 1] Python version...")
if sys.version_info >= (3, 8):
    print("  [OK]   Python 3.8+ detected")
    success_count += 1
else:
    errors.append("Python 3.8+ required")
    print(f"  [FAIL] Python {sys.version_info.major}.{sys.version_info.minor} detected (need 3.8+)")

print()

# Check 2: Required files
print("[CHECK 2] Required files...")
required_files = [
    "main.py",
    "dashboard.py",
    "dashboard.html",
    "requirements.txt",
    "yolov8n.pt"
]

for file in required_files:
    if os.path.exists(file):
        print(f"  [OK]   {file}")
        success_count += 1
    else:
        if file == "yolov8n.pt":
            warnings.append(f"{file} will be downloaded on first run")
            print(f"  [WARN] {file} (will auto-download on first run)")
        else:
            errors.append(f"{file} not found")
            print(f"  [FAIL] {file} NOT FOUND")

print()

# Check 3: Required folders
print("[CHECK 3] Required folders...")
required_folders = [
    "phone_incidents"
]

for folder in required_folders:
    if os.path.isdir(folder):
        print(f"  [OK]   {folder}/ exists")
        success_count += 1
    else:
        print(f"  [WARN] {folder}/ will be created on first run")
        warnings.append(f"{folder} will be created automatically")

print()

# Check 4: Python packages
print("[CHECK 4] Required Python packages...")
required_packages = {
    "cv2": "opencv-python",
    "ultralytics": "ultralytics",
    "flask": "flask",
    "winotify": "winotify"
}

missing_packages = []
for module, package_name in required_packages.items():
    try:
        __import__(module)
        print(f"  [OK]   {module}")
        success_count += 1
    except ImportError:
        print(f"  [FAIL] {module} (package: {package_name})")
        missing_packages.append(package_name)

if missing_packages:
    errors.append(f"Missing packages: {', '.join(missing_packages)}")

print()

# Check 5: Database setup
print("[CHECK 5] Database setup...")
db_file = "detection_incidents.db"

if os.path.exists(db_file):
    print(f"  [OK]   {db_file} exists")
    success_count += 1

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check for incidents table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents'")
        if cursor.fetchone():
            print("  [OK]   incidents table exists")
            success_count += 1
        else:
            print("  [WARN] incidents table will be created on first run")
            warnings.append("incidents table will be created automatically")

        conn.close()
    except Exception as e:
        errors.append(f"Database error: {e}")
        print(f"  [FAIL] Database error: {e}")
else:
    print(f"  [WARN] {db_file} will be created on first run")
    warnings.append("Database will be created automatically on first run")

print()

# Check 6: CSV log file
print("[CHECK 6] CSV log file...")
csv_file = "incident_log.csv"

if os.path.exists(csv_file):
    print(f"  [OK]   {csv_file} exists")
    success_count += 1

    # Check if it has headers
    try:
        with open(csv_file, 'r') as f:
            first_line = f.readline()
            if "incident_id" in first_line:
                print("  [OK]   CSV headers found")
                success_count += 1
            else:
                print("  [WARN] CSV headers may be missing")
                warnings.append("CSV file may need headers")
    except Exception as e:
        print(f"  [FAIL] CSV read error: {e}")
else:
    print(f"  [WARN] {csv_file} will be created on first run")
    warnings.append("CSV log will be created automatically")

print()

# Check 7: Snapshots folder contents
print("[CHECK 7] Snapshots folder...")
if os.path.isdir("phone_incidents"):
    num_files = len(os.listdir("phone_incidents"))
    if num_files > 0:
        print(f"  [OK]   {num_files} snapshots found")
        success_count += 1
    else:
        print("  [WARN] No snapshots yet (will be created after first detection)")
        warnings.append("No snapshots yet")

print()

# Summary
print("=" * 60)
print("  VALIDATION SUMMARY")
print("=" * 60)
print(f"[OK]   Checks passed: {success_count}")

if warnings:
    print(f"[WARN] Warnings: {len(warnings)}")
    for warning in warnings:
        print(f"  - {warning}")

if errors:
    print(f"[FAIL] Errors: {len(errors)}")
    for error in errors:
        print(f"  - {error}")
    print()
    print("RECOMMENDATION:")
    print("  Run: pip install -r requirements.txt")
    print()
else:
    print()
    print("[OK] All checks passed! You're ready to start.")
    print()
    print("NEXT STEPS:")
    print("  1. Terminal 1: python main.py")
    print("  2. Terminal 2: python dashboard.py")
    print("  3. Open browser: http://localhost:5000")

print()

sys.exit(0 if not errors else 1)
