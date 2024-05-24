#include <NewPing.h>
#include <Servo.h>

#define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     6  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

int enA = 3;
int in1 = 4;
int in2 = 5;

int SensorValue1[8];
char j, k;
long result1;
long result2;

NewPing sonar1(TRIGGER_PIN, 6, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(TRIGGER_PIN, 7, MAX_DISTANCE); // NewPing setup of pins and maximum distance.

Servo myservo;

void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
  myservo.attach(9);
  pinMode(enA, OUTPUT); 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);

  analogWrite(enA, 100);

}

void loop() {
    delay(50);    

    // for (j = 0; j < ; j++) {
    //   SensorValue1[j] = sonar1.ping_cm();
    //   delay(20);
    // }

    // result1= 0;
    // for (j = 0; j < 8; j++) {
    //   result1= result1+ SensorValue1[j]; // add them up
    // }
    // result1= result1/ 8 / US_ROUNDTRIP_CM;               // this is our averaged result
    // map(sonar1.ping_cm(), 0, 300, 70, 170);

    // digitalWrite(in1, LOW); 
    // digitalWrite(in2, HIGH); 
    // for (int i = 0; i < 50; i++) {
    int left = sonar1.ping_cm();
    if (left != 0){
    myservo.write(map(sonar1.ping_cm(), 80, 0, 75, 165));
    Serial.println(sonar1.ping_cm());
    }
      //   delay(50);
      // }
    // delay(3000);
    // digitalWrite(in1, LOW); 
    // digitalWrite(in2, LOW); 
    // delay(2000);
}