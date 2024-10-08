#!/bin/bash
# Setze den Pfad zu Python und dem Skript im Home-Verzeichnis des aktuellen Benutzers
PYTHON_PATH="/usr/bin/python3"  # Pfad zu Python
SCRIPT_PATH="$HOME/virt_viewer.py"  # Home-Verzeichnis des aktuellen Benutzers

# Führe das Python-Skript aus
"$PYTHON_PATH" "$SCRIPT_PATH"

# Warte auf eine Eingabe (optional)
read -p "Press any key to continue..."
