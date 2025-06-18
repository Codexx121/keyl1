from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import os

app = Flask(__name__)
LOG_FILE = "logs/dashboard_logs.txt"

def clear_logs():
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("")

@app.route('/clear_logs', methods=['POST'])
def clear_logs_route():
    clear_logs()
    return redirect(url_for('dashboard'))  # redirect back to dashboard after clearing

os.makedirs("logs", exist_ok=True)
open(LOG_FILE, "a", encoding="utf-8").close()

@app.route('/')
def dashboard():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        logs = f.read()
    return render_template("dashboard.html", logs=logs)

@app.route('/log', methods=['POST'])
def receive_log():
    data = request.get_json()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {data.get('content', '')}\n")
    return {"status": "received"}, 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
