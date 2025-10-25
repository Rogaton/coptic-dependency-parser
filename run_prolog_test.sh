#!/bin/bash
# Convenience script to run Prolog tests with correct venv

cd "$(dirname "$0")"
source .venv/bin/activate
python3 coptic_prolog_rules.py
