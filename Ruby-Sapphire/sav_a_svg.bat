@echo off
REM Uso: sav_a_svg.bat plantilla.svg save.sav
python "%~dp0x6_gen3.py" sav2svg "%~1" "%~2"
pause
