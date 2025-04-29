import serial
import csv
import os
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

puerto = 'COM3'  # Cambia según tu sistema
baudios = 9600

archivo = f'registro_pid_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

print("🕐 Esperando conexión con Arduino...")

# Esperar hasta que el puerto esté disponible
while True:
    try:
        ser = serial.Serial(puerto, baudios, timeout=1)
        break
    except:
        pass

with open(archivo, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tiempo', 'Velocidad', 'Setpoint', 'PWM', 'Error', 'KP', 'KI', 'KD'])

    print("⏺️ Grabando datos... Presiona Ctrl+C para detener.")
    tiempo_inicio = datetime.now()

    try:
        while True:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()

            if "DATA Vel:" in linea:
                partes = linea.split("|")
                try:
                    vel = float(partes[0].split(":")[1])
                    setpoint = float(partes[1].split(":")[1])
                    pwm = float(partes[2].split(":")[1])
                    kp = float(partes[4].split(":")[1])
                    ki = float(partes[5].split(":")[1])
                    kd = float(partes[6].split(":")[1])
                    error = abs(setpoint - vel)
                    tiempo_transcurrido = (datetime.now() - tiempo_inicio).total_seconds()

                    writer.writerow([tiempo_transcurrido, vel, setpoint, pwm, error, kp, ki, kd])

                    print(f"{tiempo_transcurrido:.2f}s | v={vel:.3f} | sp={setpoint:.3f} | pwm={pwm:.1f} | err={error:.4f}")
                except Exception as e:
                    print("❌ Error al procesar línea:", e)

    except KeyboardInterrupt:
        print("\n🛑 Grabación finalizada.")
        ser.close()

# ─────────── 📈 GRAFICAR TRAS LA GRABACIÓN ───────────

# Cargar los datos
df = pd.read_csv(archivo)

# Graficar
plt.figure(figsize=(10, 5))
plt.plot(df['Tiempo'], df['Velocidad'], label='Velocidad real', linewidth=2)
plt.plot(df['Tiempo'], df['Setpoint'], label='Setpoint (referencia)', linestyle='--', linewidth=2)
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (vueltas/s)')
plt.title('Respuesta del sistema al escalón')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
