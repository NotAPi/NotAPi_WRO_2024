#include <NewPing.h>
#include <Servo.h>
// servo 75 → left, 165 is right
// #define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
// #define ECHO_PIN     6  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

int enA = 3;
int in1 = 4;
int in2 = 5;
int angle;
float angleF;

NewPing sonar1(11, 6, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(12, 7, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar3(13, 8, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

Servo myservo;

int sentido = 0; //horario = 0, antiorario = 1

void setup() {
  Serial.begin(115200);
  myservo.attach(9);
  pinMode(enA, OUTPUT); 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  analogWrite(enA, 100);

  digitalWrite(in1, LOW); 
  digitalWrite(in2, LOW); 
  myservo.write(120);
  // delay(100);
  // myservo.write(165);

}

  int Left(){
    int medida = sonar1.ping_cm();
    if(medida == 0){
    medida = 300;
    }
    return medida;
  }

  int Right(){
    int medida = sonar2.ping_cm();
    if(medida == 0){
    medida = 300;
    }
    return medida;
  }

  int Center(){
    int medida = sonar3.ping_cm();
    if(medida == 0){
    medida = 300;
    }
    return medida;
  }

 


void loop() {
  delay(50);    

  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH); 

  int left = Left();
  int right = Right();
  int front = Center();  
  

  if (front < 80 && front != 0 ) {
    // Stop the car
    digitalWrite(in1, LOW); 
    digitalWrite(in2, LOW); 
    delay(1000);
    // Compare the two sides
    if (Left() > Right() && (Left()<299 || Right()<299) ) {
      myservo.write(75); //left
      sentido = 1; // antihorario
          delay(1000);
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH);
  delay(975);
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);
  delay(5);
  myservo.write(120);
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH);
  delay(1000);
    } else if (Right() > Left() && (Left()<299 || Right()<299)) {
      myservo.write(165); //right
      sentido = 0; // horario
          delay(1000);
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH);
  delay(975);
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW);
  delay(5);
  myservo.write(120);
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH);
  delay(1000);
    }

if( sentido = 0){ // horario
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH); 

    if(Left() < 40){
      myservo.write(160);
    }
    if(Left() > 40){
      myservo.write(70);
    }

}

if( sentido = 1){ // horario
  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH); 

    if(Right() < 40){
      myservo.write(70);
    }
    if(Right() > 40){
      myservo.write(160);
    }

}





  }

}