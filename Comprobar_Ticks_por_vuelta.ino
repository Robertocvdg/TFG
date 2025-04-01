volatile unsigned long ticks = 0;

void setup() {
  Serial.begin(9600);
  attachInterrupt(digitalPinToInterrupt(2), countTicks, RISING);
}

void loop() {
  delay(13000); // Espera 5 segundos para contar los ticks
  noInterrupts();
  Serial.print("Ticks: ");
  Serial.println(ticks);
  ticks = 0;
  interrupts();
}

void countTicks() {
  ticks++;
}
