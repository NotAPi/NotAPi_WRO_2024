#include <NewPing.h>
#include <Servo.h>

#define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

int enA = 3;
int in1 = 4;
int in2 = 5;

int SensorValue1[8];
char j, k;
long result1;
long result2;

NewPing sonar1(11, 6, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(12, 7, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar3(13, 8, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

Servo myservo;

void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  myservo.attach(9);
  pinMode(enA, OUTPUT); 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  analogWrite(enA, 128);


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



    Serial.print(Left());
    Serial.print(" ");
    Serial.print(Right());
    Serial.print(" ");
    Serial.println(Left());

 // digitalWrite(in1, HIGH); 
  //digitalWrite(in2, LOW); 
  
  
}
