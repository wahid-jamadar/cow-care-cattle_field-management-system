#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "sadik";
const char* password = "12345678";
const char* serverUrl = "http://
:<port>/api/iot/send-data"; // Replace with your server's IP and port

void setup() {
  Serial.begin(115200);
  Serial.println("Starting...");

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Example data payload
    String payload = "{";
    payload += "\"device_id\": \"device123\",";
    payload += "\"temperature\": 38.5,";
    payload += "\"heart_rate\": 75,";
    payload += "\"spo2\": 95,";
    payload += "\"motion_x\": 0.1,";
    payload += "\"motion_y\": 0.2,";
    payload += "\"motion_z\": 0.3";
    payload += "}";

    Serial.println("Sending data: " + payload);

    int httpResponseCode = http.POST(payload);

    Serial.print("Response code: ");
    Serial.println(httpResponseCode);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Server response:");
      Serial.println(response);
    } else {
      Serial.println("Error in request");
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected!");
  }

  delay(5000);
}