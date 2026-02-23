import streamlit as st
import sqlite3
import pandas as pd
import os

BASE_PATH = r"C:\Users\luism\OneDrive\Proyecto\FINANZAS_PINTOSANO"
BASE_DATOS = os.path.join(BASE_PATH, "finanzas.db")

conn = sqlite3.connect(BASE_DATOS)
df = pd.read_sql_query("SELECT * FROM caja_diaria ORDER BY fecha", conn)

st.title("Dashboard Financiero Pintosano")

if df.empty:
    st.warning("No hay datos cargados.")
    st.stop()

df["fecha"] = pd.to_datetime(df["fecha"])

st.metric("Total Ventas", f"${df['ventas_totales'].sum():,.2f}")
st.metric("Total Efectivo", f"${df['ventas_efectivo'].sum():,.2f}")
st.metric("Total Digital", f"${df['ventas_digital'].sum():,.2f}")

st.line_chart(df.set_index("fecha")[["ventas_totales","ventas_efectivo","ventas_digital"]])
