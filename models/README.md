# Models Directory

This directory is for storing trained models locally.

## 📥 Model Files

The parser looks for:
```
models/cop.diaparser
```

**File size**: ~51 MB (trained model)
**Models are NOT included in this repository** - see setup options below.

---

## 🔧 Setup Options

You have **three options** for using this parser:

### Option 1: Use Stanza's Built-in Parser (Easiest) ⭐

If you don't have the DiaParser model, the parser will automatically fall back to Stanza's built-in dependency parser for Coptic.

**No setup required!** Just install Stanza models:
```bash
python3 -c "import stanza; stanza.download('cop')"
```

The parser will detect that no DiaParser model is present and use Stanza instead.

### Option 2: Download Pre-trained Model

**Note**: Pre-trained models may be available from:
- Coptic Scriptorium project
- Universal Dependencies project
- Model hosting services

If you have access to a pre-trained Coptic DiaParser model:

1. Download the model file
2. Place it in this directory as `cop.diaparser`
3. The parser will automatically detect and use it

### Option 3: Train Your Own Model (Advanced)

If you have the training data from CopticScriptorium, you can train your own model.

**Requirements**:
- Training data: `data/depparse/cop_scriptorium.train.in.conllu`
- Development data: `data/depparse/cop_scriptorium.dev.in.conllu`
- Test data: `data/depparse/cop_scriptorium.test.in.conllu`

**Training time**: 2-4 hours (CPU), 30-60 minutes (GPU)

---

## 🔍 How the Parser Finds the Model

The parser checks for models in this priority order:

1. **Environment variable**: `COPTIC_DIAPARSER_MODEL`
   ```bash
   export COPTIC_DIAPARSER_MODEL=/path/to/cop.diaparser
   ```

2. **Local model**: `./models/cop.diaparser` (this directory)

3. **Fallback**: Use Stanza's built-in dependency parser

See `config.py` for configuration details.

---

## 📊 Model Information

**Trained on**: Coptic Scriptorium Universal Dependencies corpus
- **Architecture**: BiAffine attention dependency parser (Dozat & Manning, 2017)
- **Annotation**: Universal Dependencies v2 scheme
- **Language**: Sahidic Coptic (primarily)

---

## 🚀 Quick Start

### For Users (No Model Available)

```bash
# Install dependencies
pip install -r requirements.txt

# Download Stanza models (automatic fallback)
python3 -c "import stanza; stanza.download('cop')"

# Run parser (will use Stanza)
python3 coptic-parser.py
```

### For Users (With Model)

```bash
# Place model in this directory
cp /path/to/trained/model.diaparser ./models/cop.diaparser

# Run parser (will use DiaParser)
python3 coptic-parser.py
```

---

## 📚 Additional Resources

- **DiaParser**: https://github.com/Unipisa/diaparser
- **Coptic Scriptorium**: https://copticscriptorium.org/
- **Universal Dependencies**: https://universaldependencies.org/

---

## ⚖️ Licensing

Model files in this directory retain their original licenses:
- CopticScriptorium models: See their project for license terms
- DiaParser: Apache 2.0 License
- Other models: Consult respective sources

This repository's code (separate from models) is licensed under CC BY-NC-SA 4.0.
