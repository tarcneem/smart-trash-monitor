# 🗑️ Smart Trash Monitor

A real-time IoT waste management system that monitors trash bin fill levels and displays their status on a live map dashboard.

Built with ESP32, Python Flask, SQLite, and Leaflet.js.

---

## 📸 Dashboard Preview

> Real-time map showing bin status across Beit Hanina, Jerusalem.
> Green = OK | Yellow = Half Full | Red = Full

<img width="1916" height="889" alt="image" src="https://github.com/user-attachments/assets/ea2e0940-9c01-4346-8f6a-e1f75c712579" />

---

## 🧠 System Architecture

```
HC-SR04 Sensor
      │
   ESP32 (WiFi)
      │
      ▼
Flask Server (Python)
      │
   SQLite DB
      │
      ▼
Web Dashboard (Leaflet.js)
```

---

## ⚙️ How It Works

1. The **HC-SR04 ultrasonic sensor** measures the distance between the bin lid and the trash inside
2. The **ESP32** calculates the fill percentage and sends it to the server every 10 seconds over WiFi
3. The **Flask server** receives the data, stores it in a SQLite database, and serves it to the dashboard
4. The **web dashboard** displays all bins on an interactive map with color-coded status, updating automatically every 10 seconds

**Fill level logic:**
- 🟢 0–49% → OK
- 🟡 50–79% → Half Full
- 🔴 80–100% → Full (needs pickup)

---

## 🛠️ Hardware Requirements

| Component | Purpose |
|-----------|---------|
| ESP32 (Freenove or similar) | WiFi-enabled microcontroller |
| HC-SR04 Ultrasonic Sensor | Fill level measurement |
| Jumper wires | Connections |
| USB cable | Power & programming |

**Wiring:**
| HC-SR04 Pin | ESP32 Pin |
|-------------|-----------|
| VCC | 3.3V / 5V |
| GND | GND |
| TRIG | GPIO 5 |
| ECHO | GPIO 18 |

---

## 💻 Software Requirements

- Python 3.x
- Arduino IDE with ESP32 board support
- Required Python packages:

```bash
pip install flask flask-cors
```

---

## 🚀 Getting Started

### 1. Set up the server

```bash
git clone https://github.com/YOUR_USERNAME/smart-trash-monitor.git
cd smart-trash-monitor
pip install flask flask-cors
python server.py
```

Server runs on `http://localhost:5000`

### 2. Flash the ESP32

Open `smart_trash_monitor.ino` in Arduino IDE and update:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverURL = "http://YOUR_LAPTOP_IP:5000/update";
```

Flash to your ESP32.

### 3. Open the dashboard

Go to `http://YOUR_LAPTOP_IP:5000` in your browser.

---

## 📁 Project Structure

```
smart-trash-monitor/
├── server.py              # Flask backend + SQLite database
├── dashboard.html         # Real-time web dashboard
├── smart_trash_monitor/
│   └── smart_trash_monitor.ino   # ESP32 firmware
└── README.md
```

---

## 🔧 Key Engineering Decisions

**Why ultrasonic sensing?**
The HC-SR04 provides reliable distance measurements in the 2–200cm range, making it ideal for bin fill detection. Averaging 3 readings reduces noise from spurious reflections.

**Why Flask + SQLite?**
Lightweight and deployable without external dependencies. SQLite stores historical readings locally, enabling future analytics features.

**Why Leaflet.js?**
Open-source, lightweight map library with no API key required. Supports real-time marker updates without page reload.

**Scalability**
Each additional bin requires only one ESP32 + sensor with a unique `BIN_ID`. The server and dashboard scale to any number of bins without code changes.

---

## 📊 Future Improvements

- [ ] Predictive fill alerts based on historical data
- [ ] Analytics dashboard showing fill patterns over time
- [ ] Optimized collection route based on bin priority
- [ ] Computer vision integration for waste type classification
- [ ] Cloud deployment for remote monitoring

---

## 👩‍💻 Author

**Tarneem** — Electrical & Electronics Engineer  

---

## 📄 License

MIT License
