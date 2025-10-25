# Quick Start Guide - Coptic Parser

## 🚀 Fastest Way to Start

```bash
./start-parser.sh
```

That's it! The startup script does everything automatically.

---

## 📋 What the Startup Script Does

✅ Finds and activates the virtual environment
✅ Checks all dependencies are installed
✅ Creates virtual environment if missing
✅ Installs missing packages automatically
✅ Launches the parser

---

## 🔧 Manual Start (if needed)

```bash
# 1. Navigate to parser directory
cd /home/aldn/NLP/coptic-nlp/stanfordparser/stanza

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Run parser
python3 coptic-parser.py
```

---

## ⚠️ Common Mistake

```bash
# ❌ WRONG - No virtual environment activation
python3 coptic-parser.py

# ✅ CORRECT - Use startup script
./start-parser.sh

# ✅ CORRECT - Or activate first
source .venv/bin/activate
python3 coptic-parser.py
```

---

## 🔍 How to Know You're in the Virtual Environment

Your prompt should show `(.venv)`:

```bash
# ✅ Correct - Virtual environment active
(.venv) aldn@alsys:~/path/to/stanza$

# ❌ Wrong - No virtual environment
aldn@alsys:~/path/to/stanza$
```

---

## 🐛 Getting "ModuleNotFoundError"?

This means you're NOT in the virtual environment!

**Quick fix:**
```bash
./start-parser.sh
```

Or manually:
```bash
source .venv/bin/activate
python3 coptic-parser.py
```

---

## 📦 First Time Setup

If you've never installed dependencies:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download Coptic models
python3 -c "import stanza; stanza.download('cop')"

# Make startup script executable
chmod +x start-parser.sh

# Done! Now use:
./start-parser.sh
```

---

## 🎯 Create a Global Command (Optional)

To run the parser from anywhere:

```bash
# Add to your ~/.bashrc
echo "alias coptic-parser='cd /home/aldn/NLP/coptic-nlp/stanfordparser/stanza && ./start-parser.sh'" >> ~/.bashrc

# Reload
source ~/.bashrc

# Now from any directory, just type:
coptic-parser
```

---

## 📚 Need More Help?

- **Detailed troubleshooting**: See `TROUBLESHOOTING.md`
- **Full documentation**: See `README.md`
- **Missing modules**: See "Missing Dependencies" section in TROUBLESHOOTING.md

---

## ✅ Checklist

Before starting the parser, ensure:

- [ ] You're in the stanza directory
- [ ] Virtual environment exists (`.venv/` folder)
- [ ] Dependencies are installed (`requirements.txt`)
- [ ] Stanza Coptic models downloaded
- [ ] Startup script is executable (`chmod +x start-parser.sh`)

---

## 🎓 Understanding Virtual Environments

### What is `.venv`?
A directory containing Python packages **isolated** from your system Python.

### Why do I need to activate it?
So Python knows where to find the installed packages (joblib, pandas, sklearn, etc.)

### What happens if I don't activate?
Python looks in system directories, won't find the packages, and gives "ModuleNotFoundError"

### How do I activate it?
```bash
source .venv/bin/activate
```

### How do I know it's active?
Your prompt shows `(.venv)` at the beginning.

---

## 💡 Pro Tips

1. **Always use the startup script** - Handles everything for you
2. **New terminal = Need to activate again** - Virtual environments aren't automatic
3. **Reboot = Need to activate again** - Same reason
4. **Use the alias** - Makes starting easier
5. **Keep requirements.txt updated** - All dependencies are listed

---

**Remember**: If you see "ModuleNotFoundError", you forgot to activate the virtual environment!

**Solution**: `./start-parser.sh` 🎯
