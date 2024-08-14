#include <NewPing.h>
#include <Servo.h>
// Define the pins for the ultrasonic sensor
#define TRIGGER_L 3
#define ECHO_L 2

#define TRIGGER_F 5
#define ECHO_F 4

#define TRIGGER_R 7
#define ECHO_R 6

#define MAX_DISTANCE 150 // Maximum distance to ping for (in centimeters)

#define BUTTON_PIN 12

#define EnA 10
#define In1 9
#define In2 8

Servo myservo;

// Create sonar objects
NewPing sonarL(TRIGGER_L, ECHO_L, MAX_DISTANCE);
NewPing sonarF(TRIGGER_F, ECHO_F, MAX_DISTANCE);
NewPing sonarR(TRIGGER_R, ECHO_R, MAX_DISTANCE);

int distanceL = sonarL.ping_cm();
int distanceF = sonarF.ping_cm();
int distanceR = sonarR.ping_cm();

int distanceS = (distanceL + distanceR) / 2;

int mode = 1; // 1 (R), 2 (L)

void setup()
{
  pinMode(EnA, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);

  Serial.begin(9600);
  // pinMode(BUTTON_PIN, INPUT_PULLUP); // Set the button pin as input with internal pull-up resistor
  myservo.attach(11);
  // Wait for button press to set the mode
  // while (mode == 0) {
  //   if (digitalRead(BUTTON_PIN) == LOW) {
  //     delay(50); // Debounce delay
  //     if (digitalRead(BUTTON_PIN) == LOW) {
  //       mode = 1;
  //       delay(1000); // Wait for 1 second to check for a second press
  //       if (digitalRead(BUTTON_PIN) == LOW) {
  //         delay(50); // Debounce delay
  //         if (digitalRead(BUTTON_PIN) == LOW) {
  //           mode = 2;
  //         }
  //       }
  //     }
  //   }
  // }
}
void loop()
{
  // int distanceL = sonarL.ping_cm();
  // int distanceF = sonarF.ping_cm();
  // int distanceR = sonarR.ping_cm();
  
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
  analogWrite(EnA, 150);

  // // servo 120 mid
  // if (distanceR > distanceS)
  //   {
  //     myservo.write(140);
  //   }

  // if (distanceR < distanceS)
  //   {
  //     myservo.write(100);
  //   } 
    // Print the distance to the Serial Monitor
        // Serial.print(distanceL);
        // Serial.print(" ");
        // Serial.print(distanceF);
        // Serial.print(" ");
        // Serial.print(distanceR);
        // Serial.print(" ");
  Serial.println(distanceL + distanceR);
  delay(25);
}