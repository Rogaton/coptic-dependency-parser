# Coptic Dependency Parser

Neural dependency parser for Coptic text with tokenization, POS tagging, lemmatization, and dependency analysis.

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Stanza](https://img.shields.io/badge/Stanza-NLP-green.svg)](https://stanfordnlp.github.io/stanza/)

> **Try it online:** [Coptic Parser Web Demo](https://huggingface.co/spaces/Rogaton/coptic-dependency-parser) (no installation required)

---

## Overview

This parser provides comprehensive linguistic analysis of Coptic texts using state-of-the-art neural NLP models:

- **Tokenization**: Sentence and word segmentation
- **POS Tagging**: Universal Dependencies tagset (NOUN, VERB, DET, etc.)
- **Lemmatization**: Dictionary/base forms of words
- **Dependency Parsing**: Grammatical relationships (subject, object, modifier, etc.)
- **Visualization**: Interactive dependency trees and tables

Perfect for Coptic language students, digital humanities researchers, linguists, and corpus analysts.

---

## Features

✨ **Full NLP Pipeline**
- Trained on [Coptic SCRIPTORIUM](https://copticscriptorium.org/) corpus
- Neural dependency parser with biaffine attention ([DiaParser](https://github.com/Unipisa/diaparser))
- Integrated with [Stanford Stanza](https://stanfordnlp.github.io/stanza/) framework

🖥️ **Two Interfaces**
- **GUI Application**: Desktop app with dependency graph visualization
- **Command Line**: Scriptable batch processing

📊 **Output Formats**
- Interactive tables
- Dependency tree graphs
- CoNLL-U format
- Plain text analysis

---

## Installation

### Prerequisites

- **Python 3.9 or higher**
- **pip** (Python package manager)
- **virtualenv** (recommended)

### Step-by-Step Installation

1. **Clone the repository:**

```bash
git clone https://github.com/Rogaton/coptic-dependency-parser.git
cd coptic-dependency-parser
```

2. **Create a virtual environment:**

```bash
python3 -m venv .venv
```

3. **Activate the virtual environment:**

```bash
# On Linux/macOS:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

4. **Install dependencies:**

```bash
pip install -r requirements.txt
```

5. **Download Coptic models:**

```bash
python3 -c "import stanza; stanza.download('cop')"
```

This will download the Stanza Coptic language models (~100MB).

---

## Quick Start

### GUI Application

Launch the full graphical interface with dependency visualization:

```bash
python3 coptic-parser.py
```

Features:
- Input Coptic text via virtual keyboard or paste
- View results in interactive table
- Generate dependency tree graphs
- Navigate between sentences
- Export results

### Simple GUI (Tokenization & POS Only)

For faster tokenization and POS tagging without full dependency parsing:

```bash
python3 coptic-parser-simple-wrapper.py
```

### Web Demo

For quick testing without installation, use the online demo:

🔗 **[Try the Hugging Face Space](https://huggingface.co/spaces/Rogaton/coptic-dependency-parser)**

---

## Usage Examples

### Example 1: Parse a Simple Sentence

**Input:**
```
ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ
```
(Translation: "I am God")

**Output:**
```
ID   FORM     LEMMA    UPOS   HEAD   DEPREL
1    ⲁⲛⲟⲕ    ⲁⲛⲟⲕ    PRON   2      nsubj
2    ⲡⲉ      ⲡⲉ      AUX    0      root
3    ⲡⲛⲟⲩⲧⲉ  ⲛⲟⲩⲧⲉ   NOUN   2      nsubj
```

### Example 2: Analyze Multiple Sentences

Paste or type multiple sentences - the parser automatically handles sentence boundaries.

### Example 3: Export Results

Results can be:
- Copied from the output window
- Saved as text files
- Exported in CoNLL-U format for further analysis

---

## Documentation

- **[Quick Start Guide](QUICK_START.md)**: Fast setup and common workflows
- **[Troubleshooting](TROUBLESHOOTING.md)**: Solutions to common issues
- **[Contributing](CONTRIBUTING.md)**: How to contribute to the project
- **[Credits & Attribution](CREDITS_AND_ATTRIBUTION.md)**: Acknowledgments and citations

---

## Performance

### Model Details

- **Framework**: Stanford Stanza + DiaParser
- **Architecture**: BiLSTM with biaffine attention
- **Training Data**: Coptic SCRIPTORIUM Universal Dependencies corpus
- **Training Time**: ~12 hours on CPU (Intel, 64GB RAM)

### Speed Benchmarks

- **Desktop**: Near-instant parsing for typical texts
- **Web demo (CPU)**: ~190 words/second
- **Batch processing**: Efficient for large corpora

---

## Technical Architecture

```
Input Text
    ↓
┌─────────────────┐
│  Stanza Pipeline │
│  - Tokenization  │
│  - POS Tagging   │
│  - Lemmatization │
└────────┬─────────┘
         ↓
┌─────────────────┐
│   DiaParser      │
│  - Biaffine Dep. │
│  - Graph Builder │
└────────┬─────────┘
         ↓
┌─────────────────┐
│  Visualization   │
│  - Tables        │
│  - Graphs        │
│  - CoNLL-U       │
└─────────────────┘
```

---

## Training Your Own Models

The repository includes training data in the `data/` directory:

- **Tokenization**: `data/tokenize/`
- **Dependency parsing**: `data/depparse/`

See the Stanza and DiaParser documentation for training instructions.

---

## Built With

### Core Dependencies

- **[Coptic SCRIPTORIUM](https://copticscriptorium.org/)** - Training corpus and annotations
- **[Stanford Stanza](https://stanfordnlp.github.io/stanza/)** - NLP pipeline framework
- **[DiaParser](https://github.com/Unipisa/diaparser)** - Neural dependency parser
- **[PyTorch](https://pytorch.org/)** - Deep learning backend

### Supporting Libraries

- **tkinter** - Desktop GUI
- **matplotlib** - Graph visualization
- **pandas** - Data processing
- **numpy** - Numerical computing

---

## Citation

If you use this parser in academic research, please cite:

### This Tool

```bibtex
@software{coptic_dependency_parser_2024,
  title={Coptic Dependency Parser},
  author={Rogaton},
  year={2024},
  url={https://github.com/Rogaton/coptic-dependency-parser}
}
```

### Foundational Resources

**Coptic SCRIPTORIUM:**
```bibtex
@article{zeldes2016coptic,
  title={Coptic SCRIPTORIUM: Digital Resources for the Study of Coptic Literature},
  author={Zeldes, Amir and Schroeder, Caroline T.},
  journal={Digital Humanities},
  year={2016}
}
```

**Stanford Stanza:**
```bibtex
@inproceedings{qi2020stanza,
  title={Stanza: A {Python} Natural Language Processing Toolkit for Many Human Languages},
  author={Qi, Peng and Zhang, Yuhao and Zhang, Yuhui and Bolton, Jason and Manning, Christopher D.},
  booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations},
  year={2020}
}
```

**DiaParser:**
```bibtex
@inproceedings{attardi2021diaparser,
  title={DiaParser: A Fast and Accurate Dependency Parser},
  author={Attardi, Giuseppe and others},
  year={2021}
}
```

---

## License

### Dual License Structure

This project uses a **dual licensing model**:

#### 1. Original Work - CC BY-NC-SA 4.0 (Non-Commercial)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**All original code, documentation, GUI, and project-specific files created by Rogaton are licensed under:**

**Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International**

This means:
- ✅ **Free for academic research, education, and personal use**
- ✅ Share, adapt, and build upon the work
- ✅ Must give attribution and share adaptations under the same license
- ❌ **No commercial use without permission**

#### 2. Third-Party Dependencies

All dependencies retain their original permissive licenses:
- **Stanford Stanza** - Apache License 2.0
- **DiaParser** - Apache License 2.0
- **PyTorch** - BSD 3-Clause License
- **Gradio** - Apache License 2.0
- **NumPy, Pandas, Matplotlib, SciPy, Scikit-learn** - BSD 3-Clause License

See the [LICENSES/](LICENSES/) directory for complete license texts and [LICENSE](LICENSE) for complete details.

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- How to report bugs
- How to suggest features
- Code contribution guidelines
- Testing procedures

---

## Support

### Get Help

- **Issues**: [GitHub Issues](https://github.com/Rogaton/coptic-dependency-parser/issues)
- **Questions**: Use the "question" issue template
- **Bugs**: Use the "bug report" template
- **Features**: Use the "feature request" template

### Known Limitations

- Trained specifically on Coptic - not suitable for other languages
- Quality depends on training data coverage
- May struggle with rare constructions or non-standard orthography
- Best performance on texts similar to SCRIPTORIUM corpus

---

## Acknowledgments

This parser was developed as an open source contribution to Coptic digital humanities, making neural NLP accessible to researchers and students.

Trained on consumer hardware (CPU-only) to demonstrate that advanced NLP is now accessible to individual researchers with modest resources.

Special thanks to:
- The Coptic SCRIPTORIUM team for corpus development
- Stanford NLP Group for Stanza framework
- University of Pisa for DiaParser
- The Coptic studies community

---

## Project Status

**Active Development** - Regular updates and maintenance

Latest release: Version 1.1 (2024)

See [SUMMARY_VERSION_1.1.md](SUMMARY_VERSION_1.1.md) for recent changes.

---

## Related Projects

- **[Coptic SCRIPTORIUM](https://copticscriptorium.org/)** - Coptic corpus and tools
- **[Stanford Stanza](https://stanfordnlp.github.io/stanza/)** - Multi-language NLP toolkit
- **[Universal Dependencies](https://universaldependencies.org/)** - Annotation standards

---

**Start parsing Coptic texts today!** 🎯

```bash
git clone https://github.com/Rogaton/coptic-dependency-parser.git
cd coptic-dependency-parser
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -c "import stanza; stanza.download('cop')"
python3 coptic-parser.py
```
