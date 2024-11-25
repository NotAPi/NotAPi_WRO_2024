// Conexiones del driver L293D para un motor DC
int enA = 5;
int in1 = 6;
int in2 = 7;

void setup() {
  // Colocando los pines en modo salida
  pinMode(enA, OUTPUT); 
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT); 
}

void loop() {
  // Iniciamos con el motor detenido
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  delay(2000);
  
  // Máxima velocidad del motor 
  analogWrite(enA, 255);
  
  // Encendemos el motor
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW); 
  delay(2000);
  
  // Invertimos el sentido del giro del motor
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);  
  delay(2000);
  
  // Apagamos el motor
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  delay(2000);
  
  // Turn on motors
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);
    
  // Aumenta la velocidad de cero a máximo
  for (int i = 0; i < 256; i=i+1) {
    analogWrite(enA, i);    
    delay(50);
  }
  
  // Disminuye la velocidad de máximo a cero
  for (int i = 255; i >= 0; i=i-1) {
    analogWrite(enA, i);  
    delay(50);
  }
  
}