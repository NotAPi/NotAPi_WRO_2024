#include <Servo.h>

// 80------110---150

// Motor Control Pins
#define IN1_PIN       9
#define IN2_PIN       8
#define ENABLE_PIN    10

Servo steeringServo;
#define SERVO_PIN 11
#define mid 109
#define max 80
#define min mid + (mid - max)

void setup() {
  // put your setup code here, to run once:
  steeringServo.attach(SERVO_PIN);
  steeringServo.write(140);
  Serial.begin(9600);

  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);


  analogWrite(ENABLE_PIN, 200);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);



}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(steeringServo.read());
  
}
