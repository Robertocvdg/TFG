import serial
import csv
import os
import subprocess
from datetime import datetime

puerto = 'COM3'  # Cambia si es necesario
baudios = 9600

archivo = f'registro_pid_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

print("🕐 Esperando datos desde Arduino...")

# Intentar conectar al puerto serie
while True:
    try:
        ser = serial.Serial(puerto, baudios, timeout=1)
        break
    except:
        pass

with open(archivo, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tiempo', 'Velocidad', 'Setpoint', 'PWM', 'Error', 'KP', 'KI', 'KD'])

    print("⏺️ Conectado. Grabando datos... Presiona Ctrl+C para detener.")
    tiempo_inicio = datetime.now()

    try:
        while True:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            print("DEBUG:", linea)

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

                    print(f"t={tiempo_transcurrido:.1f}s | v={vel:.3f} | sp={setpoint:.3f} | pwm={pwm:.1f} | err={error:.4f} | KP={kp} KI={ki} KD={kd}")
                except Exception as e:
                    print("❌ Error al procesar línea:", e)
    except KeyboardInterrupt:
        print("\n🛑 Grabación terminada.")
        ser.close()

        try:
            os.startfile(archivo)  # Para Windows
        except AttributeError:
            try:
                subprocess.call(['xdg-open', archivo])  # Para Linux
            except:
                print(f"📁 Archivo guardado en: {archivo}")
