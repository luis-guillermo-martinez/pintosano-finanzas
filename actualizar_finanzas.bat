@echo off
cd /d C:\Users\luism\OneDrive\Proyecto\FINANZAS_PINTOSANO

echo =============================
echo ACTUALIZANDO FINANZAS
echo =============================

python actualizar_finanzas.py
python resumen_mensual.py
python grafico_finanzas.py
python reporte_pdf.py

echo.
echo ===== SISTEMA COMPLETADO =====
pause
