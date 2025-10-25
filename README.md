---
title: Coptic Dependency Parser
emoji: 📜
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - coptic
  - dependency-parsing
  - nlp
  - ancient-languages
  - digital-humanities
  - stanza
  - coptic-scriptorium
  - linguistics
  - pos-tagging
  - lemmatization
language:
  - cop
---

# Coptic Dependency Parser

Neural dependency parser for Coptic text with part-of-speech tagging and lemmatization.

Try it directly in your browser - no installation required!

## What This Demo Does

This parser performs comprehensive linguistic analysis of Coptic text:

- **Tokenization**: Splits text into sentences and individual words
- **POS Tagging**: Identifies parts of speech (NOUN, VERB, DET, etc.) using Universal Dependencies tagset
- **Lemmatization**: Finds dictionary/base forms of words
- **Dependency Parsing**: Analyzes grammatical relationships between words (subject, object, modifier, etc.)

## How to Use

1. Enter Coptic text in the input box (single or multiple sentences)
2. Click "Parse Text" or press Enter
3. View results in two formats:
   - **Dependency Table**: Visual table with all linguistic annotations
   - **Text Output**: Detailed text listing of all relationships

## Example Input

```
ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ
```
(Translation: "I am God")

The parser will show you:
- Each word's part of speech
- Its lemma (dictionary form)
- Which word it depends on
- The grammatical relationship

## Technical Details

### Models and Training

- **Base Framework**: [Stanford Stanza](https://stanfordnlp.github.io/stanza/) for Coptic NLP
- **Parser**: [DiaParser](https://github.com/Unipisa/diaparser) with biaffine attention mechanism
- **Training Data**: [Coptic SCRIPTORIUM](https://copticscriptorium.org/) corpus
- **Training Hardware**: CPU-only (Intel, 64GB RAM)
- **Training Time**: 12 hours on complete Coptic SCRIPTORIUM dataset
- **Architecture**: Neural dependency parser with BiLSTM + biaffine attention

### Performance

**Real-world benchmarks**:
- **Desktop (local)**: Instant parsing for typical texts
- **Web demo (HF CPU)**: 67 sentences, 1,337 words in < 7 seconds (~190 words/second)
- Handles single and multi-sentence texts efficiently
- Processes long documents (tested up to 67+ sentences)
- Follows Universal Dependencies annotation standards
- Trained on authentic Coptic texts from diverse genres

## Built On Open Source

This parser integrates several excellent open source projects:

### Primary Components

- **[Coptic SCRIPTORIUM](https://copticscriptorium.org/)**: Training corpus and linguistic annotations
  - Zeldes, A. & Schroeder, C. T. (2016). "Coptic SCRIPTORIUM: Digital Resources for the Study of Coptic Literature"
- **[Stanford Stanza](https://stanfordnlp.github.io/stanza/)**: NLP pipeline framework
  - Qi, P., Zhang, Y., Zhang, Y., Bolton, J., & Manning, C. D. (2020). "Stanza: A Python Natural Language Processing Toolkit for Many Human Languages"
- **[DiaParser](https://github.com/Unipisa/diaparser)**: Neural dependency parser
  - Attardi, G. et al. (2021). "DiaParser: A Fast and Accurate Dependency Parser"

### Supporting Libraries

- PyTorch: Deep learning framework
- Gradio: Web interface
- NumPy, Pandas: Data processing
- Matplotlib: Visualization

## Use Cases

Perfect for:

- **Coptic Language Students**: Learn grammatical structure through visualization
- **Digital Humanities Researchers**: Analyze Coptic texts computationally
- **Linguists**: Study syntactic patterns in ancient Coptic
- **Corpus Linguists**: Extract dependency statistics from texts
- **NLP Researchers**: Experiment with low-resource language parsing

## Limitations

- Trained specifically on Coptic - not suitable for other languages
- Quality depends on training data coverage
- May struggle with very rare constructions or non-standard orthography
- Best performance on texts similar to Coptic SCRIPTORIUM corpus genres

## Citation

If you use this parser in academic research, please cite:

### This Tool
```
@software{coptic_dependency_parser_2024,
  title={Coptic Dependency Parser},
  author={Rogaton},
  year={2024},
  url={https://github.com/Rogaton/coptic-dependency-parser}
}
```

### Foundational Resources

**Coptic SCRIPTORIUM:**
```
@article{zeldes2016coptic,
  title={Coptic SCRIPTORIUM: Digital Resources for the Study of Coptic Literature},
  author={Zeldes, Amir and Schroeder, Caroline T.},
  journal={Digital Humanities},
  year={2016}
}
```

**Stanford Stanza:**
```
@inproceedings{qi2020stanza,
  title={Stanza: A {Python} Natural Language Processing Toolkit for Many Human Languages},
  author={Qi, Peng and Zhang, Yuhao and Zhang, Yuhui and Bolton, Jason and Manning, Christopher D.},
  booktitle={Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics: System Demonstrations},
  year={2020}
}
```

## License

**Apache License 2.0**

This project is licensed under the Apache License 2.0, which allows free use, modification, and distribution. All dependencies (Stanza, DiaParser, PyTorch, Gradio) are under permissive open source licenses. See [LICENSE](https://github.com/Rogaton/coptic-dependency-parser/blob/main/LICENSE) for details.

## Links

- **Full Application** (desktop GUI with visualization): [GitHub Repository](https://github.com/Rogaton/coptic-dependency-parser)
- **Documentation**: Comprehensive guides available in GitHub repo
- **Issues/Questions**: [GitHub Issues](https://github.com/Rogaton/coptic-dependency-parser/issues)

## About the Developer

This parser was developed as an open source contribution to Coptic digital humanities, making neural NLP tools accessible to researchers and students without requiring extensive computational resources or programming expertise.

Trained on consumer hardware (CPU-only MiniPC) to demonstrate that advanced NLP is now accessible to individual researchers with modest resources.

---

**Try it now!** Enter your Coptic text above and explore the grammatical structure. ⬆️
