#include <NewPing.h>

#include <Servo.h> // Include the Servo library

#define miligiro 700 

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
#define mid 109
#define min 80
#define max mid + (mid - min)


// Sensor Setup
NewPing sonarRight(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
NewPing sonarLeft(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

void forward() {
  analogWrite(ENABLE_PIN, 250);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
}

void stop() {
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENABLE_PIN, 0);
}

void giroIzquierda(){
  steeringServo.write(max);
  delay(500);
  forward();
  delay(miligiro);
  stop();
}

void giroDerecha(){
  steeringServo.write(min);
  delay(500);
  forward();
  delay(miligiro);
  stop();
}


void setup() {
  // Motor Control
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENABLE_PIN, 0);

  // Servo Control (120 mid)

  steeringServo.attach(SERVO_PIN);
  steeringServo.write(mid);
  delay(100);
  // Serial Communication
  Serial.begin(9600);

}

void loop() {
  while (sonarFront.ping_cm() == 0){
   forward();     
  }
  int diff = abs(sonarLeft.ping_cm() - sonarRight.ping_cm());
  if(diff > 10){
    if (sonarLeft.ping_cm() > sonarRight.ping_cm()){
      steeringServo.write(mid - 2);
    }
    if (sonarLeft.ping_cm() < sonarRight.ping_cm()){
      steeringServo.write(mid + 2);
    }
  }

  if (sonarFront.ping_cm() < 110) {
    stop();
    delay(1000);
    if (sonarLeft.ping_cm() > sonarRight.ping_cm()){
      giroIzquierda();
    }
    else (sonarLeft.ping_cm() < sonarRight.ping_cm()){
      giroDerecha();
    }
  }

  steeringServo.write(mid);
}
