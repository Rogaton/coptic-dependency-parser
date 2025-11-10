#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coptic Parser Corpus Testing Framework
=======================================

Tests the Coptic Dependency Parser with Till's grammar modules
on authentic CopticScriptorium corpora.

Usage:
    python3 test_parser_on_corpus.py <conllu_file> [--sentences N]

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict, Counter

def extract_sentences_from_conllu(conllu_path: Path, max_sentences: int = None) -> List[Tuple[str, str, str]]:
    """
    Extract Coptic sentences from CoNLL-U file.

    Returns:
        List of (sent_id, text, english_translation) tuples
    """
    sentences = []

    with open(conllu_path, 'r', encoding='utf-8') as f:
        current_id = None
        current_text = None
        current_en = None

        for line in f:
            line = line.strip()

            if line.startswith('# sent_id = '):
                current_id = line.replace('# sent_id = ', '')
            elif line.startswith('# text = '):
                current_text = line.replace('# text = ', '')
            elif line.startswith('# text_en = '):
                current_en = line.replace('# text_en = ', '')
            elif line == '' and current_id and current_text:
                # End of sentence
                sentences.append((current_id, current_text, current_en or ""))
                current_id = None
                current_text = None
                current_en = None

                if max_sentences and len(sentences) >= max_sentences:
                    break

    return sentences


def analyze_with_till_modules(text: str) -> Dict[str, List[str]]:
    """
    Analyze text using Till's grammar modules.

    Returns dictionary of detected patterns.
    """
    from coptic_dialect_handler import Dialect
    from coptic_morphology_till import create_morphology_analyzer_till
    from coptic_pronouns_prepositions_till import create_pronouns_prepositions_analyzer_till
    from coptic_articles_till import create_articles_analyzer_till
    from coptic_conjunctions_till import create_conjunctions_analyzer_till
    from coptic_negation_till import create_negation_analyzer_till
    from coptic_proper_names import is_proper_name

    # Initialize analyzers
    morphology = create_morphology_analyzer_till(Dialect.SAHIDIC)
    pronouns_preps = create_pronouns_prepositions_analyzer_till(Dialect.SAHIDIC)
    articles = create_articles_analyzer_till(Dialect.SAHIDIC)
    conjunctions = create_conjunctions_analyzer_till(Dialect.SAHIDIC)
    negation = create_negation_analyzer_till(Dialect.SAHIDIC)

    # Tokenize (simple split on spaces and punctuation)
    tokens = re.findall(r'[ⲁ-ⲱϣϥϧϩϫϭϯ]+|[^\s]', text)

    results = {
        'articles': [],
        'pronouns': [],
        'prepositions': [],
        'conjunctions': [],
        'negations': [],
        'morphology': []
    }

    for token in tokens:
        # Skip proper names and ecclesiastical terms to reduce false positives
        if is_proper_name(token):
            continue

        # Articles (§35-50)
        article_result = articles.identify(token)
        if article_result:
            gender_str = f"{article_result.gender}." if article_result.gender else ""
            results['articles'].append(f"{token} → {article_result.article_type} {gender_str}{article_result.number}")

        # Pronouns & Prepositions (§122-172)
        # Try exact match first
        pron_prep_result = pronouns_preps.identify_form(token)

        # If no exact match, try substring matching for bound prepositions (ϩⲛⲧⲉⲣⲏⲙⲟⲥ = ϩⲛ + ⲧⲉⲣⲏⲙⲟⲥ)
        if not pron_prep_result and len(token) > 2:
            # Try common prefixes (prepositions often appear at start)
            for prefix_len in [2, 3, 4, 5]:
                if len(token) >= prefix_len:
                    prefix = token[:prefix_len]
                    pron_prep_result = pronouns_preps.identify_form(prefix)
                    if pron_prep_result and pron_prep_result[1] == 'PREP':
                        # Found bound preposition
                        break
                    else:
                        pron_prep_result = None

        if pron_prep_result:
            lemma, pos, features, section = pron_prep_result
            # Map POS tags to readable form types
            pos_map = {
                'PDEM': 'demonstrative',
                'PPOSS': 'possessive',
                'PINT': 'interrogative',
                'PIND': 'indefinite',
                'PREP': 'preposition',
                'ADV': 'adverbial'
            }
            form_type = pos_map.get(pos, pos)

            if pos in ['PDEM', 'PPOSS', 'PINT', 'PIND']:
                # Pronouns
                person = features.get('Person', features.get('person', ''))
                gender = features.get('Gender', features.get('gender', ''))
                number = features.get('Number', features.get('number', ''))
                feat_str = '/'.join(filter(None, [person, gender, number]))
                results['pronouns'].append(f"{token} → {form_type} {feat_str}" if feat_str else f"{token} → {form_type}")
            elif pos in ['PREP', 'ADV']:
                meaning = features.get('Meaning', features.get('meaning', ''))
                results['prepositions'].append(f"{token} → {meaning}" if meaning else f"{token} → {form_type}")

        # Conjunctions (§292-304)
        conj_result = conjunctions.identify(token)
        if conj_result:
            results['conjunctions'].append(f"{token} → {conj_result.conj_type}: {conj_result.meaning} ({conj_result.subtype})")

        # Negation (§309-319)
        neg_result = negation.identify_negation(token)
        if neg_result:
            results['negations'].append(f"{token} → {neg_result.neg_type}: {neg_result.meaning}")

        # Morphology (§245-268)
        morph_result = morphology.segment_word(token)
        if morph_result and len(morph_result) > 1:  # Only show if segmented
            segments = " + ".join([f"{s.form}({s.pos})" for s in morph_result])
            results['morphology'].append(f"{token} → {segments}")

    return results


def test_corpus(conllu_path: Path, max_sentences: int = 10):
    """
    Test parser on corpus and generate report.
    """
    print("=" * 80)
    print("COPTIC PARSER - CORPUS TESTING WITH TILL'S GRAMMAR")
    print("=" * 80)
    print(f"\nCorpus: {conllu_path.name}")
    print(f"Testing on: {max_sentences} sentences\n")

    # Extract sentences
    print("📖 Extracting sentences from CoNLL-U...")
    sentences = extract_sentences_from_conllu(conllu_path, max_sentences)
    print(f"✓ Extracted {len(sentences)} sentences\n")

    # Statistics
    stats = {
        'total_tokens': 0,
        'patterns_found': defaultdict(int)
    }

    # Analyze each sentence
    for i, (sent_id, text, text_en) in enumerate(sentences, 1):
        print("-" * 80)
        print(f"SENTENCE {i}/{len(sentences)}")
        print(f"ID: {sent_id}")
        print(f"Coptic: {text}")
        if text_en:
            print(f"English: {text_en}")
        print()

        # Count tokens
        tokens = re.findall(r'[ⲁ-ⲱϣϥϧϩϫϭϯ]+', text)
        stats['total_tokens'] += len(tokens)

        # Analyze with Till modules
        results = analyze_with_till_modules(text)

        # Display results by module
        if results['articles']:
            print("📰 ARTICLES (Till §35-50):")
            for item in results['articles']:
                print(f"   • {item}")
                stats['patterns_found']['articles'] += 1

        if results['pronouns']:
            print("👤 PRONOUNS (Till §122-172):")
            for item in results['pronouns']:
                print(f"   • {item}")
                stats['patterns_found']['pronouns'] += 1

        if results['prepositions']:
            print("🔗 PREPOSITIONS (Till §173-191):")
            for item in results['prepositions']:
                print(f"   • {item}")
                stats['patterns_found']['prepositions'] += 1

        if results['conjunctions']:
            print("🔀 CONJUNCTIONS (Till §292-304):")
            for item in results['conjunctions']:
                print(f"   • {item}")
                stats['patterns_found']['conjunctions'] += 1

        if results['negations']:
            print("🚫 NEGATIONS (Till §309-319):")
            for item in results['negations']:
                print(f"   • {item}")
                stats['patterns_found']['negations'] += 1

        if results['morphology']:
            print("🔬 MORPHOLOGY (Till §245-268):")
            for item in results['morphology'][:3]:  # Show first 3
                print(f"   • {item}")
            if len(results['morphology']) > 3:
                print(f"   ... and {len(results['morphology']) - 3} more")
            stats['patterns_found']['morphology'] += len(results['morphology'])

        if not any(results.values()):
            print("   (No Till patterns detected in this sentence)")

        print()

    # Final statistics
    print("=" * 80)
    print("TESTING SUMMARY")
    print("=" * 80)
    print(f"Sentences analyzed: {len(sentences)}")
    print(f"Total tokens: {stats['total_tokens']}")
    print(f"\nTill's Grammar Patterns Detected:")
    print(f"  • Articles (§35-50): {stats['patterns_found']['articles']}")
    print(f"  • Pronouns (§122-172): {stats['patterns_found']['pronouns']}")
    print(f"  • Prepositions (§173-191): {stats['patterns_found']['prepositions']}")
    print(f"  • Conjunctions (§292-304): {stats['patterns_found']['conjunctions']}")
    print(f"  • Negations (§309-319): {stats['patterns_found']['negations']}")
    print(f"  • Morphological segmentations (§245-268): {stats['patterns_found']['morphology']}")
    print(f"\nTotal patterns found: {sum(stats['patterns_found'].values())}")
    print(f"Coverage: {sum(stats['patterns_found'].values())}/{stats['total_tokens']} tokens ({100*sum(stats['patterns_found'].values())/stats['total_tokens']:.1f}%)")
    print("\n✓ Testing complete!")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 test_parser_on_corpus.py <conllu_file> [--sentences N]")
        print("\nExample:")
        print("  python3 test_parser_on_corpus.py ~/copticNLP/corpora/helias/helias_CONLLU/helias_encomium.conllu --sentences 5")
        sys.exit(1)

    conllu_path = Path(sys.argv[1])
    max_sentences = 10  # Default

    if '--sentences' in sys.argv:
        idx = sys.argv.index('--sentences')
        if idx + 1 < len(sys.argv):
            max_sentences = int(sys.argv[idx + 1])

    if not conllu_path.exists():
        print(f"Error: File not found: {conllu_path}")
        sys.exit(1)

    test_corpus(conllu_path, max_sentences)
