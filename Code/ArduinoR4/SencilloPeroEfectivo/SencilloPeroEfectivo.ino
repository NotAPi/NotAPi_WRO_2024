#include <NewPing.h>
#include <Servo.h> // Include the Servo library

// Pin definitions
#define TRIGGER_PIN1  3
#define ECHO_PIN1     2
#define TRIGGER_PIN2  5
#define ECHO_PIN2     4
#define TRIGGER_PIN3  7
#define ECHO_PIN3     6
int MaxDistance = 300;

// Motor Control Pins
#define IN1_PIN       9
#define IN2_PIN       8
#define ENABLE_PIN    10

// Servo Control
Servo myservo;
#define SERVO_PIN 11

int centro = 110;
int miligiro = 500;
int distanciafreno = 50;

NewPing sonarRight(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
NewPing sonarLeft(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

void forward(int vel) {
  analogWrite(ENABLE_PIN, vel);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
}

void stop() {
  analogWrite(ENABLE_PIN, 150);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
}

void forceStop() {
  // Breve inversión del motor para frenar el robot
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

  myservo.attach(SERVO_PIN);

  Serial.begin(9600);

  myservo.write(centro);

  stop();
}
//192.168.217.95
int getDistance(NewPing &sonar) {
  int distance = sonar.ping_cm();
  if (distance == 0) {
    distance = MaxDistance;
  }
  return distance;
}

void giroIzquierda(){
  myservo.write(160);
  delay(500);
  forward(250);
  delay(miligiro);
  stop();
}

void giroDerecha(){
  myservo.write(80);
  delay(500);
  forward(250);
  delay(miligiro);
  stop();
}

int getAverageFrontDistance(int numReadings) {
  int sum = 0;
  
  // Tomar múltiples lecturas y acumularlas
  for (int i = 0; i < numReadings; i++) {
    int distance = getDistance(sonarFront);
    sum += distance;
    delay(10); // Pequeño retraso entre lecturas para evitar interferencias
  }

  // Calcular el promedio de las lecturas
  int averageDistance = sum / numReadings;
  
  return averageDistance;
}

void loop() {
  int leftDistance = getDistance(sonarLeft);
  int frontDistance = getDistance(sonarFront);
  int rightDistance = getDistance(sonarRight);

  Serial.print(leftDistance);
  Serial.print("  ");
  Serial.print(frontDistance);
  Serial.print("  ");
  Serial.println(rightDistance);



  if (frontDistance > distanciafreno) {
    if (getAverageFrontDistance(5) > distanciafreno){
    myservo.write(centro);
    delay(10);
    forward(150);
    }
  }
  else if (frontDistance < 100) {
    forceStop();
    stop();
    delay(1000);
    if (leftDistance > rightDistance){
      giroIzquierda();
    }
    else if (leftDistance < rightDistance){
      giroDerecha();
    }
    else{
      giroIzquierda();
    }
  }


  // Other logic for controlling the robot based on sensor data
}
