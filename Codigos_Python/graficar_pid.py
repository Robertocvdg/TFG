import pandas as pd
import matplotlib.pyplot as plt

archivo = input("Nombre del archivo CSV (ej: registro_pid_20250422_1530.csv): ")

# Cargar los datos
df = pd.read_csv(archivo)

# Graficar velocidad vs setpoint
plt.figure()
plt.plot(df['Tiempo'], df['Velocidad'], label='Velocidad real')
plt.plot(df['Tiempo'], df['Setpoint'], label='Setpoint', linestyle='--')
plt.xlabel('Tiempo (s)')
plt.ylabel('Vueltas/s')
plt.title('Velocidad vs Setpoint')
plt.legend()
plt.grid()

# Graficar PWM
plt.figure()
plt.plot(df['Tiempo'], df['PWM'], label='PWM', color='orange')
plt.xlabel('Tiempo (s)')
plt.ylabel('PWM')
plt.title('PWM aplicado')
plt.grid()

# Graficar error
plt.figure()
plt.plot(df['Tiempo'], df['Error'], label='Error', color='red')
plt.xlabel('Tiempo (s)')
plt.ylabel('Error absoluto (v/s)')
plt.title('Error de seguimiento')
plt.grid()

plt.show()
