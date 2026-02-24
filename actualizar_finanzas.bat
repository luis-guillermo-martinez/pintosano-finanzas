@echo off

cd /d %~dp0

echo ==========================
echo ACTUALIZANDO DATOS
echo ==========================

python actualizar_finanzas.py

echo ==========================
echo SUBIENDO A GITHUB
echo ==========================

git add .
git commit -m "Actualizacion automatica"
git push origin main

echo.
echo SISTEMA COMPLETADO
pause