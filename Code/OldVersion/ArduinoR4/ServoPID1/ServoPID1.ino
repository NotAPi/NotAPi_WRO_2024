#include <NewPing.h>
#include <Servo.h>

// #define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
// #define ECHO_PIN     6  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 500 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

int enA = 3;
int in1 = 4;
int in2 = 5;
int angle;
float angleF;

NewPing sonar1(11, 6, MAX_3DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(12, 7, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar3(13, 8, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

Servo myservo;

void setup() {
  Serial.begin(115200);
  myservo.attach(9);
  pinMode(enA, OUTPUT); 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  analogWrite(enA, 100);

  digitalWrite(in1, LOW); 
  digitalWrite(in2, LOW); 
}

void loop() {
  delay(50);    

  digitalWrite(in1, LOW); 
  digitalWrite(in2, HIGH); 

  int left = sonar1.ping_cm();
  int right = sonar2.ping_cm();
  
  
  Serial.print(left);
  Serial.print(" ");
  Serial.print(right);
  Serial.print(" ");
  // Serial.print(sonar3.ping_cm());
  // Serial.print(" ");

  
  if (left > right){
    angleF = float(right) *100 / left;
    int angle = (int)angleF;
    delay(10);
    myservo.write(map(angle, 100, 0, 75, 120));
    // Serial.println(sonar1.ping_cm());
    Serial.print(angle);
    Serial.println("     1");

  }
  if (left < right){
    angleF = float(left) *100 / right;
    int angle = (int)angleF;
    delay(10);
    myservo.write(map(angle, 0, 100, 120, 165));
    Serial.print(angle);
    Serial.println("     2");
  }

}