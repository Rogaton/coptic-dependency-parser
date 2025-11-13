# Coptic Dependency Parser

⚠️ **Warning: This program is still at an experimental stage. Use it at your own risk!**

A neural-symbolic dependency parser for Coptic texts, combining state-of-the-art neural dependency parsing with symbolic Prolog-based grammatical validation.

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📖 Description

The Coptic Dependency Parser is a specialized NLP tool designed for analyzing Coptic texts using Universal Dependencies formalism. It integrates:

- **Neural Parsing**: DiaParser (biaffine attention parser) for accurate dependency structure prediction
- **Symbolic Validation**: Prolog-based grammatical rules for Coptic-specific syntactic patterns
- **Text Normalization**: Automatic handling of combining diacritical marks to prevent unknown tokens
- **Interactive Visualization**: Graphical dependency tree display with transliteration

This hybrid neural-symbolic approach enhances parsing accuracy by leveraging both data-driven learning and explicit linguistic knowledge of Coptic grammar, including:
- VSO (Verb-Subject-Object) word order patterns
- Tripartite nominal sentences (Subject-Copula-Predicate)
- Coptic article and pronoun systems
- Morphological agreement rules

## ✨ Features

### Core Functionality
- **🔍 Dependency Parsing**: Neural dependency parsing using DiaParser trained on Coptic Scriptorium data
- **📝 Interactive GUI**: User-friendly interface with virtual Coptic keyboard
- **🌳 Tree Visualization**: Graphical dependency trees with arc labels and POS tags
- **📊 Multiple Export Formats**: HTML and PDF export of parsing results
- **⚙️ Text Normalization**: Automatic preprocessing to handle combining diacritics
- **✅ Grammatical Validation**: Prolog-based pattern matching and error detection

### Linguistic Features
- **Tripartite Pattern Recognition**: Automatic detection of Coptic nominal sentences
- **VSO Word Order Validation**: Coptic-specific syntactic constraint checking
- **Morphological Analysis**: Article stripping and clitic identification
- **POS Tagging**: Stanza-based part-of-speech tagging for Coptic
- **Lemmatization**: Basic lemmatization support

## 🚀 Installation

### Prerequisites

- **Python 3.8 or higher**
- **SWI-Prolog** (for Prolog integration)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install swi-prolog

  # macOS
  brew install swi-prolog

  # Windows: Download from https://www.swi-prolog.org/download/stable
  ```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Rogaton/coptic-dependency-parser.git
   cd coptic-dependency-parser
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Stanza models for Coptic**
   ```bash
   python3 -c "import stanza; stanza.download('cop')"
   ```

4. **Download or train the DiaParser model**

   The parser can work with either:
   - Pre-trained Coptic model (place in `models/cop.diaparser`)
   - Stanza's built-in dependency parser (automatic fallback)

   See `config.py` for model path configuration.

## 📚 Usage

### Running the GUI Application

```bash
python3 coptic-parser.py
```

### Using the Parser

1. **Input Text**: Type or paste Coptic text in the input field, or use the virtual keyboard
2. **Parse**: Click "Parse & Analyze Dependencies" to process the text
3. **View Results**:
   - **Parse Text Tab**: See detailed token-level analysis
   - **Dependency Graph Tab**: Navigate through visual dependency trees
   - **Dependency Table Tab**: Export results to HTML or PDF

### Example Input

```coptic
ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ
```

This tripartite sentence ("I am God") will be analyzed with:
- Dependency structure showing subject-copula-predicate relations
- Automatic pattern recognition
- POS tagging and lemmatization

### Programmatic Usage

```python
from coptic_prolog_rules import create_prolog_engine
import stanza

# Initialize NLP pipeline
nlp = stanza.Pipeline('cop', processors='tokenize,pos,lemma,depparse')

# Initialize Prolog validation
prolog = create_prolog_engine()

# Parse text
text = "ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ"
doc = nlp(text)

# Validate with Prolog
for sentence in doc.sentences:
    words = [word.text for word in sentence.words]
    pos_tags = [word.upos for word in sentence.words]
    heads = [word.head for word in sentence.words]
    deprels = [word.deprel for word in sentence.words]

    validation = prolog.validate_parse_tree(words, pos_tags, heads, deprels)
    print(validation)
```

## 📁 Project Structure

```
coptic-dependency-parser/
├── coptic-parser.py              # Main GUI application
├── coptic_prolog_rules.py        # Prolog integration module
├── coptic_text_normalizer.py    # Text preprocessing
├── config.py                     # Configuration management
├── coptic_grammar.pl             # Prolog dependency grammar rules
├── coptic_lexicon.pl             # Coptic lexical database (6,842+ entries)
├── requirements.txt              # Python dependencies
├── LICENSE                       # CC BY-NC-SA 4.0 License
├── README.md                     # This file
├── tools/                        # Evaluation and comparison tools
│   ├── parser_comparison_tool.py # Compare with CopticScriptorium
│   └── evaluate_baseline.py     # Baseline performance evaluation
├── docs/                         # Documentation
│   └── evaluation/              # Evaluation reports and documentation
│       ├── CORPUS_COMPARATIVE_ANALYSIS.md
│       └── COPTICSCRIPTORIUM_README.md
├── data/
│   ├── depparse/                # Training/evaluation data (CoNLL-U format)
│   ├── lexicon/                 # Lexical resources
│   └── tokenize/                # Tokenization data
└── models/
    └── cop.diaparser            # DiaParser model (download separately)
```

## 🔧 Configuration

Model paths and settings can be configured in `config.py`:

```python
# Set custom model path via environment variable
export COPTIC_DIAPARSER_MODEL=/path/to/your/cop.diaparser

# Or place model file in:
# ./models/cop.diaparser
```

## 📊 Data Sources

This parser uses linguistic data from:

- **Coptic Scriptorium** - UD-annotated Coptic corpus for training
- **Universal Dependencies** - Dependency annotation scheme
- **Comprehensive Coptic Lexicon** - Extracted morphological information

## 📈 Evaluation & Comparison

### Parser Comparison Tool

Compare the dependency parser with CopticScriptorium's morpheme-level tagger to understand their complementary strengths:

```bash
# Run comparison on example texts
python3 tools/parser_comparison_tool.py

# Compare specific text
python3 tools/parser_comparison_tool.py "ⲁϥⲥⲱⲧⲙ ⲙⲙⲟϥ"
```

**Key Differences:**
- **Dependency Parser**: Word-level tokenization, syntactic structure, UD framework
- **CS Tagger**: Morpheme-level segmentation, TreeTagger format, corpus annotation

Both tools share underlying components (Till analyzers, normalization) but serve different research purposes. See [COPTICSCRIPTORIUM_README.md](docs/evaluation/COPTICSCRIPTORIUM_README.md) for details.

### Performance Metrics

Evaluated across diverse Coptic text genres:

| Corpus Type | Coverage | Characteristics |
|-------------|----------|-----------------|
| Documentary Papyri | **95.6%** | Simple, formulaic syntax |
| Monastic Literature | **93.7%** | Standardized prescriptive language |
| Biblical Texts | **93.1%** | Translation Greek (Koine → Sahidic) |
| Literary Texts | **82.4%** | Complex rhetorical structures |

The parser achieves **82-96% coverage** using Till's grammar modules (§35-50 Articles, §292-304 Conjunctions, §309-319 Negations, §245-268 Morphology). See [CORPUS_COMPARATIVE_ANALYSIS.md](docs/evaluation/CORPUS_COMPARATIVE_ANALYSIS.md) for detailed evaluation results.

### Running Baseline Evaluation

```bash
# Evaluate parser performance on test corpora
python3 tools/evaluate_baseline.py

# Evaluate on specific corpus files
python3 tools/evaluate_baseline.py corpus1.txt corpus2.txt
```

## 🧪 Technical Details

### Architecture

- **Neural Parser**: BiAffine attention mechanism (Dozat & Manning, 2017)
- **POS Tagger**: Stanza neural pipeline for Coptic
- **Validation Engine**: PySwip integration with SWI-Prolog
- **Visualization**: Matplotlib-based dependency graph rendering

### Performance

- Handles multi-sentence documents
- Real-time validation with Prolog constraints
- Supports batch processing via command-line interface

### Linguistic Patterns Supported

- VSO transitive/intransitive sentences
- Tripartite nominal sentences (standard & converted)
- Determiner-noun phrases with gender agreement
- Adjective modification (post-nominal)
- Prepositional phrases
- Coordination structures

## 📄 License

**Original Work**: Copyright (c) 2024-2025 André Linden

Licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**You are free to:**
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

**Third-Party Dependencies**: Retain their respective original licenses (Apache 2.0, MIT, etc.). See `LICENSES/` directory for details.

## 🙏 Credits and Attribution

This parser integrates multiple open-source NLP tools and resources:

### Core NLP Tools

1. **[Coptic Scriptorium](https://copticscriptorium.org/)**
   - Coptic NLP models and annotated corpus
   - Citation: Zeldes, A., & Schroeder, C. T. (2016). "An NLP Pipeline for Coptic"
   - License: Creative Commons licenses (varies by component)

2. **[Stanza - Stanford NLP Library](https://stanfordnlp.github.io/stanza/)**
   - Tokenization, POS tagging, and lemmatization for Coptic
   - Citation: Qi, P., Zhang, Y., Zhang, Y., Bolton, J., & Manning, C. D. (2020). "Stanza: A Python Natural Language Processing Toolkit for Many Human Languages"
   - License: Apache 2.0

3. **[DiaParser - Biaffine Dependency Parser](https://github.com/Unipisa/diaparser)**
   - Neural dependency parsing implementation
   - Citation: Attardi, G., et al. (2009)
   - License: Apache 2.0

4. **[Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/)**
   - Neural dependency parsing architecture
   - Citation: Manning, C. D., Surdeanu, M., Bauer, J., Finkel, J., Bethard, S. J., & McClosky, D. (2014). "The Stanford CoreNLP Natural Language Processing Toolkit"
   - License: GPL v3+

### Linguistic Resources

- **Universal Dependencies Project** - Annotation scheme and guidelines
- **Comprehensive Coptic Lexicon** - Morphological database

### Additional Libraries

- **PySwip** - SWI-Prolog Python interface
- **Matplotlib** - Visualization library
- **WeasyPrint** - PDF export functionality

## 🐛 Known Issues

- Experimental stage: Results should be manually validated
- Large model files (50+ MB) require Git LFS or separate download
- Prolog integration requires SWI-Prolog installation
- Some rare Coptic constructions may not be recognized

## 🤝 Contributing

As this is an experimental research project, contributions and feedback are welcome:

- Report bugs or issues via GitHub Issues
- Suggest linguistic patterns or grammatical rules
- Contribute test cases or example texts

## 📧 Contact

For questions, suggestions, or collaboration inquiries:

- **Author**: André Linden
- **Email**: relanir@bluewin.ch
- **Project**: Coptic NLP Research

## 🔗 Related Resources

- [Coptic Scriptorium Project](https://copticscriptorium.org/)
- [Universal Dependencies](https://universaldependencies.org/)
- [Stanza Documentation](https://stanfordnlp.github.io/stanza/)
- [DiaParser Documentation](https://github.com/Unipisa/diaparser)

## 📜 Citation

If you use this parser in your research, please cite:

```bibtex
@software{coptic_dependency_parser,
  author = {Linden, André},
  title = {Coptic Dependency Parser: A Neural-Symbolic Approach},
  year = {2024-2025},
  url = {https://github.com/Rogaton/coptic-dependency-parser},
  note = {Experimental version}
}
```

---

**Note**: This is research software under active development. Always verify parsing results manually for critical applications.
