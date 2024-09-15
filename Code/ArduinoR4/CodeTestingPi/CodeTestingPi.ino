#include <Servo.h> // Include the Servo library

#define IN1_PIN       9
#define IN2_PIN       8
#define ENABLE_PIN    10

// Servo Control
Servo steeringServo;
#define SERVO_PIN 11
#define mid 109
#define max 80
#define min mid + (mid - max) // 138

Servo servoMotor;
char buff[5]; //Var which will help us differentiate the start and end of information


void setup(){
  Serial.begin(115200); //Baud rate == 115200
  servoMotor.attach(SERVO_PIN); // Orange wire for servo motor
  servoMotor.write(mid); //Sets servo to be straight (90 degrees)
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENABLE_PIN, 0);
}


void loop(){
  if(Serial.available() > 0) //If Arduino recieves a signal from the Pi
  {
    Serial.readBytes(buff,5);
    buff[4] = '\0'; //end of byte, so the Arduino know when the start and end of a command is
    int val = atoi(buff); //converts string to int

    if(val <= 1900 && val >= 1200) // Determines if the number is speed
    {
      if (val > 1500) {
        analogWrite(ENABLE_PIN, 250);
        digitalWrite(IN1_PIN, HIGH);
        digitalWrite(IN2_PIN, LOW);
      } else if (val < 1500) {
        analogWrite(ENABLE_PIN, 250);
        digitalWrite(IN1_PIN, LOW);
        digitalWrite(IN2_PIN, HIGH);
        return;
      }
      else if(val > 2000 && val <= 2180) // Determines if the number is an angle
      {                         
        int angle = val - 2000;
        servoMotor.write(map(angle, 0, 180, min, max)); // 2045 left, 2090 straight, 2135 right
      }
    }
  }
}