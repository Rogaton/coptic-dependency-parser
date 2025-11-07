#!/usr/bin/env python3
"""
Coptic Text Normalizer
======================

Handles Unicode normalization for Coptic text, particularly dealing with
combining diacritical marks that can cause tokenization issues in NLP models.

Common Coptic Combining Marks:
- U+0307 (COMBINING DOT ABOVE): ̇  - marks syllabic consonants
- U+0304 (COMBINING MACRON): ̄  - marks long vowels
- U+0308 (COMBINING DIAERESIS): ̈  - marks specific vowel qualities

These marks are not in Stanza's training vocabulary and get converted to <UNK>.

Author: Coptic NLP Project
License: CC BY-NC-SA 4.0
"""

import unicodedata
import re
from typing import Dict, List, Tuple


class CopticTextNormalizer:
    """
    Normalize Coptic text for NLP processing

    Strategies:
    1. Remove combining diacritics (default)
    2. Convert to base characters with precomposed equivalents
    3. Preserve original for reference/display
    """

    # Combining marks commonly used in Coptic texts
    COMBINING_MARKS = {
        '\u0307': '',  # COMBINING DOT ABOVE
        '\u0304': '',  # COMBINING MACRON
        '\u0308': '',  # COMBINING DIAERESIS
        '\u0323': '',  # COMBINING DOT BELOW
        '\u0300': '',  # COMBINING GRAVE ACCENT
        '\u0301': '',  # COMBINING ACUTE ACCENT
        '\u0302': '',  # COMBINING CIRCUMFLEX ACCENT
        '\u0303': '',  # COMBINING TILDE
        '\u0305': '',  # COMBINING OVERLINE
        '\u0306': '',  # COMBINING BREVE
        '\u030A': '',  # COMBINING RING ABOVE
        '\u030B': '',  # COMBINING DOUBLE ACUTE ACCENT
        '\u030C': '',  # COMBINING CARON
        '\uFE20': '',  # COMBINING LIGATURE LEFT HALF
        '\uFE21': '',  # COMBINING LIGATURE RIGHT HALF
        '\uFE22': '',  # COMBINING DOUBLE TILDE LEFT HALF
        '\uFE23': '',  # COMBINING DOUBLE TILDE RIGHT HALF
        '\uFE24': '',  # COMBINING MACRON LEFT HALF
        '\uFE25': '',  # COMBINING MACRON RIGHT HALF
        '\uFE26': '',  # COMBINING CONJOINING MACRON - CRITICAL for Coptic manuscripts
        '\uFE27': '',  # COMBINING LIGATURE LEFT HALF BELOW
        '\uFE28': '',  # COMBINING LIGATURE RIGHT HALF BELOW
        '\uFE29': '',  # COMBINING TILDE LEFT HALF BELOW
        '\uFE2A': '',  # COMBINING TILDE RIGHT HALF BELOW
        '\uFE2B': '',  # COMBINING MACRON LEFT HALF BELOW
        '\uFE2C': '',  # COMBINING MACRON RIGHT HALF BELOW
        '\uFE2D': '',  # COMBINING CONJOINING MACRON BELOW
    }

    def __init__(self, mode='strip', preserve_original=True, normalize_punctuation=True):
        """
        Initialize normalizer

        Args:
            mode: 'strip' (remove marks) or 'nfd' (decompose) or 'nfc' (compose)
            preserve_original: Keep original text for display purposes
            normalize_punctuation: Convert Coptic punctuation to standard forms
        """
        self.mode = mode
        self.preserve_original = preserve_original
        self.normalize_punctuation = normalize_punctuation

    def normalize(self, text: str) -> str:
        """
        Normalize Coptic text by removing combining diacritics

        Args:
            text: Original Coptic text with diacritics

        Returns:
            Normalized text without combining marks
        """
        # First normalize punctuation if enabled
        if self.normalize_punctuation:
            text = self._normalize_punctuation(text)

        if self.mode == 'strip':
            return self._strip_combining_marks(text)
        elif self.mode == 'nfd':
            # Decompose then remove marks
            nfd = unicodedata.normalize('NFD', text)
            return self._strip_combining_marks(nfd)
        elif self.mode == 'nfc':
            # Try to compose to precomposed characters first
            return unicodedata.normalize('NFC', text)
        else:
            return text

    def _normalize_punctuation(self, text: str) -> str:
        """
        Normalize Coptic manuscript punctuation to standard forms

        This helps Stanza recognize sentence boundaries correctly.
        """
        # Middle dot (·) is used as sentence delimiter in Coptic manuscripts
        text = text.replace('\u00B7', '.')  # MIDDLE DOT → FULL STOP

        # Other common Coptic punctuation variants
        text = text.replace('\u2027', '.')  # HYPHENATION POINT → FULL STOP
        text = text.replace('\u2022', '.')  # BULLET → FULL STOP
        text = text.replace('\u2219', '.')  # BULLET OPERATOR → FULL STOP

        return text

    def _strip_combining_marks(self, text: str) -> str:
        """Remove all combining diacritical marks from text"""
        # Remove known combining marks
        for mark, replacement in self.COMBINING_MARKS.items():
            text = text.replace(mark, replacement)

        # Remove any remaining combining marks (Unicode category Mn, Mc, Me)
        # This catches any marks we didn't explicitly list
        text = ''.join(char for char in text
                      if unicodedata.category(char) not in ('Mn', 'Mc', 'Me'))

        return text

    def normalize_tokens(self, tokens: List[str]) -> List[str]:
        """Normalize a list of tokens"""
        return [self.normalize(token) for token in tokens]

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text for combining marks and provide statistics

        Returns:
            dict with:
              - original_text: input text
              - normalized_text: cleaned text
              - marks_found: list of combining marks detected
              - count: number of combining marks removed
              - affected_positions: positions where marks were found
        """
        marks_found = []
        affected_positions = []

        for i, char in enumerate(text):
            if char in self.COMBINING_MARKS or unicodedata.category(char) in ('Mn', 'Mc', 'Me'):
                marks_found.append({
                    'char': char,
                    'unicode': f'U+{ord(char):04X}',
                    'name': unicodedata.name(char, 'UNKNOWN'),
                    'position': i,
                    'context': text[max(0, i-3):min(len(text), i+4)]
                })
                affected_positions.append(i)

        normalized = self.normalize(text)

        return {
            'original_text': text,
            'normalized_text': normalized,
            'marks_found': marks_found,
            'count': len(marks_found),
            'affected_positions': affected_positions,
            'has_issues': len(marks_found) > 0
        }

    def create_mapping(self, original: str, normalized: str) -> List[Tuple[str, str]]:
        """
        Create word-by-word mapping between original and normalized text

        Useful for display purposes to show what changed
        """
        orig_words = original.split()
        norm_words = normalized.split()

        mapping = []
        for orig, norm in zip(orig_words, norm_words):
            if orig != norm:
                mapping.append((orig, norm))

        return mapping


def demonstrate_normalization():
    """Demonstrate the normalization on sample Coptic text"""
    normalizer = CopticTextNormalizer(mode='strip')

    # Sample text with combining marks
    sample = "ϫⲉ ⲁ̇ ⲟⲨ ⲥⲧⲁⲥⲓ̄ⲥ ϣⲱⲡⲉ Ⲡⲉϫⲁ ⲩ ⲛⲁ ϥ ⲟⲛ · ϫⲉ ⲁ̇ⲛⲟⲛ ⲧⲉⲛ ⲥⲟⲟⲩⲛ̇ ϫⲉ ⲟⲩ ⲇⲓ̈ⲕⲁⲓ̈ⲟⲥ ⲡⲉ ⲡⲉⲓ̈ ⲣⲱⲙⲉ"

    print("="*70)
    print("Coptic Text Normalization Demo")
    print("="*70)

    # Analyze the text
    analysis = normalizer.analyze_text(sample)

    print(f"\nOriginal text:")
    print(f"  {analysis['original_text'][:100]}...")

    print(f"\nNormalized text:")
    print(f"  {analysis['normalized_text'][:100]}...")

    print(f"\nCombining marks found: {analysis['count']}")

    if analysis['marks_found']:
        print("\nDetailed mark locations:")
        for mark in analysis['marks_found'][:10]:  # Show first 10
            print(f"  {mark['name']} ({mark['unicode']}) at position {mark['position']}")
            print(f"    Context: {mark['context']}")

    # Show word changes
    mapping = normalizer.create_mapping(
        analysis['original_text'],
        analysis['normalized_text']
    )

    if mapping:
        print(f"\nWords changed ({len(mapping)}):")
        for orig, norm in mapping[:10]:  # Show first 10
            print(f"  {orig} → {norm}")

    print("\n" + "="*70)


if __name__ == "__main__":
    demonstrate_normalization()
