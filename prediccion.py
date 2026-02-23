import sqlite3
import pandas as pd
import numpy as np
import os

BASE_PATH = r"C:\Users\luism\OneDrive\Proyecto\FINANZAS_PINTOSANO"
BASE_DATOS = os.path.join(BASE_PATH, "finanzas.db")

conn = sqlite3.connect(BASE_DATOS)
df = pd.read_sql_query("SELECT * FROM caja_diaria ORDER BY fecha", conn)

if len(df) < 2:
    print("Necesitás más datos para predicción.")
    exit()

df["fecha"] = pd.to_datetime(df["fecha"])
df["dias"] = (df["fecha"] - df["fecha"].min()).dt.days

x = df["dias"]
y = df["ventas_totales"]

coef = np.polyfit(x, y, 1)
modelo = np.poly1d(coef)

proximo_dia = x.max() + 1
prediccion = modelo(proximo_dia)

print("Predicción próxima venta estimada:", round(prediccion,2))
