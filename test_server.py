import os
from flask import Flask, send_from_directory

app = Flask(__name__)
SNAPSHOT_FOLDER = "phone_incidents"

@app.route('/api/snapshot/<path:filename>')
def serve_snapshot(filename):
    return send_from_directory(os.path.abspath(SNAPSHOT_FOLDER), filename)

if __name__ == '__main__':
    print("Starting test server on 5001")
    app.run(port=5001)
