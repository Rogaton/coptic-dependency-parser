#!/bin/bash
# Convenience script to run Coptic parser web app with correct venv

cd "$(dirname "$0")"
source .venv/bin/activate
python3 app.py
