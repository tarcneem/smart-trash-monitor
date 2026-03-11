#include <WiFi.h>
#include <HTTPClient.h>

// WiFi
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// Server
const char* serverURL = "http://YOUR_LAPTOP_IP:5000/update";
// Pins
#define TRIG_PIN 5
#define ECHO_PIN 18
#define THRESHOLD 10
#define MAX_DISTANCE 200
#define BIN_ID 1
#define BIN_HEIGHT 50  // bin depth in cm

void sendToServer(float distance) {
  if (WiFi.status() != WL_CONNECTED) return;

  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");

  String payload = "{\"bin_id\":" + String(BIN_ID) + ",\"distance\":" + String(distance) + "}";
  int response = http.POST(payload);

  Serial.print("Server response: ");
  Serial.println(response);

  http.end();
}

float readDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  if (duration == 0) return -1;
  return duration * 0.034 / 2;
}

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  Serial.println(WiFi.localIP());
}

void loop() {
  float total = 0;
  int validReadings = 0;

  for (int i = 0; i < 3; i++) {
    float d = readDistance();
    if (d > 0 && d < MAX_DISTANCE) {
      total += d;
      validReadings++;
    }
    delay(50);
  }

  if (validReadings == 0) {
    Serial.println("No object detected");
    delay(2000);
    return;
  }

  float distance = total / validReadings;
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  sendToServer(distance);

  delay(10000); // Send every 10 seconds
}
