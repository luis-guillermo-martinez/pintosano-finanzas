import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_PATH = r"C:\Users\luism\OneDrive\Proyecto\FINANZAS_PINTOSANO"
BASE_DATOS = os.path.join(BASE_PATH, "finanzas.db")

conn = sqlite3.connect(BASE_DATOS)

df = pd.read_sql_query("SELECT * FROM caja_diaria ORDER BY fecha", conn)

if df.empty:
    print("No hay datos para mostrar.")
    input("Presioná Enter para cerrar...")
    exit()

df["fecha"] = pd.to_datetime(df["fecha"])

promedio = df["ventas_totales"].mean()

plt.figure()

plt.plot(df["fecha"], df["ventas_totales"])
plt.plot(df["fecha"], df["ventas_efectivo"])
plt.plot(df["fecha"], df["ventas_digital"])

plt.axhline(promedio)

plt.title("Evolución de Ventas")
plt.xlabel("Fecha")
plt.ylabel("Monto")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nPromedio general:", round(promedio, 2))

input("\nPresioná Enter para cerrar...")
