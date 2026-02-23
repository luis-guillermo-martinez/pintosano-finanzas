import sqlite3
import pandas as pd
import os

BASE_PATH = r"C:\Users\luism\OneDrive\Proyecto\FINANZAS_PINTOSANO"
BASE_DATOS = os.path.join(BASE_PATH, "finanzas.db")

conn = sqlite3.connect(BASE_DATOS)

df = pd.read_sql_query("SELECT * FROM caja_diaria", conn)

if df.empty:
    print("No hay datos.")
    input("Presioná Enter para cerrar...")
    exit()

df["fecha"] = pd.to_datetime(df["fecha"])
df["mes"] = df["fecha"].dt.to_period("M")

resumen = df.groupby("mes").agg({
    "ventas_totales": "sum",
    "ventas_efectivo": "sum",
    "ventas_digital": "sum",
    "diferencia": "sum"
})

print("\n===== RESUMEN MENSUAL =====\n")
print(resumen)

input("\nPresioná Enter para cerrar...")
