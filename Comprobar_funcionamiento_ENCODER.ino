volatile int contador = 0;  // Variable global para contar pulsos

void setup() {
  Serial.begin(9600);  // Inicializa el puerto serie
  pinMode(2, INPUT_PULLUP);  // Canal A con pull-up interno
  pinMode(3, INPUT_PULLUP);  // Canal B con pull-up interno

  // Configurar interrupciones
  attachInterrupt(digitalPinToInterrupt(2), cambioEncoder, CHANGE);
}

void loop() {
  Serial.println(contador);  // Muestra el conteo en el monitor serie
  delay(200);
}

void cambioEncoder() {
  if (digitalRead(2) == digitalRead(3)) {
    contador++;  // Sentido horario
  } else {
    contador--;  // Sentido antihorario
  }
}
