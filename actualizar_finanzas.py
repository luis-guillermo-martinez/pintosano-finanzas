import os
import sqlite3
import pandas as pd

# ===== CONFIGURACION =====
BASE_PATH = r"C:\Users\luism\OneDrive\Desarrollo\mi_software_dietetica\pintosano-finanzas"
CARPETA_REPORTES = os.path.join(BASE_PATH, "reportes_caja")
BASE_DATOS = os.path.join(BASE_PATH, "finanzas.db")

# ===== CONECTAR BASE =====
conn = sqlite3.connect(BASE_DATOS)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS caja_diaria (
    fecha TEXT PRIMARY KEY,
    ventas_totales REAL,
    ventas_efectivo REAL,
    ventas_digital REAL,
    total_caja REAL,
    diferencia REAL
)
""")
conn.commit()


# ===== FUNCION LIMPIAR NUMEROS =====
def limpiar_numero(valor):
    if pd.isna(valor):
        return None

    valor = str(valor).strip().replace("$", "").strip()

    # Si ya viene como float correcto, devolverlo
    try:
        return float(valor)
    except:
        pass

    # Si viene formato argentino 100.331,18
    if "," in valor:
        valor = valor.replace(".", "")
        valor = valor.replace(",", ".")
        return float(valor)

    return float(valor)



# ===== PROCESAR ARCHIVOS =====
archivos = [f for f in os.listdir(CARPETA_REPORTES) if f.lower().endswith(".xls")]

for archivo in archivos:
    ruta = os.path.join(CARPETA_REPORTES, archivo)

    df = pd.read_excel(ruta, header=None)

    fecha = None
    ventas_totales = None
    ventas_efectivo = None
    ventas_digital = None
    total_caja = None
    diferencia = None

    for i in range(len(df)):
        for j in range(len(df.columns)):

            valor = str(df.iloc[i, j])

            if "Fecha/Hora Cierre:" in valor:
                fecha = str(df.iloc[i, j+1]).strip()

            if "Total Ventas:" in valor:
                ventas_totales = limpiar_numero(df.iloc[i, j+1])

            if "Total Ventas Efectivo:" in valor:
                ventas_efectivo = limpiar_numero(df.iloc[i, j+1])

            if "Total Ventas M.Digital:" in valor:
                ventas_digital = limpiar_numero(df.iloc[i, j+1])

            if "Total en  Caja CALCULADO:" in valor:
                total_caja = limpiar_numero(df.iloc[i, j+1])

            if "Diferencia con  Caja Calculada:" in valor:
                diferencia = limpiar_numero(df.iloc[i, j+1])

    print("Procesando:", archivo)
    print("Fecha detectada:", fecha)

    if fecha:
        try:
            cursor.execute("""
                INSERT INTO caja_diaria 
                (fecha, ventas_totales, ventas_efectivo, ventas_digital, total_caja, diferencia)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                fecha,
                ventas_totales,
                ventas_efectivo,
                ventas_digital,
                total_caja,
                diferencia
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            pass


# ===== RESUMEN =====
cursor.execute("SELECT COUNT(*) FROM caja_diaria")
total_dias = cursor.fetchone()[0]

print("\n====== RESUMEN FINANCIERO ======\n")
print("Días registrados:", total_dias)

if total_dias > 0:
    cursor.execute("SELECT AVG(ventas_totales) FROM caja_diaria")
    promedio = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM caja_diaria WHERE diferencia < 0")
    dias_negativos = cursor.fetchone()[0]

    print("Venta promedio:", round(promedio, 2))
    print("Días con diferencia negativa:", dias_negativos)
else:
    print("Sin datos cargados todavía.")

input("\nPresioná Enter para cerrar...")
