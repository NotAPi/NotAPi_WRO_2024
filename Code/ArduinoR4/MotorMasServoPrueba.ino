/*

Por ahora solo funciona el servo
el motor no funciona, 
puede ser por falta de voltaje ya que no tenemos herramienta de mesura,
si no, el problema puede provenir de una mala pocición del cableado o una mala configuración de pines en el programa,
y si no es ninguno de esos, será un problema del códico. 

*/

int lapausa = 20; //regular el movimiento del servo (tiempo original 20)
int servoPin = 9;
int PinIN1 = 12;
int PinIN2 = 13;
int ENAPin = 11;

int ServMax = 150;
int ServMin = 40;
int ServCent = 85;

void setup() {
  Serial.begin(9600);

  pinMode(PinIN1, OUTPUT);
  pinMode(PinIN2, OUTPUT);
  analogWrite (ENAPin, 255);
  

  pinMode (servoPin, OUTPUT);
  digitalWrite(servoPin, HIGH);
  delay(1000);
}






void loop() {
  
  MotorForwards();

  moverServo(servoPin, 120);   // Movemos un poco el servomotor 
  delay(500);
  moverServo(servoPin, 0);   // Movemos un poco el servomotor 
  delay(500);
  moverServo(servoPin, 165);   // Movemos un poco el servomotor 
  delay(500); 

}







void moverServo(int pin, int angulo) {
  int tiempoPulso = map(angulo, 0, 180, 1000, 2000); // Mapear el ángulo al tiempo de pulso (1000 a 2000 microsegundos)
  digitalWrite(pin, HIGH); // Poner el pin en HIGH
  delayMicroseconds(tiempoPulso); // Esperar durante el tiempo del pulso
  digitalWrite(pin, LOW); // Poner el pin en LOW
  delayMicroseconds(20000 - tiempoPulso); // Esperar el resto del ciclo
}

void MotorForwards()
{
  digitalWrite (PinIN1, HIGH);
  digitalWrite (PinIN2, LOW);
}

void MotorBackwards()
{
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, HIGH);
}

void MotorStop()
{
  digitalWrite (PinIN1, LOW);
  digitalWrite (PinIN2, LOW);
}
