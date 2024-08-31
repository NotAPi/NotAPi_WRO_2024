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
Servo myservo;
#define SERVO_PIN 11

NewPing sonarRight(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
NewPing sonarLeft(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

void forward() {
  analogWrite(ENABLE_PIN, 150);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
}

void stop() {
  analogWrite(ENABLE_PIN, 150);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

void setup() {
  // put your setup code here, to run once:

}

void loop() {
  // put your main code here, to run repeatedly:

}
