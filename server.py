from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('trash.db')
    c = conn.cursor()
    
    # Bins table
    c.execute('''CREATE TABLE IF NOT EXISTS bins (
        id INTEGER PRIMARY KEY,
        name TEXT,
        location TEXT,
        lat REAL,
        lng REAL
    )''')
    
    # Readings table
    c.execute('''CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bin_id INTEGER,
        distance REAL,
        fill_percent REAL,
        timestamp TEXT
    )''')
    
    # Add a test bin
    c.execute('''INSERT OR IGNORE INTO bins (id, name, location, lat, lng) 
             VALUES (1, "Taha Hussein St - Bin 1", "Beit Hanina - Taha Hussein Street", 31.8346, 35.2269)''')

    c.execute('''INSERT OR IGNORE INTO bins (id, name, location, lat, lng) 
                VALUES (2, "Taha Hussein St - Bin 2", "Beit Hanina - Taha Hussein Street", 31.8338, 35.2275)''')

    c.execute('''INSERT OR IGNORE INTO bins (id, name, location, lat, lng) 
                VALUES (3, "Beit Hanina Main Street", "Beit Hanina - Main Street", 31.8301, 35.2252)''')

    c.execute('''INSERT OR IGNORE INTO bins (id, name, location, lat, lng) 
                VALUES (4, "Beit Hanina Market Area", "Beit Hanina - Market", 31.8320, 35.2260)''')
    conn.commit()
    conn.close()

# Receive data from ESP32
@app.route('/update', methods=['POST'])
def update():
    data = request.json
    bin_id = data.get('bin_id', 1)
    distance = data.get('distance')
    bin_height = 50  # bin depth in cm
    fill_percent = max(0, min(100, (1 - distance / bin_height) * 100))
    
    conn = sqlite3.connect('trash.db')
    c = conn.cursor()
    c.execute('''INSERT INTO readings (bin_id, distance, fill_percent, timestamp)
                 VALUES (?, ?, ?, ?)''',
              (bin_id, distance, fill_percent, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    print(f"Bin {bin_id}: {fill_percent:.1f}% full")
    return jsonify({"status": "ok", "fill_percent": fill_percent})

# Send data to Dashboard
@app.route('/status', methods=['GET'])
def status():
    conn = sqlite3.connect('trash.db')
    c = conn.cursor()
    
    c.execute('''SELECT b.id, b.name, b.location, b.lat, b.lng, 
                        r.fill_percent, r.timestamp
                 FROM bins b
                 LEFT JOIN readings r ON r.id = (
                     SELECT id FROM readings 
                     WHERE bin_id = b.id 
                     ORDER BY timestamp DESC LIMIT 1
                 )''')
    
    bins = []
    for row in c.fetchall():
        bins.append({
            "id": row[0],
            "name": row[1],
            "location": row[2],
            "lat": row[3],
            "lng": row[4],
            "fill_percent": round(row[5], 1) if row[5] else 0,
            "last_update": row[6] or "No data"
        })
    
    conn.close()
    return jsonify(bins)
@app.route('/')
def dashboard():
    return send_from_directory('.', 'dashboard.html')




if __name__ == '__main__':
    init_db()
    print("Server running on http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000)