import sqlite3
import pandas as pd
import os

BASE_PATH = r"C:\Users\luism\OneDrive\Proyecto\FINANZAS_PINTOSANO"
BASE_DATOS = os.path.join(BASE_PATH, "finanzas.db")

conn = sqlite3.connect(BASE_DATOS)
df = pd.read_sql_query("SELECT * FROM caja_diaria", conn)

if df.empty:
    exit()

promedio = df["ventas_totales"].mean()
desvio = df["ventas_totales"].std()

limite_inferior = promedio - desvio

alertas = df[df["ventas_totales"] < limite_inferior]

if not alertas.empty:
    print("⚠️ ALERTA: Ventas anormalmente bajas detectadas")
    print(alertas[["fecha","ventas_totales"]])
else:
    print("Sin anomalías detectadas.")
