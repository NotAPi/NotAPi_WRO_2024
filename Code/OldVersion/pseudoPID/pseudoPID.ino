//Versión Alpha
#include <NewPing.h>
#include <Servo.h>

// Constants for ultrasonic sensors
#define TRIGGER_PIN_LEFT 11
#define ECHO_PIN_LEFT 6
#define TRIGGER_PIN_RIGHT 12
#define ECHO_PIN_RIGHT 7
#define TRIGGER_PIN_FRONT 13
#define ECHO_PIN_FRONT 8
#define MAX_DISTANCE 300 // Maximum distance to measure (cm)

// Motor and Servo pins
#define MOTOR_PIN1 5
#define MOTOR_PIN2 4
#define ENABLE_PIN 3
#define SERVO_PIN 9

// PID constants
float kp = 1.0, ki = 0.02, kd = 0.1;
float error, previous_error = 0, integral = 0, derivative;
float correction;

// Target distance from the wall (in cm)
const float targetDistance = 30.0;

// Initialize ultrasonic sensors
NewPing sonarLeft(TRIGGER_PIN_LEFT, ECHO_PIN_LEFT, MAX_DISTANCE);
NewPing sonarRight(TRIGGER_PIN_RIGHT, ECHO_PIN_RIGHT, MAX_DISTANCE);
NewPing sonarFront(TRIGGER_PIN_FRONT, ECHO_PIN_FRONT, MAX_DISTANCE);

// Initialize servo motor
Servo steeringServo;

void setup() {
  pinMode(MOTOR_PIN1, OUTPUT);
  pinMode(MOTOR_PIN2, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);

  steeringServo.attach(SERVO_PIN);
  
  Serial.begin(9600);
}

void loop() {
  // Measure distances
  float distanceLeft = sonarLeft.ping_cm();
  float distanceRight = sonarRight.ping_cm();
  float distanceFront = sonarFront.ping_cm();

  // Check for corners or obstacles
  if (distanceFront < targetDistance) {
    // Stop or perform a turn to avoid the obstacle
    avoidObstacle();
  } else {
    // Calculate PID error terms for wall following
    error = distanceLeft - distanceRight;
    integral += error;
    derivative = error - previous_error;
    correction = kp * error + ki * integral + kd * derivative;

    // Map correction to servo angle (assuming 90 is straight)
    int servoAngle = constrain(map(correction, -30, 30, 65, 165), 65, 165);
    steeringServo.write(servoAngle);

    // Set motor speed
    int motorSpeed = 100; // Adjust speed as needed
    analogWrite(ENABLE_PIN, motorSpeed);
    
    // Set motor direction (forward)
    digitalWrite(MOTOR_PIN1, HIGH);
    digitalWrite(MOTOR_PIN2, LOW);

    // Update previous error
    previous_error = error;
  }

  delay(50);
}

void avoidObstacle() {
  // Stop the motors
  analogWrite(ENABLE_PIN, 0);
  digitalWrite(MOTOR_PIN1, LOW);
  digitalWrite(MOTOR_PIN2, LOW);

  // Turn the robot (for example, 90 degrees to the right)
  steeringServo.write(165); // Full right
  delay(500); // Wait for the turn to complete
  analogWrite(ENABLE_PIN, 150); // Move forward
  delay(500); // Move a bit forward to clear the obstacle
  analogWrite(ENABLE_PIN, 0); // Stop again

  // Reset servo to straight
  steeringServo.write(90);
}
