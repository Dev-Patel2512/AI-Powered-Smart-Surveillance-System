"""
Hikvision Live People Counter
==============================
Connects to a Hikvision RTSP camera, detects every human face in real time,
draws a GREEN SQUARE around each face, and shows a live count on screen.

Requirements:
    pip install opencv-python numpy

Run:
    python hikvision_people_counter.py

Press   Q   inside the video window to quit.
Press   UP ARROW / DOWN ARROW   to adjust sensitivity dynamically.
"""

import cv2
import threading
import time
import sys
import os
import urllib.request
import numpy as np

# ==============================================================================
#  CONFIGURATION  — edit these values to match your setup
# ==============================================================================

IP_ADDRESS           = "172.31.1.62" #172.31.1.60
RTSP_URL             = f"rtsp://admin:Admin%40123@{IP_ADDRESS}:554/Streaming/Channels/101"

CONFIDENCE_THRESHOLD = 0.50   # 0.0–1.0  (lower = detect more, higher = stricter)
BOX_COLOR            = (0, 255, 0)   # BGR  →  pure green
BOX_THICKNESS        = 2             # pixels
CORNER_LENGTH        = 18            # length of each corner bracket arm (pixels)
DISPLAY_WIDTH        = 1280          # output window width
DISPLAY_HEIGHT       = 720           # output window height
RECONNECT_DELAY      = 3.0           # seconds between reconnect attempts

# Caffe model files (auto-downloaded on first run)
PROTO_FILE = "deploy.prototxt"
MODEL_FILE = "res10_300x300_ssd_iter_140000.caffemodel"


# ==============================================================================
#  AUTO-DOWNLOADER  — fetches model weights if not present
# ==============================================================================

def download_models() -> None:
    files = {
        PROTO_FILE: (
            "https://raw.githubusercontent.com/opencv/opencv/master/"
            "samples/dnn/face_detector/deploy.prototxt"
        ),
        MODEL_FILE: (
            "https://github.com/opencv/opencv_3rdparty/raw/"
            "dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"
        ),
    }
    for fname, url in files.items():
        if not os.path.exists(fname):
            print(f"[SETUP] Downloading {fname} ...")
            try:
                urllib.request.urlretrieve(url, fname)
                print(f"[SETUP] {fname} ready.")
            except Exception as e:
                print(f"[ERROR] Failed to download {fname}: {e}")
                sys.exit(1)


# ==============================================================================
#  THREAD-SAFE RTSP STREAM
# ==============================================================================

class LiveCameraStream:
    """
    Grabs frames on a background daemon thread so the main loop always gets
    the freshest frame with no network-buffer lag.
    A threading.Lock keeps reads and writes fully thread-safe.
    Auto-reconnects if the stream drops.
    """

    def __init__(self, url: str) -> None:
        self.url     = url
        self._lock   = threading.Lock()
        self._stopped = False
        self._ret    = False
        self._frame  = None
        self._cap    = self._connect()

    # ── internal helpers ──────────────────────────────────────────────────────

    def _connect(self) -> cv2.VideoCapture:
        cap = cv2.VideoCapture(self.url)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        if not cap.isOpened():
            print("\n[ERROR] Cannot open RTSP stream.")
            print(f"        → {self.url}")
            print("        Check network / IP / credentials.\n")
            sys.exit(1)
        ret, frame = cap.read()
        with self._lock:
            self._ret, self._frame = ret, frame
        print(f"[INFO]  Connected to {self.url}")
        return cap

    def _update(self) -> None:
        while not self._stopped:
            if not self._cap.isOpened():
                print(f"[WARN]  Stream lost — retrying in {RECONNECT_DELAY}s ...")
                time.sleep(RECONNECT_DELAY)
                self._cap = self._connect()
                continue
            ret, frame = self._cap.read()
            if not ret:
                time.sleep(0.01)
                continue
            with self._lock:
                self._ret, self._frame = ret, frame

    # ── public API ────────────────────────────────────────────────────────────

    def start(self) -> "LiveCameraStream":
        t = threading.Thread(target=self._update, daemon=True)
        t.start()
        return self

    def read(self):
        with self._lock:
            if self._frame is None:
                return False, None
            return self._ret, self._frame.copy()

    def stop(self) -> None:
        self._stopped = True
        self._cap.release()


# ==============================================================================
#  DRAWING HELPERS
# ==============================================================================

def draw_corner_square(
    img: np.ndarray,
    x1: int, y1: int,
    x2: int, y2: int,
    color: tuple,
    thickness: int,
    arm: int,
) -> None:
    """
    Draw a stylish corner-bracket rectangle (like a targeting reticle).
    Four corners only — looks cleaner than a solid box on a busy background.
    """
    # Top-left
    cv2.line(img, (x1,      y1),      (x1 + arm, y1),      color, thickness)
    cv2.line(img, (x1,      y1),      (x1,       y1 + arm), color, thickness)
    # Top-right
    cv2.line(img, (x2,      y1),      (x2 - arm, y1),      color, thickness)
    cv2.line(img, (x2,      y1),      (x2,       y1 + arm), color, thickness)
    # Bottom-left
    cv2.line(img, (x1,      y2),      (x1 + arm, y2),      color, thickness)
    cv2.line(img, (x1,      y2),      (x1,       y2 - arm), color, thickness)
    # Bottom-right
    cv2.line(img, (x2,      y2),      (x2 - arm, y2),      color, thickness)
    cv2.line(img, (x2,      y2),      (x2,       y2 - arm), color, thickness)


def draw_face_label(
    img: np.ndarray,
    x1: int, y1: int,
    index: int,
    confidence: float,
    color: tuple,
) -> None:
    """Draw 'Face #N  XX%' tag just above the bounding box."""
    text      = f"Face #{index}  {confidence * 100:.0f}%"
    font      = cv2.FONT_HERSHEY_SIMPLEX
    scale     = 0.50
    thick     = 1

    (tw, th), bl = cv2.getTextSize(text, font, scale, thick)
    pad      = 4
    label_y  = max(y1 - 8, th + pad * 2)

    # Dark pill background
    cv2.rectangle(
        img,
        (x1,          label_y - th - pad),
        (x1 + tw + pad * 2, label_y + bl),
        (0, 0, 0),
        cv2.FILLED,
    )
    cv2.putText(img, text, (x1 + pad, label_y), font, scale, color, thick, cv2.LINE_AA)


def draw_hud(
    img: np.ndarray,
    count: int,
    fps: float,
    w: int,
    current_thresh: float,
) -> None:
    """
    Draw a top-centre HUD banner:
        👁  LIVE PEOPLE COUNT : 5   |   FPS : 24.3  |  SENSITIVITY: 50%
    """
    text  = f"  LIVE COUNT :  {count}   |   FPS : {fps:.1f}   |   CONFIDENCE: {current_thresh * 100:.0f}%  "
    font  = cv2.FONT_HERSHEY_DUPLEX
    scale = 0.75
    thick = 1

    (tw, th), bl = cv2.getTextSize(text, font, scale, thick)
    pad  = 10
    x    = (w - tw) // 2
    y    = th + pad * 2

    # Semi-opaque banner
    overlay = img.copy()
    cv2.rectangle(overlay, (x - pad, pad), (x + tw + pad, y + bl + pad), (0, 0, 0), cv2.FILLED)
    cv2.addWeighted(overlay, 0.55, img, 0.45, 0, img)

    # Green border line under the banner
    cv2.line(img, (x - pad, y + bl + pad), (x + tw + pad, y + bl + pad), BOX_COLOR, 1)

    cv2.putText(img, text, (x, y), font, scale, BOX_COLOR, thick, cv2.LINE_AA)


# ==============================================================================
#  MAIN
# ==============================================================================

def main() -> None:
    global CONFIDENCE_THRESHOLD

    # 1. Download model weights if needed
    download_models()

    # 2. Load the deep-learning face detector
    print("[INFO]  Loading neural network ...")
    net = cv2.dnn.readNetFromCaffe(PROTO_FILE, MODEL_FILE)
    print("[INFO]  Model loaded successfully.\n")

    # 3. Start the live RTSP stream
    camera = LiveCameraStream(RTSP_URL).start()
    time.sleep(1.0)   # warm-up — let the buffer fill
    print("[INFO]  Streaming. Press  Q  in the video window to quit.\n")

    # Metrics Tracking
    fps_timer   = time.time()
    fps_frames  = 0
    fps_display = 0.0
    session_peak = 0

    # ── Main loop ─────────────────────────────────────────────────────────────
    while True:
        ret, frame = camera.read()
        if not ret or frame is None:
            time.sleep(0.01)
            continue

        h, w = frame.shape[:2]

        # ── A. Build input blob and run inference ─────────────────────────────
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)),
            scalefactor = 1.0,
            size        = (300, 300),
            mean        = (104.0, 177.0, 123.0),
        )
        net.setInput(blob)
        detections = net.forward()          # shape (1, 1, N, 7)

        # ── B. Draw green squares on every detected face ──────────────────────
        face_count = 0

        for i in range(detections.shape[2]):
            conf = float(detections[0, 0, i, 2])
            if conf < CONFIDENCE_THRESHOLD:
                continue

            face_count += 1

            # Scale box coords from 300×300 back to original frame size
            raw = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            x1, y1, x2, y2 = raw.astype(int)

            # Clamp to frame edges
            x1 = max(0, x1);      y1 = max(0, y1)
            x2 = min(w - 1, x2);  y2 = min(h - 1, y2)

            # ── GREEN SQUARE (corner-bracket style) ───────────────────────────
            draw_corner_square(
                frame, x1, y1, x2, y2,
                color     = BOX_COLOR,
                thickness = BOX_THICKNESS,
                arm       = CORNER_LENGTH,
            )

            # ── Label above the box ───────────────────────────────────────────
            draw_face_label(frame, x1, y1, face_count, conf, BOX_COLOR)

        # Locked-in session tracking fix
        if face_count > session_peak:
            session_peak = face_count

        # ── C. FPS rolling average ────────────────────────────────────────────
        fps_frames += 1
        elapsed = time.time() - fps_timer
        if elapsed >= 1.0:
            fps_display = fps_frames / elapsed
            fps_frames  = 0
            fps_timer   = time.time()

        # ── D. Top-centre HUD banner ──────────────────────────────────────────
        draw_hud(frame, face_count, fps_display, w, CONFIDENCE_THRESHOLD)

        # ── E. Resize & display ───────────────────────────────────────────────
        display = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        cv2.imshow("Hikvision AI  —  Live Face Counter  [Q = quit]", display)

        # Handle Keyboard Inputs
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            print("\n[INFO]  Quit by user.")
            break
        # Dynamic threshold adjustment (Up/Down arrow keys or OS equivalents)
        elif key == 0 or key == 82: # Up Arrow
            CONFIDENCE_THRESHOLD = min(0.95, CONFIDENCE_THRESHOLD + 0.05)
        elif key == 1 or key == 84: # Down Arrow
            CONFIDENCE_THRESHOLD = max(0.05, CONFIDENCE_THRESHOLD - 0.05)

    # ── Clean shutdown ────────────────────────────────────────────────────────
    camera.stop()
    cv2.destroyAllWindows()
    print("\n=========================================")
    print("[OFFICE SESSION REPORT]")
    print(f" Peak people count detected: {session_peak}")
    print("=========================================")
    print("[INFO]  Application closed cleanly.")


if __name__ == "__main__":
    main()