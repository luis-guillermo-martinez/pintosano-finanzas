import sqlite3
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

BASE_PATH = r"C:\Users\luism\OneDrive\Proyecto\FINANZAS_PINTOSANO"
BASE_DATOS = os.path.join(BASE_PATH, "finanzas.db")
PDF_PATH = os.path.join(BASE_PATH, "reporte_financiero.pdf")

conn = sqlite3.connect(BASE_DATOS)
df = pd.read_sql_query("SELECT * FROM caja_diaria", conn)

if df.empty:
    print("No hay datos.")
    exit()

df["fecha"] = pd.to_datetime(df["fecha"])

total = df["ventas_totales"].sum()
efectivo = df["ventas_efectivo"].sum()
digital = df["ventas_digital"].sum()
diferencia = df["diferencia"].sum()

doc = SimpleDocTemplate(PDF_PATH)
elements = []

style = ParagraphStyle(name='Normal', fontSize=12)

elements.append(Paragraph("REPORTE FINANCIERO PINTOSANO", style))
elements.append(Spacer(1, 0.5 * inch))

elements.append(Paragraph(f"Total Ventas: ${round(total,2)}", style))
elements.append(Paragraph(f"Total Efectivo: ${round(efectivo,2)}", style))
elements.append(Paragraph(f"Total Digital: ${round(digital,2)}", style))
elements.append(Paragraph(f"Diferencia Acumulada: ${round(diferencia,2)}", style))

doc.build(elements)

print("PDF generado en:", PDF_PATH)
