#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baseline Model Evaluation
==========================

Evaluates current parser performance to establish baseline metrics before training.

Measures:
1. Parsing success rate
2. Till pattern coverage (articles, prepositions, morphology, conjunctions, negations)
3. Dialect identification accuracy
4. Performance (tokens/second)
5. Parse tree statistics

Usage:
    python3 evaluate_baseline.py [corpus_files...]

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

import sys
import time
import warnings
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

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


def evaluate_baseline(corpus_files=None):
    """Run comprehensive baseline evaluation"""

    print("=" * 80)
    print("COPTIC PARSER - BASELINE MODEL EVALUATION")
    print("=" * 80)
    print()

    # Default corpora if none specified
    if not corpus_files:
        import os
        corpus_files = []
        test_files = [
            'corpus_test_mark.txt',
            'corpus_test_pachomius.txt',
            'corpus_test_papyri.txt',
            'corpus_test_shenoute.txt'
        ]
        for f in test_files:
            if os.path.exists(f):
                corpus_files.append(f)

    if not corpus_files:
        print("❌ No corpus files found")
        print("Usage: python3 evaluate_baseline.py [corpus_files...]")
        return

    print(f"📂 Evaluating {len(corpus_files)} corpora")
    print()

    # Load components
    print("🔧 Loading parser components...")
    print()

    # 1. Load Stanza
    print("  [1/5] Loading Stanza...")
    import stanza
    try:
        nlp = stanza.Pipeline(
            lang='cop',
            processors='tokenize,pos,lemma,depparse',
            download_method=None
        )
        print("        ✓ Stanza loaded")
    except Exception as e:
        print(f"        ✗ Stanza failed: {e}")
        return

    # 2. Load Till modules
    print("  [2/5] Loading Till grammar modules...")
    from coptic_dialect_handler import Dialect
    from coptic_morphology_till import create_morphology_analyzer_till
    from coptic_pronouns_prepositions_till import create_pronouns_prepositions_analyzer_till
    from coptic_articles_till import create_articles_analyzer_till
    from coptic_conjunctions_till import create_conjunctions_analyzer_till
    from coptic_negation_till import create_negation_analyzer_till
    from coptic_pretokenization_morphology import create_pretokenization_morphology
    from coptic_proper_names import is_proper_name

    morphology_till = create_morphology_analyzer_till(Dialect.SAHIDIC)
    pronouns_preps_till = create_pronouns_prepositions_analyzer_till(Dialect.SAHIDIC)
    articles_till = create_articles_analyzer_till(Dialect.SAHIDIC)
    conjunctions_till = create_conjunctions_analyzer_till(Dialect.SAHIDIC)
    negation_till = create_negation_analyzer_till(Dialect.SAHIDIC)
    pretok_morph = create_pretokenization_morphology(morphology_till)
    print("        ✓ Till modules loaded (6 modules)")

    # 3. Load dialect identifier
    print("  [3/5] Loading dialect identifier...")
    try:
        from coptic_dialect_identifier import create_dialect_identifier
        dialect_id = create_dialect_identifier()
        print("        ✓ Dialect identifier loaded")
    except Exception as e:
        print(f"        ⚠ Dialect identifier not available: {e}")
        dialect_id = None

    # 4. Load text normalizer
    print("  [4/5] Loading text normalizer...")
    try:
        from coptic_text_normalizer import CopticTextNormalizer
        normalizer = CopticTextNormalizer(mode='strip')
        print("        ✓ Text normalizer loaded")
    except Exception as e:
        print(f"        ⚠ Text normalizer not available: {e}")
        normalizer = None

    print("  [5/5] Components ready")
    print()

    # Aggregate statistics
    total_stats = {
        'corpora': 0,
        'sentences': 0,
        'tokens': 0,
        'parse_errors': 0,
        'articles': 0,
        'prepositions': 0,
        'morphology': 0,
        'conjunctions': 0,
        'negations': 0,
        'proper_names': 0,
        'total_patterns': 0,
        'parse_time': 0.0,
        'dialect_counts': {}
    }

    corpus_results = []

    # Process each corpus
    for corpus_file in corpus_files:
        print("─" * 80)
        print(f"📖 Corpus: {corpus_file}")
        print("─" * 80)

        corpus_stats = {
            'name': corpus_file,
            'sentences': 0,
            'tokens': 0,
            'parse_errors': 0,
            'articles': 0,
            'prepositions': 0,
            'morphology': 0,
            'conjunctions': 0,
            'negations': 0,
            'proper_names': 0,
            'total_patterns': 0,
            'parse_time': 0.0,
            'dialects': {}
        }

        # Read corpus
        try:
            with open(corpus_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            continue

        # Split into sentences (simple split on line breaks)
        sentences = [s.strip() for s in text.split('\n') if s.strip() and len(s.strip()) > 3]
        corpus_stats['sentences'] = len(sentences)

        print(f"  Sentences: {len(sentences)}")
        print(f"  Processing...")

        start_time = time.time()

        # Process each sentence
        for sent_idx, sentence in enumerate(sentences, 1):
            if sent_idx % 10 == 0:
                print(f"    [{sent_idx}/{len(sentences)}]", end='\r')

            try:
                # Normalize
                if normalizer:
                    analysis = normalizer.analyze_text(sentence)
                    text_norm = analysis['normalized_text']
                else:
                    text_norm = sentence

                # Identify dialect
                if dialect_id:
                    detected_dialect, confidence, _ = dialect_id.identify_dialect(sentence)
                    dialect_name = detected_dialect.value
                    corpus_stats['dialects'][dialect_name] = corpus_stats['dialects'].get(dialect_name, 0) + 1

                # Pre-tokenization morphology
                morph_results = pretok_morph.analyze_text(text_norm)

                # Parse with Stanza
                doc = nlp(text_norm)

                if not doc.sentences:
                    corpus_stats['parse_errors'] += 1
                    continue

                stanza_sentence = doc.sentences[0]
                tokens = [word.text for word in stanza_sentence.words]
                pos_tags = [word.upos for word in stanza_sentence.words]

                corpus_stats['tokens'] += len(tokens)

                # Map morphology to tokens
                token_morphology = pretok_morph.map_to_tokens(morph_results, tokens, text_norm)

                # Analyze each token
                for i, token in enumerate(tokens):
                    # Skip proper names
                    if is_proper_name(token):
                        corpus_stats['proper_names'] += 1
                        continue

                    # Check pre-tokenization morphology
                    pretok_segments = pretok_morph.get_morphology_for_token(i, token, token_morphology)
                    if pretok_segments:
                        corpus_stats['morphology'] += 1
                        corpus_stats['total_patterns'] += 1
                        continue

                    # Check articles
                    article_result = articles_till.identify(token)
                    if article_result:
                        corpus_stats['articles'] += 1
                        corpus_stats['total_patterns'] += 1
                        continue

                    # Check pronouns/prepositions
                    pron_prep_result = pronouns_preps_till.identify_form(token)
                    if pron_prep_result:
                        lemma, pos, feats, section = pron_prep_result
                        if pos in ['PREP', 'ADV']:
                            corpus_stats['prepositions'] += 1
                            corpus_stats['total_patterns'] += 1
                            continue

                    # Check substring prepositions (bound forms)
                    if not pron_prep_result and len(token) > 2:
                        for prefix_len in [2, 3, 4, 5]:
                            if prefix_len >= len(token):
                                continue
                            prefix = token[:prefix_len]
                            pron_prep_result = pronouns_preps_till.identify_form(prefix)
                            if pron_prep_result and pron_prep_result[1] == 'PREP':
                                corpus_stats['prepositions'] += 1
                                corpus_stats['total_patterns'] += 1
                                break

                    # Check regular morphology
                    segments = morphology_till.segment_word(token)
                    if segments and len(segments) > 1:
                        corpus_stats['morphology'] += 1
                        corpus_stats['total_patterns'] += 1
                        continue

                    # Check conjunctions
                    conj_result = conjunctions_till.identify(token)
                    if conj_result:
                        corpus_stats['conjunctions'] += 1
                        corpus_stats['total_patterns'] += 1
                        continue

                    # Check negations
                    neg_result = negation_till.identify_negation(token)
                    if neg_result:
                        corpus_stats['negations'] += 1
                        corpus_stats['total_patterns'] += 1
                        continue

            except Exception as e:
                corpus_stats['parse_errors'] += 1

        corpus_stats['parse_time'] = time.time() - start_time

        # Display corpus results
        print()
        print(f"  ✓ Processing complete")
        print()
        print(f"  📊 Results:")
        print(f"    Sentences:     {corpus_stats['sentences']:>6}")
        print(f"    Tokens:        {corpus_stats['tokens']:>6}")
        print(f"    Parse errors:  {corpus_stats['parse_errors']:>6} ({corpus_stats['parse_errors']/max(corpus_stats['sentences'],1)*100:.1f}%)")
        print()
        print(f"  📈 Till Pattern Coverage:")
        print(f"    Articles:      {corpus_stats['articles']:>6} ({corpus_stats['articles']/max(corpus_stats['tokens'],1)*100:.1f}%)")
        print(f"    Prepositions:  {corpus_stats['prepositions']:>6} ({corpus_stats['prepositions']/max(corpus_stats['tokens'],1)*100:.1f}%)")
        print(f"    Morphology:    {corpus_stats['morphology']:>6} ({corpus_stats['morphology']/max(corpus_stats['tokens'],1)*100:.1f}%)")
        print(f"    Conjunctions:  {corpus_stats['conjunctions']:>6} ({corpus_stats['conjunctions']/max(corpus_stats['tokens'],1)*100:.1f}%)")
        print(f"    Negations:     {corpus_stats['negations']:>6} ({corpus_stats['negations']/max(corpus_stats['tokens'],1)*100:.1f}%)")
        print(f"    Proper names:  {corpus_stats['proper_names']:>6} (filtered)")
        print(f"    Total:         {corpus_stats['total_patterns']:>6} ({corpus_stats['total_patterns']/max(corpus_stats['tokens'],1)*100:.1f}%)")
        print()
        print(f"  ⏱️  Performance:")
        print(f"    Parse time:    {corpus_stats['parse_time']:.2f}s")
        print(f"    Tokens/sec:    {corpus_stats['tokens']/max(corpus_stats['parse_time'],0.001):.1f}")
        print()

        if corpus_stats['dialects']:
            print(f"  🗣️  Dialects detected:")
            for dialect, count in sorted(corpus_stats['dialects'].items(), key=lambda x: x[1], reverse=True):
                print(f"    {dialect}: {count} ({count/max(corpus_stats['sentences'],1)*100:.1f}%)")
            print()

        # Aggregate
        total_stats['corpora'] += 1
        total_stats['sentences'] += corpus_stats['sentences']
        total_stats['tokens'] += corpus_stats['tokens']
        total_stats['parse_errors'] += corpus_stats['parse_errors']
        total_stats['articles'] += corpus_stats['articles']
        total_stats['prepositions'] += corpus_stats['prepositions']
        total_stats['morphology'] += corpus_stats['morphology']
        total_stats['conjunctions'] += corpus_stats['conjunctions']
        total_stats['negations'] += corpus_stats['negations']
        total_stats['proper_names'] += corpus_stats['proper_names']
        total_stats['total_patterns'] += corpus_stats['total_patterns']
        total_stats['parse_time'] += corpus_stats['parse_time']

        for dialect, count in corpus_stats['dialects'].items():
            total_stats['dialect_counts'][dialect] = total_stats['dialect_counts'].get(dialect, 0) + count

        corpus_results.append(corpus_stats)

    # Display aggregate results
    print()
    print("=" * 80)
    print("AGGREGATE BASELINE RESULTS")
    print("=" * 80)
    print()
    print(f"📚 Corpora evaluated:  {total_stats['corpora']}")
    print(f"📄 Total sentences:    {total_stats['sentences']}")
    print(f"🔤 Total tokens:       {total_stats['tokens']}")
    print(f"❌ Parse errors:       {total_stats['parse_errors']} ({total_stats['parse_errors']/max(total_stats['sentences'],1)*100:.1f}%)")
    print()
    print(f"📊 Till Pattern Coverage (across all corpora):")
    print(f"  Articles:      {total_stats['articles']:>6} ({total_stats['articles']/max(total_stats['tokens'],1)*100:.1f}%)")
    print(f"  Prepositions:  {total_stats['prepositions']:>6} ({total_stats['prepositions']/max(total_stats['tokens'],1)*100:.1f}%)")
    print(f"  Morphology:    {total_stats['morphology']:>6} ({total_stats['morphology']/max(total_stats['tokens'],1)*100:.1f}%)")
    print(f"  Conjunctions:  {total_stats['conjunctions']:>6} ({total_stats['conjunctions']/max(total_stats['tokens'],1)*100:.1f}%)")
    print(f"  Negations:     {total_stats['negations']:>6} ({total_stats['negations']/max(total_stats['tokens'],1)*100:.1f}%)")
    print(f"  Proper names:  {total_stats['proper_names']:>6} (filtered)")
    print(f"  Total:         {total_stats['total_patterns']:>6} ({total_stats['total_patterns']/max(total_stats['tokens'],1)*100:.1f}%)")
    print()
    print(f"⏱️  Overall Performance:")
    print(f"  Total parse time:  {total_stats['parse_time']:.2f}s")
    print(f"  Avg tokens/sec:    {total_stats['tokens']/max(total_stats['parse_time'],0.001):.1f}")
    print()

    if total_stats['dialect_counts']:
        print(f"🗣️  Dialect Distribution:")
        for dialect, count in sorted(total_stats['dialect_counts'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {dialect}: {count} sentences ({count/max(total_stats['sentences'],1)*100:.1f}%)")
        print()

    print("=" * 80)
    print()
    print("💡 Baseline established!")
    print()
    print("Next steps:")
    print("  1. Add your personal document collection")
    print("  2. Run this evaluation again to measure coverage on your texts")
    print("  3. If coverage is low, consider fine-tuning Stanza on your corpus")
    print("  4. Annotate sample sentences for training data (if needed)")
    print()

    return total_stats, corpus_results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        corpus_files = sys.argv[1:]
    else:
        corpus_files = None

    evaluate_baseline(corpus_files)
