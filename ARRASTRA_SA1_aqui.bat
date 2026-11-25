@echo off
REM Arrastra el .sa1 (64 KB) -> crea el .sav de 128 KB estandar
python "%~dp0x6_gen3.py" ring2std "%~1"
pause
