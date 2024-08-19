#include <NewPing.h>
#include <Servo.h> // Include the Servo library

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

// PID constants
float Kp = 0.8;
float Ki = 0.2;
float Kd = 0.6;

// PID variables
float previousError = 0;
float integral = 0;

// Sensor Setup
NewPing sonarRight(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
NewPing sonarLeft(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

void forward() {
  analogWrite(ENABLE_PIN, 150);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
}

void stop() {
  analogWrite(ENABLE_PIN, 200);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  delay(50);
  analogWrite(ENABLE_PIN, 150);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

void setup() {
  // Motor Control
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  stop();

  // Servo Control (120 mid)
  steeringServo.attach(SERVO_PIN);
  steeringServo.write(120);

  // Serial Communication
  Serial.begin(9600);
}

void loop() {
  if (sonarFront.ping_cm() < 10 && sonarFront.ping_cm() != 0) {
    stop();
    return;
  } else if (sonarRight.ping_cm() == 0) {
    steeringServo.write(80);
    forward();
    return;
  } else if (sonarLeft.ping_cm() == 0) {
    steeringServo.write(160);
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
  float newServoAngle = 120 + output;

  // Constrain the servo angle to be within 80 to 160 degrees
  newServoAngle = constrain(newServoAngle, 80, 160);

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