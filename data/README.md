# Data Directory

This directory contains optional training and reference data for the Coptic Dependency Parser.

## ⚠️ Important: Parser Works Without This Data!

**The parser is ready to use without any files in this directory.** All essential lexical data is already embedded in `coptic_lexicon.pl` (6,842+ entries).

These data folders are only needed if you want to:
- Retrain the dependency parsing model
- Experiment with different training configurations
- Extend the lexicon with your own data

## 📁 Directory Structure

### `depparse/` - Dependency Parsing Training Data

**Purpose**: CoNLL-U format treebank files for training DiaParser

**Files needed (if training)**:
- `cop_scriptorium.train.in.conllu` (~114 MB)
- `cop_scriptorium.dev.in.conllu` (~14 MB)
- `cop_scriptorium.test.in.conllu` (~14 MB)

**Where to obtain**:
- Coptic Scriptorium UD Treebank: https://github.com/UniversalDependencies/UD_Coptic-Scriptorium
- Download the latest release
- Place .conllu files in this directory

**License**: CC BY-SA 4.0 (Coptic Scriptorium)

### `lexicon/` - Lexical Resources

**Purpose**: Additional lexical data for analysis

**Note**: The main lexicon is already in `coptic_lexicon.pl` at the project root. This directory is for supplementary resources only.

**Optional files**:
- Custom lexicon extensions
- Frequency lists
- Morphological databases

### `tokenize/` - Tokenization Configuration

**Purpose**: Multi-word token (MWT) expansion rules

**Files included**:
- `cop_scriptorium-ud-dev-mwt.json` - Development set MWT rules
- `cop_scriptorium-ud-train-mwt.json` - Training set MWT rules

These tiny configuration files are included and used by Stanza for proper tokenization.

## 🚀 Quick Start

### For Users (Just Want to Parse Text)

**You don't need anything in this directory!** Just run:

```bash
pip install -r requirements.txt
python3 -c "import stanza; stanza.download('cop')"
python3 coptic-parser.py
```

The parser will work immediately using:
- Stanza's built-in models
- The embedded `coptic_lexicon.pl` lexicon
- Prolog grammar rules in `coptic_grammar.pl`

### For Developers (Want to Train Models)

1. **Download training data** from Coptic Scriptorium
2. **Place .conllu files** in `depparse/`
3. **Train with DiaParser** (see models/README.md)

## 📊 Data Statistics

### Embedded Lexicon (coptic_lexicon.pl)
- **Entries**: 6,842 lemmas
- **Coverage**: Nouns, verbs, adjectives, pronouns, particles, etc.
- **Features**: Gender, number, morphological information
- **Source**: Extracted from Coptic Scriptorium resources

### Training Corpus (optional download)
- **Tokens**: ~140,000 tokens
- **Sentences**: ~5,000 sentences
- **Language**: Sahidic Coptic (primarily)
- **Annotation**: Universal Dependencies v2 scheme

## 📖 Documentation

For more information about the data sources and training:
- **Coptic Scriptorium**: https://copticscriptorium.org/
- **Universal Dependencies**: https://universaldependencies.org/cop/
- **Main README**: ../README.md

## ⚖️ License

- **Training data**: CC BY-SA 4.0 (Coptic Scriptorium)
- **This parser code**: CC BY-NC-SA 4.0
- **Embedded lexicon**: Derived from Coptic Scriptorium, CC BY-SA 4.0

---

**TL;DR**: These folders are empty placeholders. Users don't need to add anything here unless they want to retrain models. The parser works out-of-the-box with the included lexicon and grammar files.
