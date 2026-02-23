import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Pintosano Finanzas", layout="wide")

BASE_DATOS = "finanzas.db"

if not os.path.exists(BASE_DATOS):
    st.warning("Base de datos no encontrada.")
    st.stop()

conn = sqlite3.connect(BASE_DATOS)
df = pd.read_sql_query("SELECT * FROM caja_diaria ORDER BY fecha", conn)

st.title("📊 Dashboard Financiero Pintosano")

if df.empty:
    st.warning("No hay datos cargados.")
    st.stop()

df["fecha"] = pd.to_datetime(df["fecha"])

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Ventas", f"${df['ventas_totales'].sum():,.2f}")
col2.metric("💵 Total Efectivo", f"${df['ventas_efectivo'].sum():,.2f}")
col3.metric("💳 Total Digital", f"${df['ventas_digital'].sum():,.2f}")

st.divider()

st.subheader("Evolución de Ventas")
st.line_chart(df.set_index("fecha")[["ventas_totales","ventas_efectivo","ventas_digital"]])

st.divider()

promedio = df["ventas_totales"].mean()
st.metric("Promedio diario", f"${promedio:,.2f}")

st.subheader("Resumen mensual")

df["mes"] = df["fecha"].dt.to_period("M")
resumen = df.groupby("mes").sum(numeric_only=True)

st.dataframe(resumen)