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

int distanciaObjetivo = 40; // Distancia deseada en cm

// Crear un objeto NewPing
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

// Crear un filtro Kalman
SimpleKalmanFilter kalmanFilter(2, 2, 0.05);

void setup() {
  Serial.begin(9600);

  // Configurar los pines del motor como salida
  pinMode(EnA, OUTPUT);
  pinMode(In1, OUTPUT);
  pinMode(In2, OUTPUT);

  // Configurar el servo
  myServo.attach(SERVO_PIN);

  // Inicializar el motor a velocidad constante
  moverMotor(150); // Velocidad fija
}

void loop() {
  // Leer la distancia con el sensor de ultrasonidos
  unsigned int distance = sonar.ping_cm();

  // Aplicar el filtro de Kalman
  float filteredDistance = kalmanFilter.updateEstimate(distance);

  // Mostrar la distancia medida y la distancia filtrada
  Serial.print("  ");
  Serial.print(distance);
  Serial.print("  ");
  Serial.print(filteredDistance);

  // Calcular el desvío del servo en función de la distancia desde 40 cm
  int desviacion = (filteredDistance - distanciaObjetivo);
  int anguloServo = 120 + desviacion; // 120 es el ángulo central

  // Limitar el ángulo del servo a los valores mínimo y máximo (70-170 grados)
  if (anguloServo < 70) anguloServo = 70;
  if (anguloServo > 170) anguloServo = 170;

  // Mover el servo al ángulo calculado
  myServo.write(anguloServo);
  Serial.print("  ");
  Serial.println(anguloServo);

  delay(100); // Pequeño retraso entre lecturas
}

void moverMotor(int velocidad) {
  analogWrite(EnA, velocidad);
  digitalWrite(In1, HIGH);
  digitalWrite(In2, LOW);
}
