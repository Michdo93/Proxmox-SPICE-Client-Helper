@echo off
REM Setze den Pfad zu Python und dem Skript im Home-Verzeichnis des aktuellen Benutzers
set PYTHON_PATH=C:\Python312\python.exe
set SCRIPT_PATH=%USERPROFILE%\virt_viewer.py  REM Home-Verzeichnis des aktuellen Benutzers

REM Führe das Python-Skript aus
"%PYTHON_PATH%" "%SCRIPT_PATH%"

REM Warte auf eine Eingabe, bevor das Fenster geschlossen wird
pause
