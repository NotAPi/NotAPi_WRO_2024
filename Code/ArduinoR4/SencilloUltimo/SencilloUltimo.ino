/*
TODO:
- desencayar y reposicionar:
  - last time giro too long
  - if pingFront equal for x time


*/

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
#define mid 109
#define max 80
#define min mid + (mid - max)

int centro = mid ;// para que vaya recto 
int miligiroDERECHA = 620; // cuantos milisegundo está con el motor prendido en amboos giros
int miligiroIZQUIERDA = 600; // cuantos milisegundo está con el motor prendido en amboos giros
int miligiroREPO = 500;
int distanciafreno = 40; // a que distancia en cm se para respecto la pared de delante xd

int giros = 0;
int gR = 0;
int gL = 0;
int tiempoREPO = 15000; // (milis)

unsigned long lastTurnTime = 0;

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
}  // Perform the repositioning logic here



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
  // if (giros = 0){
  //   gL = 1;
  // }
   
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENABLE_PIN, 255);
  delay(400); 

  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENABLE_PIN, 0);
  delay(500); 

  myservo.write(min);
  delay(450);
  forward(255);
  delay(miligiroIZQUIERDA);
  giros++;
  stop();
  lastTurnTime = millis(); // Update the last turn time
}

void giroDerecha(){
  // if (giros = 0){
  //   gR = 1;
  // }
  
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENABLE_PIN, 255);
  delay(400); 

  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENABLE_PIN, 0);
  delay(500); 


  myservo.write(max);
  delay(450);
  forward(255);
  delay(miligiroDERECHA);
  giros++;
  stop();
  lastTurnTime = millis(); // Update the last turn time

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
  
  return averageDistance;
}

void reposition() {
  lastTurnTime = millis(); // Update the last turn time
  stop();

  // if (gR == 1){
  //   myservo.write(min);
  // }else if (gL == 1){
  //   myservo.write(max);
  // }

  myservo.write(90);
  delay(800);
  lastTurnTime = millis(); // Update the last turn time

  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
  analogWrite(ENABLE_PIN, 255); 
  delay(miligiroREPO);  // Pequeño retraso para aplicar el freno
  stop();
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

  if (giros < 12) {
    if (frontDistance > distanciafreno) {
      myservo.write(centro);
      forward(200);
    } else if (frontDistance < distanciafreno) {
      forceStop();
      if (getAverageFrontDistance(50) < distanciafreno) {
        stop();
        delay(1000);
        if (leftDistance > rightDistance) {
          giroIzquierda();
        } else if (leftDistance < rightDistance) {
          giroDerecha();
        } else {
          atras();
        }
      }
    }

    // Check if 20 seconds have passed since the last turn
    if (millis() - lastTurnTime >= tiempoREPO) {
      reposition();
    }
  } else {
    // Continue moving forward until front distance is 160 cm
    if (frontDistance < 160) {
      stop();
    } else {
      myservo.write(centro);
      forward(200);
    }
  }

  Serial.println(giros);
}