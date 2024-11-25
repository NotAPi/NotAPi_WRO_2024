#include <NewPing.h>
#include <SimpleKalmanFilter.h>
#include <Servo.h>

Servo myServo;

// Definiciones para el sensor de ultrasonidos
#define TRIGGER_PIN  7  // Pin del trigger del sensor
#define ECHO_PIN     6  // Pin del echo del sensor
#define MAX_DISTANCE 200 // Distancia máxima en cm

// Pines del motor y servo
#define EnA 10
#define In1 9
#define In2 8
#define SERVO_PIN 11

int distanciaObjetivo = 40;
int servoMin = 70;  // Límite izquierdo del servo
int servoMax = 170; // Límite derecho del servo

// Crear un objeto NewPing
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

// Crear un filtro Kalman
SimpleKalmanFilter kalmanFilter(2, 2, 0.01);

void setup() {
  Serial.begin(9600);

  // Configurar los pines del motor como salida
  pinMode(EnA, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);

  // Configurar el servo
  myServo.attach(SERVO_PIN);

  // Inicialmente posicionar el sensor en el centro de su rango
  myServo.write(120); // Posición central
}

void loop() {
  for (int angle = servoMin; angle <= servoMax; angle += 10) {
    // Mover el servo al ángulo actual
    myServo.write(angle);
    delay(500); // Esperar a que el servo se estabilice

    // Leer la distancia con el sensor de ultrasonidos
    unsigned int distance = sonar.ping_cm();

    // Aplicar el filtro de Kalman
    float filteredDistance = kalmanFilter.updateEstimate(distance);

    // Mostrar la distancia medida y la distancia filtrada
    Serial.print("Ángulo: ");
    Serial.print(angle);
    Serial.print(" | Distancia medida: ");
    Serial.print(distance);
    Serial.print(" cm | Distancia filtrada: ");
    Serial.println(filteredDistance);

    // Controlar el motor para seguir la pared a 40 cm
    if (filteredDistance < (distanciaObjetivo - 5)) {
      // Si estamos demasiado cerca de la pared, reducir la velocidad del motor
      moverMotor(100); // Velocidad reducida
    } 
    else if (filteredDistance > (distanciaObjetivo + 5)) {
      // Si estamos demasiado lejos de la pared, aumentar la velocidad del motor
      moverMotor(200); // Velocidad aumentada
    } 
    else {
      // Si estamos a la distancia correcta, mantener velocidad media
      moverMotor(150); // Velocidad media
    }

    delay(100); // Pequeño retraso entre lecturas
  }
}

void moverMotor(int velocidad) {
  analogWrite(EnA, velocidad);
  if (velocidad > 0) {
    digitalWrite(In1, HIGH);
    digitalWrite(In2, LOW);
  } else {
    digitalWrite(In1, LOW);
    digitalWrite(In2, HIGH);
  }
}
