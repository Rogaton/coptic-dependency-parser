# CopticScriptorium-Compatible Tagger

## Overview

This is a command-line tool for annotating Sahidic Coptic texts according to **CopticScriptorium** guidelines, providing:

1. **Morpheme-level tokenization** (segmentation with `|` separators)
2. **POS tagging** using CS tagset (ART, PPER, A, C, V, VBD, COP, etc.)
3. **Lemmatization** following CS rules
4. **TreeTagger-compatible output** (tab-separated format)

## Status: Initial Implementation

✅ **Completed:**
- Core architecture and class structure
- Integration with Till morphology analyzers (reused from dependency parser)
- Text normalization (handles combining diacritics)
- Basic tokenization framework
- Lemmatization rules for articles, pronouns, copulas
- TreeTagger format output
- Command-line interface

🚧 **In Progress:**
- **Morpheme segmentation** (most critical component)
  - Pattern-based segmentation for bound groups
  - Auxiliary + pronoun + verb patterns (e.g., ⲁϥⲥⲱⲧⲙ → ⲁ|ϥ|ⲥⲱⲧⲙ)
  - Preposition + suffix patterns (e.g., ⲙⲙⲟϥ → ⲙⲙⲟ|ϥ)
  - Converter + verb patterns
  - Article + noun patterns

📋 **TODO:**
- Complete POS tagging with context awareness
- Expand lemmatization for all POS classes
- Handle portmanteau tags (AOPT_PPERS, PREP_PPERO, etc.)
- TreeTagger binary integration
- Comprehensive testing against CS corpora
- Performance optimization

## Architecture

### Components

```
coptic_scriptorium_tagger.py
├── MorphemeToken           # Data class for annotated morphemes
├── CopticScriptoriumTokenizer
│   └── segment()           # Morpheme-level tokenization
├── CopticScriptoriumPOSTagger
│   └── tag()               # CS tagset POS tagging
├── CopticScriptoriumLemmatizer
│   └── lemmatize()         # CS lemmatization rules
└── CopticScriptoriumTagger # Main pipeline
    └── process()           # End-to-end annotation
```

### Reused from Dependency Parser

- `CopticTextNormalizer` - removes combining diacritics
- Till morphology analyzers:
  - `coptic_morphology_till` - verb conjugations
  - `coptic_pronouns_prepositions_till` - pronouns/preps (Till §122-172)
  - `coptic_articles_till` - articles (Till §35-50)
  - `coptic_conjunctions_till` - conjunctions
  - `coptic_negation_till` - negation markers

## Usage

### Basic Usage

```bash
# Process from stdin
echo "ⲡ ⲛⲟⲩⲧⲉ ⲡⲉ" | python3 coptic_scriptorium_tagger.py --stdin

# Process file
python3 coptic_scriptorium_tagger.py -i input.txt -o output.tt

# Disable Till analyzers (faster, less accurate)
python3 coptic_scriptorium_tagger.py -i input.txt --no-till
```

### Python API

```python
from coptic_scriptorium_tagger import CopticScriptoriumTagger

# Initialize tagger
tagger = CopticScriptoriumTagger(use_till_analyzers=True)

# Process text
text = "ⲁ ϥ ⲥⲱⲧⲙ"  # "he heard"
tokens = tagger.process(text)

# Output TreeTagger format
tt_output = tagger.process_to_tt_format(text)
print(tt_output)
```

### Output Format

TreeTagger format (tab-separated):

```
FORM    POS     LEMMA
ⲁ       APST    ⲁ
ϥ       PPERS   ⲛⲧⲟϥ
ⲥⲱⲧⲙ   V       ⲥⲱⲧⲙ
```

## CopticScriptorium Tagset

### Part-of-Speech Tags

| Tag | Description | Examples |
|-----|-------------|----------|
| **ART** | Article | ⲡ, ⲧ, ⲛ, ⲟⲩ, ϩⲉⲛ |
| **A*** | Auxiliary (tripartite base) | ⲁ (APST), ⲙⲡ (ANEGPST), ϣⲁ (AAOR), ⲉⲣⲉ (AOPT) |
| **C*** | Converter | ⲉ (CCIRC), ⲉⲧⲉ (CREL), ⲛⲉ (CPRET) |
| **PPER*** | Personal pronoun | ϥ (PPERS), ⲛⲧⲟϥ (PPERI), ⲕ (PPERO) |
| **PDEM** | Demonstrative pronoun | ⲡⲁⲓ, ⲧⲁⲓ, ⲛⲁⲓ |
| **PINT** | Interrogative pronoun | ⲟⲩ, ⲛⲓⲙ |
| **PPOS** | Possessive pronoun | ⲡⲁ, ⲡⲉϥ, ⲧⲉϥ |
| **PREP** | Preposition | ϩⲛ, ⲉ, ⲛⲥⲁ, ⲉϫⲛ |
| **V*** | Verb | ⲥⲱⲧⲙ (V), ⲟⲃⲉ (VSTAT), ⲁϫⲓ (VIMP) |
| **VBD** | Verboid | ⲡⲉϫⲉ, ⲛⲁⲛⲟⲩ |
| **N*** | Noun | ⲣⲱⲙⲉ (N), ⲁⲛⲧⲱⲛⲓⲟⲥ (NPROP) |
| **COP** | Copula | ⲡⲉ, ⲧⲉ, ⲛⲉ |
| **EXIST** | Existential/possessive | ⲟⲩⲛ, ⲙⲛ |
| **FUT** | Future marker | ⲛⲁ |
| **NEG** | Negation | ⲛ, ⲁⲛ, ⲧⲙ, ⲙⲡⲣ |
| **CONJ** | Conjunction | ⲁⲩⲱ, ϫⲉ, ⲏ |
| **ADV** | Adverb | ⲉⲃⲟⲗ, ⲟⲛ |
| **PTC** | Particle | ⲇⲉ, ⲅⲁⲣ, ⲛϭⲓ |
| **NUM** | Numeral | ⲟⲩⲁ, ⲥⲛⲁⲩ |
| **IMOD** | Inflected modifier | ⲧⲏⲣϥ, ϩⲱⲱⲧ |
| **PUNCT** | Punctuation | . , · |

*Note: * indicates multiple fine-grained variants (e.g., APST, ANEGPST for A)

### Portmanteau Tags

Some forms fuse two categories:

| Tag | Example | Meaning |
|-----|---------|---------|
| **AOPT_PPERS** | ⲉϥⲉ | Optative + 3sg.m pronoun |
| **ACOND_PPERS** | ⲉϥϣⲁⲛ | Conditional + 3sg.m pronoun |
| **PREP_PPERO** | ⲉⲣⲟ | Preposition + 2sg.f pronoun (zero) |
| **V_PPERO** | ⲛⲧ | Verb ⲉⲓⲛⲉ + 1sg object |

## Lemmatization Rules

### By POS Class

- **Articles** → masculine singular: ⲡ (for ⲡ/ⲧ/ⲛ/ⲙ/ⲡⲉ/ⲧⲉ/ⲛⲉ)
- **Personal pronouns** → independent forms: ⲁⲛⲟⲕ, ⲛⲧⲟⲕ, ⲛⲧⲟ, ⲛⲧⲟϥ, ⲛⲧⲟⲥ, ⲁⲛⲟⲛ, ⲛⲧⲱⲧⲛ, ⲛⲧⲟⲟⲩ
- **Verbs** → absolute infinitive: ⲥⲱⲧⲙ (for ⲥⲟⲧⲙ/ⲥⲉⲧⲙ/ⲥⲱⲧⲡ/etc.)
- **Possessives** → masculine form: ⲡⲉϥ (for ⲡⲉϥ/ⲧⲉϥ/ⲛⲉϥ)
- **Demonstratives** → masculine form: ⲡⲁⲓ (for ⲡⲁⲓ/ⲧⲁⲓ/ⲛⲁⲓ)
- **Copulas** → masculine: ⲡⲉ (for ⲡⲉ/ⲧⲉ/ⲛⲉ)
- **Auxiliaries** → prenominal form: ⲁ, ⲙⲡⲉ, ⲉⲣⲉ, ⲙⲁⲣⲉ, etc.
- **Converters** → prenominal form: ⲉⲣⲉ, ⲉⲧⲉⲣⲉ, ⲛⲉⲣⲉ
- **Prepositions** → prenominal form: ⲉ, ϩⲛ, ⲛ, ⲛⲥⲁ, etc.
- **Portmanteau** → underscore-separated: ⲉⲣϣⲁⲛ_ⲁⲛⲟⲕ (for ⲉⲓϣⲁⲛ)

## Testing

```bash
# Run test suite
python3 test_cs_tagger.py

# Compare against corpus
python3 test_cs_tagger.py
```

Test corpora available in: `~/copticNLP/corpora/`

## Key Differences from Dependency Parser

| Feature | Dependency Parser | CS Tagger |
|---------|------------------|-----------|
| **Tokenization** | Word-level (Stanza) | Morpheme-level (CS) |
| **POS Tagset** | Universal Dependencies | CopticScriptorium |
| **Output** | CoNLL-U + dependency trees | TreeTagger format |
| **Use Case** | Syntactic analysis | Corpus annotation |
| **Interface** | GUI + visualization | Command-line |

## Development Roadmap

### Phase 1: Core Tokenization (Current)
- [x] Basic architecture
- [x] Till analyzer integration
- [ ] Pattern-based morpheme segmentation
- [ ] Bound group splitting (ⲁϥⲥⲱⲧⲙ → ⲁ|ϥ|ⲥⲱⲧⲙ)

### Phase 2: POS Tagging
- [ ] Context-aware tagging
- [ ] Converter vs. auxiliary disambiguation
- [ ] Portmanteau tag detection
- [ ] Fine-grained tag assignment

### Phase 3: Lemmatization
- [ ] Complete verb lemmatization
- [ ] Irregular forms handling
- [ ] Noun plural forms
- [ ] Compound verb detection

### Phase 4: Integration & Testing
- [ ] TreeTagger binary integration
- [ ] Batch corpus processing
- [ ] Accuracy evaluation vs. gold standard
- [ ] Performance optimization

## References

- **CopticScriptorium Project**: https://copticscriptorium.org/
- **POS Tagset Documentation**: scriptorium_tagset_documentation.pdf
- **Lemmatization Guidelines**: Coptic SCRIPTORIUM lemmatization guidelines.pdf
- **Transcription Guidelines**: SCRIPTORIUMDiplTranscriptionGuidelines.pdf
- **Test Corpora**: ~/copticNLP/corpora/

## Citation

If you use this tool, please cite:

```
Zeldes, Amir & Caroline T. Schroeder (2016).
"An NLP Pipeline for Coptic."
In: Proceedings of the 10th SIGHUM Workshop on Language Technology
for Cultural Heritage, Social Sciences, and Humanities.
Berlin: Association for Computational Linguistics, 146-155.
```

## License

Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International

Same license as the original Coptic Dependency Parser.
