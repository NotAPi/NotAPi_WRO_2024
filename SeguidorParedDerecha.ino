#include <NewPing.h>
#include <Servo.h>

#define TRIG_PIN 7
#define ECHO_PIN 6
#define MAX_DISTANCE 200
#define SERVO_PIN 11
#define IN1 9
#define IN2 8
#define ENA 10

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);
Servo myServo;

float Kp = -1.0; // Ganancia proporcional (ajusta este valor para mejorar la respuesta)

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  myServo.attach(SERVO_PIN);
  myServo.write(120); // Servo centrado (mirando hacia adelante)

  Serial.begin(9600);
}

void loop() {
  int distance = sonar.ping_cm(); // Mide la distancia a la pared
  int desiredDistance = 20; // Queremos mantenernos a 20 cm de la pared

  // Calcula el error
  float error = distance - desiredDistance;

  // Calcula la salida proporcional
  float output = Kp * error;

  Serial.print("Distancia: ");
  Serial.print(distance);
  Serial.print(" | Error: ");
  Serial.print(error);
  Serial.print(" | Salida: ");
  Serial.println(output);

  // Control del motor (siempre hacia adelante)
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  analogWrite(ENA, 150);  // Velocidad del motor

  // Ajusta el ángulo del servo según la salida
  int servoAngle = 120 - output; // 120 es la posición centrada del servo
  servoAngle = constrain(servoAngle, 75, 165); // Limitar el ángulo entre 75 y 165 grados
  myServo.write(servoAngle);

  delay(100); // Pequeño retraso para permitir mediciones estables
}
