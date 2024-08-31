#include <WiFiS3.h>
#include <ArduinoOTA.h>

#define SECRET_SSID "My wife-eye"
#define SECRET_PASS "pegoku08"

char ssid[] = SECRET_SSID;    // your network SSID (name)
char pass[] = SECRET_PASS;    // your network password
int status = WL_IDLE_STATUS;  // the WiFi radio's status

void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  // while (!Serial) {
  // wait for serial port to connect. Needed for native USB port only
  //}
}

void loop() {
  // check the network connection once every 5 seconds:
  delay(5000);

  printWifiStatus();  //sign of life
  // check for WiFi OTA updates
  ArduinoOTA.poll();
}

void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}