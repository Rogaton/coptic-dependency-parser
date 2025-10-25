#!/bin/bash
# Convenience script to run Coptic parser with correct venv

cd "$(dirname "$0")"
source .venv/bin/activate
python3 coptic-parser.py
