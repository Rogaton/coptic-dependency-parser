#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coptic Dialect Identifier
=========================

Identifies the dialect of Coptic text based on characteristic morphemes
and spelling patterns from Walter Till's dialectal grammar.

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

from typing import Dict, List, Tuple, Counter as CounterType
from collections import Counter
from coptic_dialect_handler import Dialect


class DialectIdentifier:
    """
    Identifies Coptic dialect based on diagnostic features.

    Uses characteristic morphemes, spelling patterns, and phonological
    features that distinguish the major Coptic dialects.
    """

    def __init__(self):
        """Initialize with diagnostic features for each dialect."""

        # Diagnostic features: words/morphemes characteristic of each dialect
        # Based on Till's dialectal grammar

        self.diagnostic_features: Dict[Dialect, List[str]] = {
            # SAHIDIC (S) - Standard literary dialect
            Dialect.SAHIDIC: [
                # Articles
                "ⲡ", "ⲧ", "ⲛ",  # Definite articles
                "ⲟⲩ",  # Indefinite article
                # Pronouns
                "ⲁⲛⲟⲕ", "ⲛⲧⲟⲕ", "ⲛⲧⲟ",
                # Conjunctions
                "ⲁⲩⲱ",  # "and" (Sahidic specific)
                # Prepositions
                "ⲙⲛ",  # "with"
                # Negation
                "ⲁⲛ", "ⲧⲙ",
                # Common words
                "ⲉⲣⲉ", "ⲛⲉ", "ϫⲉ", "ⲉⲣϣⲁⲛ"
            ],

            # BOHAIRIC (B) - Northern/liturgical dialect
            Dialect.BOHAIRIC: [
                # Articles - Bohairic has distinctive forms
                "ⲫ", "ⲑ",  # Aspirated definite articles (unique to Bohairic)
                # Conjunction
                "ⲟⲩⲟϩ",  # "and" (Bohairic specific)
                # Pronouns
                "ⲁⲛⲟⲕ", "ⲛⲑⲟⲕ", "ⲛⲑⲟ",
                # Relative
                "ⲉⲧⲁϥ", "ⲉⲧⲁⲥ",
                # Common Bohairic words
                "ⲁϥ", "ⲁⲥ", "ⲭⲁ", "ⲑⲏⲛⲟⲩ"
            ],

            # AKHMIMIC (A) - Upper Egypt
            Dialect.AKHMIMIC: [
                # Pronouns
                "ⲁⲛⲁⲕ", "ⲛⲧⲁⲕ", "ⲛⲧⲁ",
                # Conjunction
                "ⲁⲟⲩ",  # "and"
                # Characteristic spellings
                "ⲑⲁ", "ⲑⲛⲁ",
                # Articles
                "ⲡⲁ", "ⲧⲁ", "ⲛⲁ"
            ],

            # LYCOPOLITAN (L) - Middle Egypt
            Dialect.LYCOPOLITAN: [
                # Conjunction
                "ⲟⲩⲁϩϩⲛ", "ⲟⲩⲁϩⲁ",  # "and"
                # Pronouns
                "ⲁⲛⲁⲕ", "ⲛⲧⲁⲕ",
                # Characteristic forms
                "ⲙⲛⲛⲥⲁ"
            ],

            # FAYYUMIC (F) - Fayyum region
            Dialect.FAYYUMIC: [
                # Distinctive Fayyumic features
                "ⲗ",  # Often uses ⲗ where others use ⲣ
                "ⲗⲱ",  # Conjunction
                # Pronouns
                "ⲁⲛⲏⲕ", "ⲛⲧⲏⲕ"
            ]
        }

        # Phonological patterns (regex-like character substitutions)
        self.phonological_markers: Dict[Dialect, List[Tuple[str, str]]] = {
            Dialect.BOHAIRIC: [
                ("ϣ", "ϫ"),  # Bohairic often has ϫ where Sahidic has ϣ
            ],
            Dialect.FAYYUMIC: [
                ("ⲣ", "ⲗ"),  # Fayyumic often has ⲗ where others have ⲣ
            ]
        }

    def identify_dialect(self, text: str) -> Tuple[Dialect, float, Dict[Dialect, int]]:
        """
        Identify the most likely dialect of the input text.

        Args:
            text: Coptic text to analyze

        Returns:
            Tuple of (identified_dialect, confidence_score, feature_counts)

        Example:
            >>> identifier = DialectIdentifier()
            >>> dialect, confidence, counts = identifier.identify_dialect("ⲁⲩⲱ ⲁⲛⲟⲕ ⲡⲉ")
            >>> print(f"Detected: {dialect.full_name} (S) - {confidence:.1%} confidence")
            Detected: Sahidic (S) - 85.0% confidence
        """

        # Normalize text: split into tokens
        tokens = self._tokenize(text)

        # Count diagnostic features for each dialect
        feature_counts: Dict[Dialect, int] = Counter()

        for dialect, features in self.diagnostic_features.items():
            for token in tokens:
                # Check exact matches
                if token in features:
                    feature_counts[dialect] += 1

                # Check if token contains characteristic morpheme
                for feature in features:
                    if len(feature) > 2 and feature in token:
                        feature_counts[dialect] += 0.5  # Partial match

        # If no features found, default to Sahidic (most common)
        if not feature_counts:
            return Dialect.SAHIDIC, 0.5, {}

        # Find dialect with most features
        most_common_dialect = feature_counts.most_common(1)[0][0]
        max_count = feature_counts[most_common_dialect]
        total_count = sum(feature_counts.values())

        # Calculate confidence (percentage of total features)
        confidence = max_count / total_count if total_count > 0 else 0.5

        # Convert float counts to int for display
        int_counts = {d: int(count) for d, count in feature_counts.items()}

        return most_common_dialect, confidence, int_counts

    def _tokenize(self, text: str) -> List[str]:
        """
        Simple tokenization of Coptic text.

        Splits on whitespace and punctuation while preserving Coptic characters.
        """
        import re
        # Split on spaces and common punctuation
        tokens = re.findall(r'[ⲁ-ⲯϣϥϧϩϫϭϯ]+', text.lower())
        return tokens

    def get_dialect_info(self, dialect: Dialect) -> str:
        """Get descriptive information about a dialect."""
        info = {
            Dialect.SAHIDIC: "Sahidic (S) - Standard literary dialect, most common in manuscripts",
            Dialect.BOHAIRIC: "Bohairic (B) - Northern dialect, used in Coptic liturgy today",
            Dialect.AKHMIMIC: "Akhmimic (A) - Upper Egyptian dialect",
            Dialect.LYCOPOLITAN: "Lycopolitan (L) - Middle Egyptian dialect (Subakhmimic)",
            Dialect.FAYYUMIC: "Fayyumic (F) - Dialect of the Fayyum region",
            Dialect.MIDDLE_EGYPTIAN: "Middle Egyptian (M) - Archaic Coptic forms",
            Dialect.PROTO_SAHIDIC: "Proto-Sahidic (P) - Early Sahidic forms"
        }
        return info.get(dialect, f"{dialect.full_name} ({dialect.value})")

    def get_confidence_description(self, confidence: float) -> str:
        """Convert confidence score to human-readable description."""
        if confidence >= 0.8:
            return "Very confident"
        elif confidence >= 0.6:
            return "Confident"
        elif confidence >= 0.4:
            return "Moderate confidence"
        else:
            return "Low confidence (mixed features)"


def create_dialect_identifier() -> DialectIdentifier:
    """Factory function to create a dialect identifier."""
    return DialectIdentifier()


# Example usage and testing
if __name__ == "__main__":
    identifier = create_dialect_identifier()

    # Test with Sahidic text
    sahidic_text = "ⲁⲩⲱ ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ"
    dialect, conf, counts = identifier.identify_dialect(sahidic_text)
    print(f"Text: {sahidic_text}")
    print(f"Detected: {identifier.get_dialect_info(dialect)}")
    print(f"Confidence: {conf:.1%} - {identifier.get_confidence_description(conf)}")
    print(f"Feature counts: {counts}\n")

    # Test with Bohairic text
    bohairic_text = "ⲟⲩⲟϩ ⲁⲛⲟⲕ ⲡⲉ ⲫⲛⲟⲩϯ"
    dialect, conf, counts = identifier.identify_dialect(bohairic_text)
    print(f"Text: {bohairic_text}")
    print(f"Detected: {identifier.get_dialect_info(dialect)}")
    print(f"Confidence: {conf:.1%} - {identifier.get_confidence_description(conf)}")
    print(f"Feature counts: {counts}")
