#include <NewPing.h>

#define TRIGGER_PIN1  3
#define ECHO_PIN1     2
#define TRIGGER_PIN2  5
#define ECHO_PIN2     4
#define TRIGGER_PIN3  7
#define ECHO_PIN3     6
#define MaxDistance   150

NewPing sonarLeft(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
NewPing sonarRight(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.print(" L");
  Serial.print(sonarLeft.ping_cm());
  Serial.print(" F");
  Serial.print(sonarFront.ping_cm());
  Serial.print(" R");
  Serial.println(sonarRight.ping_cm());
  delay(100);
}
