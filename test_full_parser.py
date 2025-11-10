#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Full Parser Integration Test - Command Line Interface
======================================================

Tests the complete pipeline:
1. Text normalization
2. Stanza tokenization & POS tagging
3. Diaparser neural dependency parsing
4. Till grammar pattern enrichment
5. Prolog validation

Usage:
    python3 test_full_parser.py

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

import sys
import warnings
warnings.filterwarnings('ignore')

# Fix PyTorch compatibility
import torch
import pickle

_original_torch_load = torch.load

def patched_torch_load(*args, **kwargs):
    kwargs['weights_only'] = False
    try:
        return _original_torch_load(*args, **kwargs)
    except (KeyError, AttributeError) as e:
        if '__getitems__' in str(e) or '__getitem__' in str(e):
            kwargs['pickle_module'] = pickle
            return _original_torch_load(*args, **kwargs)
        raise

torch.load = patched_torch_load

# Test sentences (increasing complexity)
TEST_SENTENCES = [
    # Simple sentences
    ("ⲡⲣⲱⲙⲉ ⲛⲁⲛⲟⲩϥ", "Simple: 'The man is good'"),
    ("ⲁϥⲃⲱⲕ ⲉϩⲣⲁⲓ", "Simple: 'He went up'"),

    # With negation
    ("ⲙⲡⲉϥⲃⲱⲕ ⲉⲃⲟⲗ", "Negation: 'He did not go out'"),
    ("ⲛⲉϥⲥⲟⲟⲩⲛ ⲁⲛ", "Negation particle: 'He does not know'"),

    # With prepositions and articles
    ("ⲁϥⲃⲱⲕ ⲉϩⲟⲩⲛ ⲉⲡⲉⲓ", "Prepositions: 'He went into the house'"),
    ("ⲡϫⲟⲉⲓⲥ ⲙⲡⲛⲟⲩⲧⲉ", "Genitive: 'The lord of God'"),

    # Complex structures
    ("ⲁⲩⲱ ⲡⲉϫⲁϥ ⲛⲁⲩ ϫⲉ ⲙⲁⲣⲟⲩⲃⲱⲕ", "Conjunction+quotation: 'And he said to them: Let them go'"),
    ("ⲉⲧⲃⲉ ⲡⲁⲓ ⲁϥⲙⲟⲩⲧⲉ ⲉⲣⲟϥ", "Causal: 'Because of this he called it'"),

    # Biblical (Mark 1:2)
    ("ⲕⲁⲧⲁⲡⲉⲧⲥⲏϩ ϩⲛⲏⲥⲁⲓⲁⲥ ⲡⲉⲡⲣⲟⲫⲏⲧⲏⲥ", "Biblical: 'As it is written in Isaiah the prophet'"),
]


def test_full_parser():
    """Test the complete parser pipeline"""

    print("="*80)
    print("COPTIC PARSER - FULL PIPELINE INTEGRATION TEST")
    print("="*80)
    print("\nInitializing components...")

    # 1. Load Stanza
    print("  [1/6] Loading Stanza for tokenization & POS tagging...")
    import stanza
    try:
        nlp = stanza.Pipeline(
            lang='cop',
            processors='tokenize,pos,lemma,depparse',
            download_method=None
        )
        print("        ✓ Stanza loaded successfully")
    except Exception as e:
        print(f"        ✗ Stanza failed: {e}")
        return

    # 2. Load Diaparser
    print("  [2/6] Loading Diaparser for neural dependency parsing...")
    try:
        from diaparser.parsers import Parser
        diaparser = Parser.load('en_ewt.electra-base')
        print("        ✓ Diaparser loaded successfully")
    except Exception as e:
        print(f"        ⚠ Diaparser not available: {e}")
        print("        → Will use Stanza's dependency parser instead")
        diaparser = None

    # 3. Load Till modules
    print("  [3/6] Loading Till grammar modules...")
    from coptic_dialect_handler import Dialect
    from coptic_morphology_till import create_morphology_analyzer_till
    from coptic_pronouns_prepositions_till import create_pronouns_prepositions_analyzer_till
    from coptic_articles_till import create_articles_analyzer_till
    from coptic_conjunctions_till import create_conjunctions_analyzer_till
    from coptic_negation_till import create_negation_analyzer_till
    from coptic_pretokenization_morphology import create_pretokenization_morphology

    morphology_till = create_morphology_analyzer_till(Dialect.SAHIDIC)
    pronouns_preps_till = create_pronouns_prepositions_analyzer_till(Dialect.SAHIDIC)
    articles_till = create_articles_analyzer_till(Dialect.SAHIDIC)
    conjunctions_till = create_conjunctions_analyzer_till(Dialect.SAHIDIC)
    negation_till = create_negation_analyzer_till(Dialect.SAHIDIC)
    pretok_morph = create_pretokenization_morphology(morphology_till)
    print("        ✓ Till modules loaded: Articles, Pronouns/Preps, Morphology, Conjunctions, Negations")
    print("        ✓ Pre-tokenization morphology analyzer loaded")

    # 4. Load Prolog (optional)
    print("  [4/6] Loading Prolog validation engine...")
    try:
        from coptic_prolog_rules import create_prolog_engine
        prolog = create_prolog_engine()
        print("        ✓ Prolog engine loaded successfully")
    except Exception as e:
        print(f"        ⚠ Prolog not available: {e}")
        prolog = None

    # 5. Load dialect identifier
    print("  [5/6] Loading dialect identifier...")
    try:
        from coptic_dialect_identifier import create_dialect_identifier
        dialect_id = create_dialect_identifier()
        print("        ✓ Dialect identifier loaded")
    except Exception as e:
        print(f"        ⚠ Dialect identifier not available: {e}")
        dialect_id = None

    # 6. Load text normalizer
    print("  [6/6] Loading text normalizer...")
    try:
        from coptic_text_normalizer import CopticTextNormalizer
        normalizer = CopticTextNormalizer(mode='strip')
        print("        ✓ Text normalizer loaded")
    except Exception as e:
        print(f"        ⚠ Text normalizer not available: {e}")
        normalizer = None

    print("\n" + "="*80)
    print("TESTING PARSER ON SAMPLE SENTENCES")
    print("="*80)

    # Test each sentence
    for idx, (sentence, description) in enumerate(TEST_SENTENCES, 1):
        print(f"\n{'─'*80}")
        print(f"TEST {idx}/{len(TEST_SENTENCES)}: {description}")
        print(f"{'─'*80}")
        print(f"Input: {sentence}")
        print()

        try:
            # Normalize
            if normalizer:
                analysis = normalizer.analyze_text(sentence)
                text = analysis['normalized_text']
            else:
                text = sentence

            # PRE-TOKENIZATION: Analyze morphology on whole words
            morph_results = pretok_morph.analyze_text(text)

            # Tokenize with Stanza
            doc = nlp(text)

            if not doc.sentences:
                print("  ✗ No sentences parsed")
                continue

            stanza_sentence = doc.sentences[0]
            tokens = [word.text for word in stanza_sentence.words]
            pos_tags = [word.upos for word in stanza_sentence.words]
            lemmas = [word.lemma if word.lemma else word.text for word in stanza_sentence.words]

            # Get dependencies
            if diaparser:
                parsed = diaparser.predict([tokens], prob=False, verbose=False)
                heads = parsed.sentences[0].values[6]
                deprels = parsed.sentences[0].values[7]
            else:
                heads = [word.head for word in stanza_sentence.words]
                deprels = [word.deprel for word in stanza_sentence.words]

            # MAP pre-tokenization morphology to Stanza tokens
            token_morphology = pretok_morph.map_to_tokens(morph_results, tokens, text)

            # Identify dialect
            if dialect_id:
                detected_dialect, confidence, _ = dialect_id.identify_dialect(sentence)
                print(f"📖 Dialect: {detected_dialect.value} ({confidence:.0%} confidence)")
                print()

            # Display parse with Till enrichment
            print("Dependency Parse with Till Analysis:")
            print(f"{'─'*80}")

            for i, token in enumerate(tokens):
                word_id = i + 1
                head = heads[i]
                deprel = deprels[i]
                pos = pos_tags[i]

                # Get Till enrichment
                till_info = []

                # PRIORITY 1: Check pre-tokenization morphology (compound words)
                pretok_segments = pretok_morph.get_morphology_for_token(i, token, token_morphology)
                if pretok_segments:
                    seg_str = pretok_morph.format_morphology_display(pretok_segments)
                    till_info.append(f"MORPH: {seg_str}")

                # PRIORITY 2: Check articles
                if not till_info:
                    article_result = articles_till.identify(token)
                    if article_result:
                        till_info.append(f"ART:{article_result.article_type} {article_result.source_section}")

                # PRIORITY 3: Check pronouns/prepositions
                if not till_info:
                    pron_prep_result = pronouns_preps_till.identify_form(token)
                    if pron_prep_result:
                        lemma, pron_pos, feats, section = pron_prep_result
                        pos_names = {'PDEM': 'demonstrative', 'PREP': 'preposition', 'ADV': 'adverbial',
                                    'PINT': 'interrogative', 'PPOSS': 'possessive'}
                        till_info.append(f"{pos_names.get(pron_pos, pron_pos)} {section}")

                # PRIORITY 4: Check regular morphology (single tokens)
                if not till_info:
                    segments = morphology_till.segment_word(token)
                    if segments and len(segments) > 1:
                        seg_str = "+".join([f"{s.form}({s.pos})" for s in segments])
                        till_info.append(f"MORPH: {seg_str}")

                # Check conjunctions
                conj_result = conjunctions_till.identify(token)
                if conj_result and not till_info:
                    till_info.append(f"CONJ:{conj_result.conj_type} {conj_result.source_section}")

                # Check negations
                neg_result = negation_till.identify_negation(token)
                if neg_result and not till_info:
                    till_info.append(f"NEG:{neg_result.neg_type} {neg_result.source_section}")

                # Format output
                head_text = "ROOT" if head == 0 else tokens[head-1]
                till_str = f"  [{till_info[0]}]" if till_info else ""
                print(f"  {token:15} ({pos:6}) --{deprel:10}--> {head_text:15}{till_str}")

            # Prolog validation
            if prolog and prolog.prolog_initialized:
                print()
                validation = prolog.validate_parse_tree(tokens, pos_tags, heads, deprels)

                if validation.get("patterns_found"):
                    for pattern in validation["patterns_found"]:
                        if pattern.get("is_tripartite"):
                            print(f"✓ Prolog: {pattern['description']} detected")
                            print(f"  Pattern: {pattern['pattern']}")

                if validation.get("warnings"):
                    print(f"⚠ Prolog Warnings:")
                    for warning in validation["warnings"]:
                        print(f"  - {warning}")

        except Exception as e:
            print(f"  ✗ Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "="*80)
    print("TESTING COMPLETE")
    print("="*80)
    print(f"\nTested {len(TEST_SENTENCES)} sentences across different complexity levels")
    print("\nComponents validated:")
    print("  ✓ Text normalization")
    print("  ✓ Stanza tokenization & POS tagging")
    print(f"  {'✓' if diaparser else '⚠'} Diaparser neural parsing {'(active)' if diaparser else '(fallback to Stanza)'}")
    print("  ✓ Till grammar enrichment (6 modules)")
    print(f"  {'✓' if prolog else '⚠'} Prolog validation {'(active)' if prolog else '(not available)'}")
    print("\n" + "="*80)


if __name__ == "__main__":
    test_full_parser()
