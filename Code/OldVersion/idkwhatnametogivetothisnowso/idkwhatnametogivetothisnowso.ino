#include <Servo.h>
Servo servoMotor;
char buff[5];

// Motor Control Pins
#define IN1_PIN       9
#define IN2_PIN       8
#define ENABLE_PIN    10

// Servo Control
Servo steeringServo;
#define SERVO_PIN 11
#define mid 109
#define min 80
#define max mid + (mid - min)

void fw(sp) {
  analogWrite(ENABLE_PIN, sp);
  digitalWrite(IN1_PIN, HIGH);
  digitalWrite(IN2_PIN, LOW);
}

void bk(sp) {
  analogWrite(ENABLE_PIN, sp);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, HIGH);
}


void setup(){
  Serial.begin(115200);
  
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  analogWrite(ENABLE_PIN, 0);

  // Servo Control (120 mid)

  steeringServo.attach(SERVO_PIN);
  steeringServo.write(mid);
  delay(100);
}


void loop(){
  if(Serial.available() > 0) //If Arduino recieves a signal from the Pi
  {
    Serial.readBytes(buff,5);
    buff[4] = '\0'; //end of byte, so the Arduino know when the start and end of a command is
    int val = atoi(buff); //converts string to int

    if(val <= 1900 && val >= 1200) // Determines if the number is speed
    {
      if(val >= 1500){        
        fw(map(val-1500, 400, 100, 255, 200))

      } else {
        bw(map(1500-val, 300, 100, 255, 200))
      }
    }
    else if(val > 2000 && val <= 2180) // Determines if the number is an angle
    {                                                                                                       
      steeringServo.write(map(val - 2000, 35, 145, max, min)); // 2045 left, 2090 straight, 2135 right
    }
  }
}
