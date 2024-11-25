#include <NewPing.h>
#include <Servo.h> // Include the Servo library

#include <WiFiS3.h>
#include <ArduinoOTA.h>

#define SECRET_SSID "My wife-eye"
#define SECRET_PASS "pegoku08"

char ssid[] = SECRET_SSID;    
char pass[] = SECRET_PASS;    
int status = WL_IDLE_STATUS;  

// Pin definitions
#define TRIGGER_PIN1  3
#define ECHO_PIN1     2
#define TRIGGER_PIN2  5
#define ECHO_PIN2     4
#define TRIGGER_PIN3  7
#define ECHO_PIN3     6
#define MaxDistance   150

// Motor Control Pins
#define IN1_PIN       9
#define IN2_PIN       8
#define ENABLE_PIN    10

// Servo Control
Servo steeringServo;
#define SERVO_PIN 11
#define mid 122
// PID constants
float Kp = 0.9;
float Ki = 0.3;
float Kd = 0.8;

// PID variables
float previousError = 0;
float integral = 0;

// Sensor Setup
NewPing sonarRight(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
NewPing sonarLeft(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

void forward() {
  analogWrite(ENABLE_PIN, 200);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
}

void stop() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENABLE_PIN, 255);  // Ajusta la velocidad al máximo inverso
  delay(200);  // Pequeño retraso para aplicar el freno

  // Detener el motor completamente
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENABLE_PIN, 0);
}

void setup() {
  // Motor Control
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  stop();

  // Servo Control (120 mid)

  steeringServo.attach(SERVO_PIN);
  steeringServo.write(mid);

  // Serial Communication
  Serial.begin(9600);

  // // check for the WiFi module:
  // if (WiFi.status() == WL_NO_MODULE) {
  //   Serial.println("Communication with WiFi module failed!");
  //   // don't continue
  //   while (true)
  //     ;
  // }

  // // attempt to connect to WiFi network:
  // while (status != WL_CONNECTED) {
  //   Serial.print("Attempting to connect to WPA SSID: ");
  //   Serial.println(ssid);
  //   // Connect to WPA/WPA2 network:
  //   status = WiFi.begin(ssid, pass);

  //   delay(1000);
  // }

  // // start the WiFi OTA library with internal (flash) based storage
  // // The IDE will prompt for this password during upload
  // ArduinoOTA.begin(WiFi.localIP(), "Arduino", "password", InternalStorage);

  // // you're connected now, so print out the status:
  // printWifiStatus();
}

void loop() {

  // // OTA
  // printWifiStatus();  //sign of life
  // // check for WiFi OTA updates
  // ArduinoOTA.poll();

  if (sonarFront.ping_cm() < 10 && sonarFront.ping_cm() != 0) {
    stop();
    return;
  } else if (sonarRight.ping_cm() == 0) {
    steeringServo.write(80);
    delay(750);
    forward();
    return;
  } else if (sonarLeft.ping_cm() == 0) {
    steeringServo.write(164);
    delay(750);
    forward();
    return;
  } else
  {
  
  int distanceRight = sonarRight.ping_cm();
  int distanceLeft = sonarLeft.ping_cm();

  // Calculate error (difference between left and right distances)
  float error = distanceLeft - distanceRight;

  // Calculate integral
  integral += error;

  // Calculate derivative
  float derivative = error - previousError;

  // Calculate PID output
  float output = Kp * error + Ki * integral + Kd * derivative;

  // Calculate the new servo angle
  float newServoAngle = mid + output;

  // Constrain the servo angle to be within 80 to 160 degrees
  newServoAngle = constrain(newServoAngle, 80, 164);

  // Always move forward
  forward();

  // Set the servo to the new constrained angle
  steeringServo.write(newServoAngle);

  // Update previous error
  previousError = error;

  // Print debug information
  Serial.print("Distance Right: ");
  Serial.print(distanceRight);
  Serial.print(" cm, Distance Left: ");
  Serial.print(distanceLeft);
  Serial.print(" cm, Error: ");
  Serial.print(error);
  Serial.print(", Output: ");
  Serial.print(output);
  Serial.print(", Servo Angle: ");
  Serial.println(newServoAngle);

  delay(100); // Delay for stability
  }
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