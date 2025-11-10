# Quick Start Guide - Coptic Dependency Parser

Get started with the Coptic Dependency Parser in 5 minutes!

## Prerequisites

- **Python 3.8+** installed on your system
- **SWI-Prolog** for grammatical validation (optional but recommended)

### Install SWI-Prolog

```bash
# Ubuntu/Debian
sudo apt-get install swi-prolog

# macOS (using Homebrew)
brew install swi-prolog

# Windows
# Download installer from: https://www.swi-prolog.org/download/stable
```

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/Rogaton/coptic-dependency-parser.git
cd coptic-dependency-parser
```

### 2. Create a Virtual Environment (Recommended)

Modern Linux systems (Ubuntu 23.04+, Debian 12+) use externally-managed Python environments. Using a virtual environment is the **recommended approach** to avoid conflicts:

```bash
# Create virtual environment
python3 -m venv coptic-env

# Activate it
source coptic-env/bin/activate
```

**Note**: Your prompt will change to show `(coptic-env)` when the environment is active.

**Windows users**: Use `coptic-env\Scripts\activate` instead.

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install all necessary packages:
- `stanza` - Stanford NLP for Coptic tokenization and POS tagging
- `diaparser` - Neural dependency parser
- `torch` - PyTorch (required by the above)
- `pyswip` - Prolog integration for grammatical validation
- `matplotlib`, `numpy`, `pandas` - Visualization and data handling
- `weasyprint` - PDF export functionality
- `tqdm` - Progress bars

**Note**: The installation may take a few minutes as PyTorch is a large package (~800MB).

**If you get "externally-managed-environment" error**: You must use a virtual environment (see step 2 above). Do not use `--break-system-packages` as it can damage your system Python installation.

### 4. Download Stanza Models

#```bash
pip install stanza     # works but should not be necessary as stanza is installed by running the 'requirements.txt' file.

#python3 -c "import stanza; stanza.download('cop')" # Fails. Use 'pip install stanza instead if installing dependencies does not complete.
```

This downloads the Coptic language models (~50MB) for tokenization, POS tagging, and lemmatization.

### 5. Configure DiaParser Model (Optional)

The parser can work with either:
- **DiaParser** (recommended) - Place your trained model at `models/cop.diaparser`
- **Stanza's built-in parser** (automatic fallback) - No additional setup needed

If you have a trained DiaParser model, place it in the `models/` directory:
```bash
mkdir -p models
# Copy your cop.diaparser model to models/
```

Or set a custom path:
```bash
export COPTIC_DIAPARSER_MODEL=/path/to/your/cop.diaparser
```

## Running the Parser

### Start the GUI

**Important**: If you're using a virtual environment, make sure it's activated first:
```bash
source coptic-env/bin/activate  # Only needed if not already activated
```

Then run the parser:
```bash
python3 coptic-parser.py
```

The graphical interface will open with three main tabs:
- **Parse Text** - Input and analyze Coptic text
- **Dependency Graph** - View visual dependency trees
- **Dependency Table** - Export results to HTML or PDF

### Try an Example

1. In the "Parse Text" tab, enter some Coptic text (or use the virtual keyboard):
   ```
   ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ
   ```

2. Click **"Parse & Analyze Dependencies"**

3. View the results:
   - Token-level analysis with POS tags and dependency relations
   - Navigate through dependency graphs in the "Dependency Graph" tab
   - Export to HTML or PDF in the "Dependency Table" tab

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'stanza'`

**Solution**: Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: `ModuleNotFoundError: No module named 'diaparser'`

**Solution**: Install diaparser explicitly:
```bash
pip install diaparser>=1.1.0
```

### Issue: Stanza models not found

**Solution**: Download the Coptic models:
```bash
python3 -c "import stanza; stanza.download('cop')"
```

### Issue: PySwip errors or Prolog not working

**Solution**:
1. Make sure SWI-Prolog is installed (see Prerequisites above)
2. The parser will still work without Prolog, but grammatical validation will be disabled

### Issue: "externally-managed-environment" error

**Error message**: `error: externally-managed-environment × This environment is externally managed`

**Solution**: You MUST use a virtual environment on modern Linux systems. Go back to step 2 and create a virtual environment:
```bash
python3 -m venv coptic-env
source coptic-env/bin/activate
pip install -r requirements.txt
```

### Issue: `pip install` fails with dependency conflicts

**Solution**: Create a fresh virtual environment:
```bash
# Remove old environment if it exists
rm -rf coptic-env

# Create fresh virtual environment
python3 -m venv coptic-env

# Activate it
source coptic-env/bin/activate  # Linux/macOS
# OR
coptic-env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Issue: PyTorch is too large to download

**Solution**: Install CPU-only PyTorch for smaller download:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

## What's Next?

- **Full Documentation**: See [README.md](docs/README.md) for detailed features and usage
- **Project Structure**: Explore the codebase organization
- **Configuration**: Customize settings in `config.py`
- **Data**: Check `data/` directory for training data and lexical resources

## Quick Reference

### Command Line Usage

```bash
# Start GUI
python3 coptic-parser.py

# Download Stanza models
python3 -c "import stanza; stanza.download('cop')"

# Check configuration
python3 config.py
```

### Programmatic Usage

```python
import stanza
from coptic_prolog_rules import create_prolog_engine

# Initialize pipeline
nlp = stanza.Pipeline('cop', processors='tokenize,pos,lemma,depparse')

# Parse text
text = "ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ"
doc = nlp(text)

# Access results
for sentence in doc.sentences:
    for word in sentence.words:
        print(f"{word.text}\t{word.upos}\t{word.deprel}")
```

## Support

For issues, questions, or contributions:
- **GitHub Issues**: Report bugs or request features
- **Email**: relanir@bluewin.ch
- **Documentation**: See [docs/README.md](docs/README.md)

---

**Ready to parse!** 🚀
