#include <NewPing.h>

#define TRIGGER_PIN  2  // Arduino pin tied to trigger pin on the ultrasonic sensor.
#define ECHO_PIN     6  // Arduino pin tied to echo pin on the ultrasonic sensor.
#define MAX_DISTANCE 300 // Maximum distance we want to ping for (in centimeters). Maximum sensor distance is rated at 400-500cm.

int SensorValue1[8];
char j, k;
long result1;
long result2;

NewPing sonar1(TRIGGER_PIN, 6, MAX_DISTANCE); // NewPing setup of pins and maximum distance.
NewPing sonar2(TRIGGER_PIN, 7, MAX_DISTANCE); // NewPing setup of pins and maximum distance.


void setup() {
  Serial.begin(115200); // Open serial monitor at 115200 baud to see ping results.
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
  Serial.println(sonar1.ping_cm());
}