#include <Servo.h> //De 70 a 170 maso, el medio es 120 
Servo myservo; 

// Conexiones del driver para un motor DC
int enA = 3;
int in1 = 4;
int in2 = 5;

void setup() {
  // Colocando los pines en modo salida
  Serial.begin(9600);
  pinMode(enA, OUTPUT); 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  analogWrite(enA, 100);
  
  myservo.attach(9); 
  myservo.write(120);   
}

void loop() {


  myservo.write(120);  
  digitalWrite(in1, HIGH); 
  digitalWrite(in2, LOW); 
  delay(2000);

  myservo.write(70);  
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH); 
  delay(2000);

  myservo.write(170);  
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW); 
  delay(2000);

}