/*
   .~~.   .~~.
  '. \ ' ' / .'
   .~ .~~~..~.
  : .~.'~'.~. :
 ~ (   ) (   ) ~
( : '~'.~.'~' : )
 ~ .~ (   ) ~. ~
  (  : '~' :  ) 
   '~ .~~~. ~'
       '~'
      NotAPi
*/


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

int centro = 108 ;// para que vaya recto 
int miligiroDERECHA = 950; // cuantos milisegundo está con el motor prendido en amboos giros
int miligiroIZQUIERDA = 650; // cuantos milisegundo está con el motor prendido en amboos giros

int distanciafreno = 70; // a que distancia en cm se para respecto la pared de delante xd
int distanciarevision = 200;

NewPing sonarRight(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
NewPing sonarLeft(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

void forward(int vel) {
  myservo.write(centro);
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
  forward(255);
  delay(miligiroIZQUIERDA);
  stop();
}

void giroDerecha(){
  myservo.write(80);
  delay(500);
  forward(255);
  delay(miligiroDERECHA);
  stop();
}

void atras(){
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENABLE_PIN, 255);  // Ajusta la velocidad al máximo inverso
  delay(5000);  // Pequeño retraso para aplicar el freno
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
  
  Serial.println(averageDistance);
  return averageDistance;
}

int getAverageDerechaDistance(int numReadings){
  int sum = 0;

  // Tomar múltiples lecturas y acumularlas
  for (int i = 0; i < numReadings; i++) {
    int distance = getDistance(sonarRight);
    sum += distance;
    delay(10); // Pequeño retraso entre lecturas para evitar interferencias
  }

  // Calcular el promedio de las lecturas
  int averageDistance = sum / numReadings;
  Serial.println(averageDistance);
  return averageDistance;
}

int getAverageIzquierdaDistance(int numReadings) {
  int sum = 0;
  
  // Tomar múltiples lecturas y acumularlas
  for (int i = 0; i < numReadings; i++) {
    int distance = getDistance(sonarLeft);
    sum += distance;
    delay(10); // Pequeño retraso entre lecturas para evitar interferencias
  }

  // Calcular el promedio de las lecturas
  int averageDistance = sum / numReadings;

  Serial.println(averageDistance);
  return averageDistance;
}

void loop() {
  int leftDistance = getDistance(sonarLeft);
  int frontDistance = getDistance(sonarFront);
  int rightDistance = getDistance(sonarRight);


 // Serial.print(leftDistance);
  Serial.print("  ");
  Serial.print(frontDistance);
  Serial.println("  ");
 // Serial.println(rightDistance);



  if ((frontDistance > distanciafreno) and (frontDistance > distanciarevision)) {
    myservo.write(centro);
    forward(200);
    }
  else if ((frontDistance < distanciarevision) and (frontDistance > distanciafreno)){
    stop();
    if (getAverageFrontDistance(50) < distanciarevision){    
      stop();
      delay(1000);
      int distanciahorizontal = getAverageDerechaDistance(50) + getAverageIzquierdaDistance(50);
      Serial.print("distanciahorizontal   ");
      Serial.println(distanciahorizontal);
      delay(1500);
      if (distanciahorizontal < 120 and distanciahorizontal > 40){
        int diferencia = getAverageDerechaDistance(50) - getAverageIzquierdaDistance(50);
        diferencia = constrain(diferencia, -20, 20);
        centro = centro + diferencia;
        Serial.print("CENTRO:  ");
        Serial.println(centro);
        myservo.write(centro);
        delay(1500);
      }
    }
  }
  else if (frontDistance < distanciafreno){
    forceStop();
    if (getAverageFrontDistance(50) < distanciafreno){    
      stop();
      delay(1000);
      if (leftDistance > rightDistance){
      giroIzquierda();
      }
      else if (leftDistance < rightDistance){
      giroDerecha();
      }
      else{
      atras();
      }
    }
    else{
      //no hace nada si la promedio es mayor a la distancai de freno ewyufweyfvyef
    }
  }


  // Other logic for controlling the robot based on sensor data
}
