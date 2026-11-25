@echo off
REM Arrastra un archivo .svg de la X6 sobre este .bat -> crea el .sav de 128 KB
python "%~dp0x6_gen3.py" svg2sav "%~1"
pause
