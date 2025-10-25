# Credits and Attribution

## Coptic Parser - Acknowledgments

This Coptic dependency parser is built upon the excellent work of multiple research projects and open-source contributors. It is essential to acknowledge these sources:

---

## Primary Sources

### 1. **Coptic SCRIPTORIUM**
**Website**: https://copticscriptorium.org/

The Coptic SCRIPTORIUM project provides the foundational NLP tools and trained models for Coptic language processing used in this parser.

**Components from Coptic SCRIPTORIUM:**
- Coptic tokenization models
- Coptic language resources
- Trained NLP models for Coptic text processing
- Coptic linguistic annotations and corpora

**Citation:**
```
Coptic SCRIPTORIUM. "Digital Humanities and Coptic Studies."
Available at: https://copticscriptorium.org/
```

**Key Publications:**
- Zeldes, Amir & Schroeder, Caroline T. (2016). "An NLP Pipeline for Coptic."
  In *Proceedings of LaTeCH 2016*.

**License**: The Coptic SCRIPTORIUM tools and data are released under open licenses.
Please refer to their repository for specific licensing information.

---

### 2. **Stanford CoreNLP - Neural Dependency Parser**
**Website**: https://stanfordnlp.github.io/CoreNLP/

The dependency parsing engine is based on the neural dependency parser from Stanford CoreNLP.

**Components:**
- Neural dependency parsing architecture
- Graph-based parsing algorithms
- CoNLL-U format processing

**Citation:**
```
Manning, Christopher D., Mihai Surdeanu, John Bauer, Jenny Finkel, Steven J. Bethard,
and David McClosky. 2014. The Stanford CoreNLP Natural Language Processing Toolkit.
In Proceedings of 52nd Annual Meeting of the Association for Computational Linguistics:
System Demonstrations, pp. 55-60.
```

**Specific Parser:**
- Dozat, Timothy, and Christopher D. Manning. 2017.
  "Deep Biaffine Attention for Neural Dependency Parsing."
  In *ICLR 2017*.

**License**: Stanford CoreNLP is released under the GNU General Public License (v3 or later).

---

### 3. **Stanza - Stanford NLP Library**
**Website**: https://stanfordnlp.github.io/stanza/

Stanza provides the tokenization pipeline for Coptic text processing.

**Components:**
- Coptic tokenization
- Sentence boundary detection
- Language-specific processing pipelines

**Citation:**
```
Qi, Peng, Yuhao Zhang, Yuhui Zhang, Jason Bolton, and Christopher D. Manning. 2020.
Stanza: A Python Natural Language Processing Toolkit for Many Human Languages.
In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics:
System Demonstrations, pp. 101-108.
```

**License**: Apache License 2.0

---

### 4. **DiaParser - Biaffine Dependency Parser**
**Repository**: https://github.com/Unipisa/diaparser

DiaParser provides the core dependency parsing implementation used for Coptic.

**Components:**
- Biaffine attention mechanism for dependency parsing
- Pre-trained models loading
- CoNLL-U format support

**Citation:**
```
Attardi, Giuseppe, Felice Dell'Orletta, Maria Simi, and Joseph Turian. 2009.
"Accurate Dependency Parsing with a Stacked Multilayer Perceptron."
In Proceedings of Evalita 2009.
```

**License**: Apache License 2.0

---

## Additional Libraries

### Supporting Tools:
- **PyTorch**: Deep learning framework for model execution
- **NumPy**: Numerical computing for data processing
- **Matplotlib**: Visualization of dependency trees
- **Tkinter**: GUI framework for the interactive interface

---

## This Parser Implementation

**Current Implementation**:
- GUI wrapper and visualization tools
- Multi-sentence processing pipeline
- Integration of Stanza + DiaParser for Coptic
- Dependency tree visualization
- HTML export functionality

**Author**: Developed as a user-friendly interface for Coptic dependency parsing
**Purpose**: Educational and research tool for Coptic linguistic analysis
**License**: Please consult with original tool licenses for distribution

---

## How to Cite This Tool

If you use this parser in your research or publications, please cite the original sources above, particularly:

1. **Coptic SCRIPTORIUM** for the Coptic NLP models and resources
2. **Stanford CoreNLP/Stanza** for the parsing framework
3. **DiaParser** for the dependency parsing implementation

### Suggested Citation Format:
```
This research utilized the Coptic Dependency Parser, which integrates tools from
Coptic SCRIPTORIUM (https://copticscriptorium.org/), Stanford CoreNLP/Stanza
(Manning et al., 2014; Qi et al., 2020), and DiaParser (Attardi et al., 2009)
for linguistic analysis of Coptic texts.
```

---

## Contributing

This parser builds on the work of many contributors to Coptic NLP and computational linguistics.
We are grateful for the open-source community that makes such tools possible.

If you encounter issues or have suggestions for improvements, please ensure any modifications
respect the licenses and attribution requirements of the underlying components.

---

## Contact and Support

For questions about:
- **Coptic NLP tools**: Contact Coptic SCRIPTORIUM team
- **Stanza/Stanford CoreNLP**: Refer to Stanford NLP Group documentation
- **DiaParser**: See the DiaParser GitHub repository
- **This GUI tool**: Refer to the local documentation and README files

---

**Last Updated**: 2024
**Documentation Version**: 1.0
