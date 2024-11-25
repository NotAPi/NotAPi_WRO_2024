// #include <NewPing.h>
// #include <PID_v1.h>
// #include <Servo.h> // Include the Servo library

// // Pin definitions
// #define TRIGGER_PIN1  3
// #define ECHO_PIN1     2
// #define TRIGGER_PIN2  5
// #define ECHO_PIN2     4
// #define TRIGGER_PIN3  7
// #define ECHO_PIN3     6
// #define MaxDistance   150

// // Motor Control Pins
// #define IN1_PIN       9
// #define IN2_PIN       8
// #define ENABLE_PIN    10

// // Servo Control
// Servo steeringServo;
// #define SERVO_PIN 11

// float Kp = 1;
// float Ki = 0.1;
// float Kd = 0;



// // Sensor Setup
// NewPing sonarRight(TRIGGER_PIN1, ECHO_PIN1, MaxDistance);
// NewPing sonarFront(TRIGGER_PIN2, ECHO_PIN2, MaxDistance);
// NewPing sonarLeft(TRIGGER_PIN3, ECHO_PIN3, MaxDistance);

// void forward(){
//   analogWrite(ENABLE_PIN, 150);
//   digitalWrite(IN1_PIN, HIGH);
//   digitalWrite(IN2_PIN, LOW);
// }

// void stop(){
//   analogWrite(ENABLE_PIN, 150);
//   digitalWrite(IN1_PIN, LOW);
//   digitalWrite(IN2_PIN, LOW);
// }

// void setup(){
//   // Motor Control
//   pinMode(IN1_PIN, OUTPUT);
//   pinMode(IN2_PIN, OUTPUT);
//   pinMode(ENABLE_PIN, OUTPUT);
//   stop();

//   // Servo Control (120 mid)
//   steeringServo.attach(SERVO_PIN);
//   steeringServo.write(120);

//   // Serial Communication
//   Serial.begin(9600); 

// }

// void loop() {
//   int distanceRight = sonarRight.ping_cm();
//   int distanceLeft = sonarLeft.ping_cm();

//   float error = distanceLeft - distanceRight;
//   integral += error;
//   float derivative = error - previousError;
//   float output = Kp * error + Ki * integral + Kd * derivative;

//   if (output > 0) {
//     analogWrite(ENABLE_PIN, 150);
//     digitalWrite(IN1_PIN, HIGH);
//     digitalWrite(IN2_PIN, LOW);
//     steeringServo.write(120 + output);
//   } else {
//     analogWrite(ENABLE_PIN, 150);
//     digitalWrite(IN1_PIN, LOW);
//     digitalWrite(IN2_PIN, HIGH);
//     steeringServo.write(120 + output);
//   }

//   previousError = error;

//   Serial.print("Distance Right: ");
//   Serial.print(distanceRight);
//   Serial.print(" cm, Distance Left: ");
//   Serial.print(distanceLeft);
//   Serial.print(" cm, Error: ");
//   Serial.print(error);
//   Serial.print(", Output: ");
//   Serial.println(output);

//   delay(100);
// }