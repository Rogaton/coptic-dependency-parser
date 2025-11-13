#!/usr/bin/env python3
"""
Comparison Tool: Dependency Parser vs. CopticScriptorium Tagger

Side-by-side comparison of outputs from both parsing approaches.

Author: André Linden (2025)
"""

import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from coptic_scriptorium_tagger import CopticScriptoriumTagger


def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_subheader(title):
    """Print formatted subsection header"""
    print("\n" + "-" * 80)
    print(f"  {title}")
    print("-" * 80)


def compare_parsers(text):
    """
    Compare output from both parsers for the same input text.

    Args:
        text: Coptic text to analyze
    """
    print_header("PARSER COMPARISON")
    print(f"\nInput Text: {text}\n")

    # ========================================================================
    # CopticScriptorium Tagger
    # ========================================================================
    print_subheader("CopticScriptorium Tagger (Morpheme-Level)")

    cs_tagger = CopticScriptoriumTagger(use_till_analyzers=True)
    cs_output = cs_tagger.process_to_tt_format(text)

    print("TreeTagger Format (FORM | POS | LEMMA):")
    print(cs_output)

    # Show morpheme segmentation
    tokens = cs_tagger.process(text)
    morphemes = []
    current_word = []

    for i, token in enumerate(tokens):
        current_word.append(token.form)
        # Check if next token is part of same word (heuristic)
        if i == len(tokens) - 1 or (i < len(tokens) - 1 and
                                    tokens[i+1].pos in ['PUNCT', 'ART', 'WORD'] and
                                    token.pos not in ['AUX', 'CONV', 'PREP']):
            morphemes.append('|'.join(current_word))
            current_word = []

    if current_word:
        morphemes.append('|'.join(current_word))

    print(f"\nMorpheme Segmentation (with | separators):")
    print(' '.join(morphemes))

    # ========================================================================
    # Dependency Parser (simulated - requires running coptic-parser.py)
    # ========================================================================
    print_subheader("Dependency Parser (Word-Level + Syntax)")

    print("""
NOTE: To see dependency parser output, run:
    python3 coptic-parser.py

The dependency parser provides:
- Word-level tokenization (not morpheme-level)
- Universal Dependencies POS tags (VERB, NOUN, DET, PRON, etc.)
- Dependency relations (nsubj, obj, root, etc.)
- Syntactic tree visualization
- Head-dependent relationships

Example output format:
    ID  FORM    LEMMA   UPOS    HEAD    DEPREL
    1   ⲁϥⲥⲱⲧⲙ  ⲁϥⲥⲱⲧⲙ  VERB    0       root
    2   ⲙⲙⲟϥ   ⲙⲙⲟϥ   PRON    1       obj

Use Cases:
- Dependency Parser: Syntactic analysis, sentence structure, grammatical relations
- CS Tagger: Morphology, corpus annotation, lexicography, TreeTagger training
""")

    # ========================================================================
    # Comparison Table
    # ========================================================================
    print_subheader("Feature Comparison")

    comparison = [
        ("Feature", "CS Tagger", "Dependency Parser"),
        ("─" * 25, "─" * 25, "─" * 25),
        ("Tokenization", "Morpheme-level", "Word-level"),
        ("POS Tagset", "CopticScriptorium", "Universal Dependencies"),
        ("Segmentation", "ⲁ|ϥ|ⲥⲱⲧⲙ", "ⲁϥⲥⲱⲧⲙ"),
        ("Syntax", "No", "Yes (dependencies)"),
        ("Lemmatization", "CS rules", "Stanza/Till"),
        ("Output", "TreeTagger format", "CoNLL-U + graphs"),
        ("Use Case", "Corpus annotation", "Syntax analysis"),
        ("Interface", "Command-line", "GUI + CLI"),
    ]

    for row in comparison:
        print(f"{row[0]:25} | {row[1]:25} | {row[2]:25}")

    print()


def main():
    """Main comparison tool"""
    print("=" * 80)
    print("  COPTIC PARSER COMPARISON TOOL")
    print("=" * 80)
    print("""
This tool compares two complementary approaches to Coptic NLP:

1. CopticScriptorium Tagger - Morpheme-level annotation
2. Dependency Parser - Word-level syntactic analysis

Both tools share underlying components (Till analyzers, normalization)
but serve different research purposes.
    """)

    # Test examples
    examples = [
        "ⲁϥⲥⲱⲧⲙ ⲙⲙⲟϥ",        # he heard him
        "ⲡ ⲛⲟⲩⲧⲉ ⲡⲉ",         # God is
        "ⲉϥϫⲱ ⲙⲙⲟⲥ",          # he saying it
        "ⲙⲡⲓⲥⲱⲧⲙ",            # I didn't hear
    ]

    for i, example in enumerate(examples, 1):
        print_header(f"EXAMPLE {i}")
        compare_parsers(example)

    # Summary
    print_header("SUMMARY")
    print("""
Both parsers complement each other:

CS TAGGER excels at:
✓ Morpheme segmentation (bound groups → morphemes)
✓ Fine-grained Coptic-specific POS tags
✓ Corpus annotation following CS standards
✓ TreeTagger model training
✓ Lexicographic analysis

DEPENDENCY PARSER excels at:
✓ Syntactic structure analysis
✓ Grammatical relation identification
✓ Sentence-level parsing
✓ Visualization of parse trees
✓ Cross-linguistic comparison (UD framework)

RECOMMENDATION:
- Use CS Tagger for corpus linguistics, morphology, and standardized annotation
- Use Dependency Parser for syntax, semantics, and computational linguistics
- Use BOTH for comprehensive linguistic analysis!

For more information:
- CS Tagger: python3 coptic_scriptorium_tagger.py --help
- CS Examples: python3 examples_cs_tagger.py
- Dependency Parser: python3 coptic-parser.py (GUI application)
    """)
    print("=" * 80)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        # User provided text
        text = ' '.join(sys.argv[1:])
        compare_parsers(text)
    else:
        # Run examples
        main()
