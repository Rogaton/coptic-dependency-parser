# Troubleshooting Guide - Coptic Parser

## Common Issues and Solutions

---

## 🔴 Issue: Missing Dependencies (joblib, pandas, scikit-learn, etc.)

### **Symptoms:**
```
ModuleNotFoundError: No module named 'joblib'
ModuleNotFoundError: No module named 'pandas'
ModuleNotFoundError: No module named 'sklearn'
```

### **Root Cause:**
You're not in the virtual environment! When you restart your terminal or computer, the virtual environment is not automatically activated.

### **Solution 1: Use the Startup Script** ⭐ RECOMMENDED

```bash
./start-parser.sh
```

This script:
- ✓ Automatically activates the virtual environment
- ✓ Verifies all dependencies are installed
- ✓ Creates venv if missing
- ✓ Installs dependencies if needed
- ✓ Launches the parser

### **Solution 2: Manually Activate Virtual Environment**

```bash
# Navigate to parser directory
cd /home/aldn/NLP/coptic-nlp/stanfordparser/stanza

# Activate virtual environment
source .venv/bin/activate

# You should see (.venv) in your prompt now
# Then run the parser
python3 coptic-parser.py
```

### **Solution 3: Reinstall All Dependencies**

If packages are truly missing:

```bash
# Activate virtual environment first
source .venv/bin/activate

# Reinstall all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(joblib|pandas|sklearn|stanza|diaparser)"
```

---

## 🔴 Issue: Parser Fails on Restart

### **Symptoms:**
Parser worked before, but now won't start after reboot or new terminal.

### **Diagnosis:**
```bash
# Check which Python is being used
which python3

# If it shows /usr/bin/python3 instead of .venv/bin/python3,
# you're NOT in the virtual environment!
```

### **Solution:**

**ALWAYS activate the virtual environment before running:**

```bash
# Option 1: Use the startup script
./start-parser.sh

# Option 2: Manually activate
source .venv/bin/activate
python3 coptic-parser.py
```

**Pro Tip:** Create an alias in your `~/.bashrc`:

```bash
echo "alias coptic-parser='cd /home/aldn/NLP/coptic-nlp/stanfordparser/stanza && ./start-parser.sh'" >> ~/.bashrc
source ~/.bashrc

# Now you can just type from anywhere:
coptic-parser
```

---

## 🔴 Issue: "No module named 'tkinter'"

### **Symptoms:**
```
ModuleNotFoundError: No module named 'tkinter'
ImportError: No module named '_tkinter'
```

### **Solution:**

Tkinter is not a pip package - it's part of Python system packages.

**On Linux:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**On macOS:**
- Tkinter should be included with Python from python.org
- If using Homebrew Python: `brew install python-tk@3.12` (adjust version)

**On Windows:**
- Reinstall Python from python.org with "tcl/tk" option checked

---

## 🔴 Issue: "Stanza models not found"

### **Symptoms:**
```
FileNotFoundError: Stanza cop models not found
```

### **Solution:**

```bash
# Activate virtual environment
source .venv/bin/activate

# Download Coptic models
python3 -c "import stanza; stanza.download('cop')"
```

---

## 🔴 Issue: Import errors with PyTorch

### **Symptoms:**
```
ImportError: cannot import name 'xxx' from 'torch'
RuntimeError: CUDA error
```

### **Solution:**

**For CPU-only systems:**
```bash
source .venv/bin/activate
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

**For GPU systems:**
```bash
source .venv/bin/activate
pip install torch --index-url https://download.pytorch.org/whl/cu118  # CUDA 11.8
# or
pip install torch --index-url https://download.pytorch.org/whl/cu121  # CUDA 12.1
```

---

## 🔴 Issue: "xgboost" version incompatibility

### **Symptoms:**
```
XGBoostError: check failed
xgboost.core.XGBoostError: [serialization]
```

### **Solution:**

XGBoost 2.0+ has breaking changes. Use older version:

```bash
source .venv/bin/activate
pip uninstall xgboost
pip install 'xgboost<2.0.0'
```

---

## 🔴 Issue: Parsing is very slow

### **Possible Causes:**

1. **First run** - Models are loading (takes 10-30 seconds)
2. **Very long text** - Expected for 50+ sentences
3. **No GPU** - Parser uses CPU, which is slower

### **Solutions:**

- **Be patient on first run** - Normal behavior
- **For very long texts** - Consider splitting into smaller chunks
- **Use GPU if available** - Install PyTorch with CUDA support

---

## 🔴 Issue: GUI doesn't display Coptic text properly

### **Symptoms:**
Coptic letters show as squares or question marks.

### **Solution:**

Install Coptic fonts:

**On Linux:**
```bash
sudo apt-get install fonts-noto
# or
sudo apt-get install fonts-sil-nuosu
```

**On macOS:**
```bash
# Download and install Noto Sans Coptic from:
# https://fonts.google.com/noto/specimen/Noto+Sans+Coptic
```

**On Windows:**
- Download Noto Sans Coptic from Google Fonts
- Double-click to install

---

## 🔴 Issue: "Permission denied" when running start-parser.sh

### **Solution:**

Make the script executable:

```bash
chmod +x start-parser.sh
./start-parser.sh
```

---

## 🟡 Best Practices to Avoid Issues

### **1. Always Use the Virtual Environment**

```bash
# GOOD - Use startup script
./start-parser.sh

# GOOD - Manually activate first
source .venv/bin/activate
python3 coptic-parser.py

# BAD - Running without activation
python3 coptic-parser.py  # This might use system Python!
```

### **2. Check Your Environment**

Before running, verify:

```bash
# Should show .venv/bin/python3
which python3

# Should show (.venv) in prompt
# (.venv) user@computer:~/path$
```

### **3. Keep Dependencies Updated**

```bash
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### **4. Use the Startup Script**

The `start-parser.sh` script handles everything:
- Finds and activates venv
- Verifies dependencies
- Shows what's missing
- Launches parser

---

## 🔍 Diagnostic Commands

### **Check if in Virtual Environment:**
```bash
echo $VIRTUAL_ENV
# Should show path to .venv
```

### **List Installed Packages:**
```bash
source .venv/bin/activate
pip list
```

### **Verify Critical Packages:**
```bash
source .venv/bin/activate
python3 << 'EOF'
import stanza
import torch
import diaparser
import numpy
import matplotlib
import pandas
import sklearn
import joblib
print("✓ All critical packages imported successfully!")
EOF
```

### **Check Python Version:**
```bash
python3 --version
# Should be 3.8 or higher
```

---

## 🆘 Still Having Issues?

### **Complete Clean Reinstall:**

```bash
cd /home/aldn/NLP/coptic-nlp/stanfordparser/stanza

# Remove old virtual environment
rm -rf .venv

# Create fresh virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Download Stanza models
python3 -c "import stanza; stanza.download('cop')"

# Test
python3 coptic-parser.py
```

### **Check System Requirements:**

- Python 3.8 or higher
- 2GB+ RAM
- 2GB+ free disk space
- Linux, macOS, or Windows with WSL
- Internet connection (for model downloads)

---

## 📞 Getting Help

If issues persist:

1. **Check existing issues** on GitHub (once published)
2. **Open a new issue** with:
   - Your OS and Python version
   - Complete error message
   - Output of `pip list`
   - Steps to reproduce

3. **Include diagnostic info:**
   ```bash
   python3 --version
   which python3
   echo $VIRTUAL_ENV
   pip list | grep -E "(stanza|torch|diaparser)"
   ```

---

## ✅ Quick Reference

| Problem | Quick Fix |
|---------|-----------|
| Missing modules | `./start-parser.sh` or `source .venv/bin/activate` |
| Parser won't start | Use startup script: `./start-parser.sh` |
| No tkinter | `sudo apt-get install python3-tk` |
| No Stanza models | `python3 -c "import stanza; stanza.download('cop')"` |
| Coptic text shows squares | Install Noto Sans Coptic font |
| Very slow | Normal on first run or large texts |
| XGBoost errors | `pip install 'xgboost<2.0.0'` |

---

**Last Updated**: 2024
**Version**: 1.1
