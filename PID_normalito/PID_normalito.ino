const int PIN_DIR = 8;
const int PIN_PWM = 9;

const int ENCODER1_A = 3;
volatile unsigned long encoderTicks = 0;

const unsigned long TICKS_POR_VUELTA = 105325UL;

unsigned long lastTime = 0;
unsigned long lastTicks = 0;
unsigned long tiempoInicio = 0;

float setpoint = 0.0;
float input = 0;
float output = 0;

float kp = 150;
float ki = 450;
float kd = 0.05;

float error = 0;
float lastError = 0;
float integral = 0;

bool pidActivo = false;
bool setpointCambiado = false;
bool direccion = HIGH;

float errorAcumulado = 0;
int muestrasError = 0;
unsigned long lastDiagTime = 0;

void setup() {
  Serial.begin(9600);
  pinMode(PIN_DIR, OUTPUT);
  pinMode(PIN_PWM, OUTPUT);

  pinMode(ENCODER1_A, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(ENCODER1_A), encoderTick, RISING);

  digitalWrite(PIN_DIR, direccion);
  analogWrite(PIN_PWM, 0);

  tiempoInicio = millis();
  Serial.println("Esperando 10 segundos antes de arrancar el PID...");
}

void loop() {
  if (!setpointCambiado && millis() - tiempoInicio >= 1000) {
    setpoint = 0.5;
    pidActivo = true;
    setpointCambiado = true;
    Serial.println("PID ACTIVADO - Setpoint cambiado a 0.25 vueltas/s");
  }

  unsigned long currentTime = millis();
  if (currentTime - lastTime >= 100) {  // ← Cambio a 0.1 segundos
    unsigned long currentTicks = encoderTicks;
    unsigned long deltaTicks = currentTicks - lastTicks;
    float deltaTime = (currentTime - lastTime) / 1000.0;

    input = deltaTicks / deltaTime / TICKS_POR_VUELTA;

    if (pidActivo) {
      error = setpoint - input;
      integral += error * deltaTime;
      float derivative = (error - lastError) / deltaTime;

      output = kp * error + ki * integral + kd * derivative;
      int pwmValue = constrain(output, 0, 255);
      analogWrite(PIN_PWM, pwmValue);

      lastError = error;

      errorAcumulado += abs(error);
      muestrasError++;
    } else {
      analogWrite(PIN_PWM, 0);
    }

    lastTime = currentTime;
    lastTicks = currentTicks;

    Serial.print("DATA Vel: ");
    Serial.print(input, 4);
    Serial.print(" | Setpoint: ");
    Serial.print(setpoint, 4);
    Serial.print(" | PWM: ");
    Serial.print(output);
    Serial.print(" | DIR: ");
    Serial.print(direccion == HIGH ? "adelante" : "atras");
    Serial.print(" | KP: "); Serial.print(kp);
    Serial.print(" | KI: "); Serial.print(ki);
    Serial.print(" | KD: "); Serial.println(kd);
  }

  if (millis() - lastDiagTime >= 5000) {
    if (muestrasError > 0) {
      float errorPromedio = errorAcumulado / muestrasError;
      Serial.print("Error promedio últimos 5s: ");
      Serial.println(errorPromedio, 4);
    }
    errorAcumulado = 0;
    muestrasError = 0;
    lastDiagTime = millis();
  }
}

void encoderTick() {
  encoderTicks++;
}
