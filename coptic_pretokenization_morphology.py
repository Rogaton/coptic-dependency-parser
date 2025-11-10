#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-Tokenization Morphological Analysis for Coptic
===================================================

Solves the tokenization/morphology conflict:
- Stanza tokenizes: ⲙⲡⲉϥⲃⲱⲕ → ['ⲙ', 'ⲡⲉϥ', 'ⲃⲱⲕ']
- Till needs whole token: ⲙⲡⲉϥⲃⲱⲕ → ⲙⲡⲉ + ϥ + ⲃⲱⲕ

Solution: Analyze morphology BEFORE tokenization, map results to tokens

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class MorphologyMatch:
    """Maps original word to its morphological segmentation"""
    original_word: str          # e.g., "ⲙⲡⲉϥⲃⲱⲕ"
    start_pos: int              # Character position in text
    end_pos: int                # Character position in text
    segments: List              # Till morphology segments
    token_indices: List[int]    # Which Stanza tokens correspond to this word


class PreTokenizationMorphology:
    """
    Analyzes morphology before tokenization, then maps results to tokens.

    Workflow:
    1. Extract words from raw text (space-separated)
    2. Run Till morphology on each word
    3. Store segmentation results with position info
    4. After Stanza tokenization, map segments to tokens
    """

    def __init__(self, morphology_analyzer):
        """
        Initialize with Till morphology analyzer.

        Args:
            morphology_analyzer: CopticMorphologyTill instance
        """
        self.morphology = morphology_analyzer

    def analyze_text(self, text: str) -> Dict[str, List[MorphologyMatch]]:
        """
        Analyze text before tokenization.

        Args:
            text: Raw Coptic text

        Returns:
            Dictionary mapping original words to morphology results
        """
        results = {}

        # Extract words with positions (Coptic characters only)
        word_pattern = r'[ⲁ-ⲱϣϥϧϩϫϭϯ]+'

        for match in re.finditer(word_pattern, text):
            word = match.group()
            start = match.start()
            end = match.end()

            # Analyze with Till morphology
            segments = self.morphology.segment_word(word)

            # Only store if actually segmented (>1 segment)
            if segments and len(segments) > 1:
                morph_match = MorphologyMatch(
                    original_word=word,
                    start_pos=start,
                    end_pos=end,
                    segments=segments,
                    token_indices=[]  # Will be filled after tokenization
                )
                results[word] = morph_match

        return results

    def map_to_tokens(self,
                      morphology_results: Dict[str, MorphologyMatch],
                      tokens: List[str],
                      original_text: str) -> Dict[int, MorphologyMatch]:
        """
        Map pre-tokenization morphology to Stanza tokens.

        Args:
            morphology_results: Results from analyze_text()
            tokens: Stanza tokens
            original_text: Original text

        Returns:
            Dictionary mapping token index → morphology result
        """
        token_morphology = {}

        # Build reverse index: token → position in original text
        token_positions = []
        search_start = 0

        for token in tokens:
            # Find this token in original text
            pos = original_text.find(token, search_start)
            if pos >= 0:
                token_positions.append((pos, pos + len(token)))
                search_start = pos + len(token)
            else:
                token_positions.append(None)

        # For each morphology result, find which tokens it spans
        for word, morph_match in morphology_results.items():
            word_start = morph_match.start_pos
            word_end = morph_match.end_pos

            # Find tokens that overlap with this word
            overlapping_tokens = []
            for idx, token_pos in enumerate(token_positions):
                if token_pos is None:
                    continue

                tok_start, tok_end = token_pos

                # Check if token overlaps with word
                if not (tok_end <= word_start or tok_start >= word_end):
                    overlapping_tokens.append(idx)

            # Store mapping for first token (representative)
            if overlapping_tokens:
                morph_match.token_indices = overlapping_tokens
                token_morphology[overlapping_tokens[0]] = morph_match

        return token_morphology

    def get_morphology_for_token(self,
                                  token_idx: int,
                                  token_text: str,
                                  token_morphology: Dict[int, MorphologyMatch]) -> Optional[List]:
        """
        Get Till morphology segments for a specific token.

        Args:
            token_idx: Token index
            token_text: Token text
            token_morphology: Mapping from map_to_tokens()

        Returns:
            Morphology segments or None
        """
        if token_idx in token_morphology:
            return token_morphology[token_idx].segments

        return None

    def format_morphology_display(self, segments: List) -> str:
        """
        Format morphology segments for display.

        Args:
            segments: Till MorphSegment objects

        Returns:
            Formatted string like "ⲙⲡⲉ(ANEGPST)+ϥ(PPERS)+ⲃⲱⲕ(V)"
        """
        if not segments:
            return ""

        parts = []
        for seg in segments:
            if seg.source_section:
                parts.append(f"{seg.form}({seg.pos}:{seg.source_section})")
            else:
                parts.append(f"{seg.form}({seg.pos})")

        return "+".join(parts)


def create_pretokenization_morphology(morphology_analyzer):
    """
    Factory function to create pre-tokenization morphology analyzer.

    Args:
        morphology_analyzer: CopticMorphologyTill instance

    Returns:
        PreTokenizationMorphology instance
    """
    return PreTokenizationMorphology(morphology_analyzer)


if __name__ == "__main__":
    # Test the pre-tokenization approach
    from coptic_morphology_till import create_morphology_analyzer_till
    from coptic_dialect_handler import Dialect

    print("Testing Pre-Tokenization Morphology Analysis")
    print("=" * 70)

    # Initialize
    morphology = create_morphology_analyzer_till(Dialect.SAHIDIC)
    pretok_morph = create_pretokenization_morphology(morphology)

    # Test text with compound words
    test_text = "ⲙⲡⲉϥⲃⲱⲕ ⲉⲃⲟⲗ ⲁⲩⲱ ⲙⲡⲁⲧⲉϥⲉⲓ"

    print(f"\nOriginal text: {test_text}")
    print()

    # Step 1: Pre-tokenization morphology
    print("Step 1: Pre-tokenization morphological analysis")
    print("-" * 70)
    morph_results = pretok_morph.analyze_text(test_text)

    for word, match in morph_results.items():
        seg_str = pretok_morph.format_morphology_display(match.segments)
        print(f"  {word:15} → {seg_str}")

    print()

    # Step 2: Simulate Stanza tokenization (space + punctuation split)
    print("Step 2: Simulated Stanza tokenization")
    print("-" * 70)
    tokens = test_text.split()  # Simplified
    print(f"  Tokens: {tokens}")
    print()

    # Step 3: Map morphology to tokens
    print("Step 3: Map morphology to tokens")
    print("-" * 70)
    token_morphology = pretok_morph.map_to_tokens(morph_results, tokens, test_text)

    for tok_idx, morph_match in token_morphology.items():
        token = tokens[tok_idx]
        seg_str = pretok_morph.format_morphology_display(morph_match.segments)
        print(f"  Token[{tok_idx}] '{token}' → spans '{morph_match.original_word}'")
        print(f"           Morphology: {seg_str}")

    print()
    print("=" * 70)
    print("✓ Pre-tokenization morphology test complete")
    print()
    print("This approach preserves morphological analysis even when")
    print("Stanza breaks compound words into multiple tokens.")
