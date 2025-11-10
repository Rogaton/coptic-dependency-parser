#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coptic Negation Analyzer - Based on Walter Till's Dialectal Grammar
=====================================================================

Extracts negation patterns from Till §314-319 (LA NÉGATION).

Negation appears in ~25-35% of Coptic sentences - EXTREMELY HIGH FREQUENCY!

Coverage:
- §314: Negative expressions (ⲙⲉⲩⲩⲉ patterns)
- §315: Prohibitive ⲧⲙ
- §316: Negative conjunctive
- §317: Particle ⲁⲛ placement
- §318: ⲙⲙⲟⲛ "non"
- §319: Affirmative "oui"

Plus: ⲙⲡⲉ- negative perfects (from §263)

Source: Walter Till, "Koptische Dialektgrammatik" (French translation)
        Sections §314-319 (LA NÉGATION)

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from coptic_dialect_handler import Dialect

@dataclass
class NegationForm:
    """Represents a negation morpheme"""
    form: str              # Surface form
    neg_type: str          # "prohibitive", "particle", "expression", "affirmative"
    meaning: str           # Semantic meaning
    scope: Optional[str]   # What it negates (e.g., "PrésII only")
    dialect: Dialect       # Dialect
    source_section: str    # Till section


class CopticNegationTill:
    """
    Analyzes Coptic negation based on Till §314-319.

    Negation is EXTREMELY frequent (~30% of sentences)!

    Types:
    - Prohibitive: ⲧⲙ (blocks Présent II, Final, Temporal, Conjunctive)
    - Particle: ⲁⲛ (general negation)
    - Existential: ⲙⲙⲟⲛ "there is not"
    - Perfective: ⲙⲡⲉ- (negative past)
    - Expressions: ⲙⲉⲩⲩⲉ "it doesn't happen"

    Example:
        analyzer = CopticNegationTill()
        result = analyzer.identify_negation("ⲙⲡⲉϥⲃⲱⲕ")  # ⲙⲡⲉ- negative past
    """

    def __init__(self, dialect: Dialect = Dialect.SAHIDIC):
        """Initialize analyzer."""
        self.dialect = dialect
        self._init_negation_forms()

    def _init_negation_forms(self):
        """Initialize negation morphemes from Till §314-319."""
        self.negations: Dict[str, NegationForm] = {}

        # §314: NEGATIVE EXPRESSIONS
        # "ça ne se fait pas" / "it doesn't happen"

        expressions = [
            # Sahidic/Lycopolitan
            ("ⲙⲉⲩⲩⲉ", "expression", "it doesn't happen", None, Dialect.SAHIDIC, "§314"),
            ("ⲙⲉⲱⲱⲉ", "expression", "it doesn't happen", None, Dialect.SAHIDIC, "§314"),
            # Akhmimic
            ("ⲙⲁⲩⲩⲉ", "expression", "it doesn't happen", None, Dialect.AKHMIMIC, "§314"),
            ("ⲙⲁⲱⲱⲉ", "expression", "it doesn't happen", None, Dialect.AKHMIMIC, "§314"),
            # Fayyumic
            ("ⲙⲉⲥⲱⲱⲉ", "expression", "it doesn't happen", None, Dialect.FAYYUMIC, "§314"),
        ]
        for form, neg_type, meaning, scope, dialect, section in expressions:
            self.negations[f"{form}_{dialect.value}"] = NegationForm(
                form, neg_type, meaning, scope, dialect, section
            )
            # Common forms
            if form in ["ⲙⲉⲩⲩⲉ", "ⲙⲁⲩⲩⲉ"]:
                self.negations[form] = NegationForm(
                    form, neg_type, meaning, scope, dialect, section
                )

        # §315: PROHIBITIVE ⲧⲙ
        # "do not" for Present II only
        prohibitives = [
            ("ⲧⲙ", "prohibitive", "do not", "PrésII/Final/Temporal/Conj", Dialect.SAHIDIC, "§315"),
            # Akhmimic
            ("ⲧⲙⲛ", "prohibitive", "do not", "PrésII/Final/Temporal/Conj", Dialect.AKHMIMIC, "§315"),
            # Bohairic/Fayyumic
            ("ⲱⲧⲉⲙ", "prohibitive", "do not", "PrésII/Final/Temporal/Conj", Dialect.BOHAIRIC, "§315"),
            ("ⲱⲧⲉⲙ", "prohibitive", "do not", "PrésII/Final/Temporal/Conj", Dialect.FAYYUMIC, "§315"),
        ]
        for form, neg_type, meaning, scope, dialect, section in prohibitives:
            self.negations[f"{form}_{dialect.value}"] = NegationForm(
                form, neg_type, meaning, scope, dialect, section
            )
            if form == "ⲧⲙ":
                self.negations[form] = NegationForm(
                    form, neg_type, meaning, scope, dialect, section
                )

        # §317: PARTICLE ⲁⲛ
        # Placed between ⲛ and verb: "il ne viendra pas"
        # Universal across dialects

        self.negations["ⲁⲛ"] = NegationForm(
            "ⲁⲛ", "particle", "not", "all_constructions",
            Dialect.SAHIDIC, "§317"
        )

        # §318: EXISTENTIAL NEGATIVE ⲙⲙⲟⲛ "non"
        # "il n'existe pas" / "there is not"

        existentials = [
            ("ⲙⲙⲟⲛ", "existential", "there is not", "existential", Dialect.SAHIDIC, "§318"),
            ("ⲙⲙⲟⲛ", "existential", "there is not", "existential", Dialect.BOHAIRIC, "§318"),
            ("ⲙⲙⲁⲛ", "existential", "there is not", "existential", Dialect.AKHMIMIC, "§318"),
            ("ⲙⲙⲁⲛ", "existential", "there is not", "existential", Dialect.LYCOPOLITAN, "§318"),
            ("ⲙⲙⲁⲛ", "existential", "there is not", "existential", Dialect.FAYYUMIC, "§318"),
            ("ⲙⲡⲱⲣ", "existential", "no (substantive)", "substantive", Dialect.SAHIDIC, "§318"),
            ("ⲙⲫⲱⲣ", "existential", "no (substantive)", "substantive", Dialect.BOHAIRIC, "§318"),
            ("ⲙⲡⲉ", "existential", "not (past)", "past", Dialect.SAHIDIC, "§318"),
            ("ⲙⲫⲉ", "existential", "not (past)", "past", Dialect.BOHAIRIC, "§318"),
            ("ⲙⲡⲏ", "existential", "not", "general", Dialect.FAYYUMIC, "§318"),
        ]
        for form, neg_type, meaning, scope, dialect, section in existentials:
            self.negations[f"{form}_{dialect.value}"] = NegationForm(
                form, neg_type, meaning, scope, dialect, section
            )
            if form in ["ⲙⲙⲟⲛ", "ⲙⲡⲉ"]:
                self.negations[form] = NegationForm(
                    form, neg_type, meaning, scope, dialect, section
                )

        # Negative perfect prefixes
        neg_perfects = [
            ("ⲙⲡⲉ", "prefix", "not (perfect)", "perfect", Dialect.SAHIDIC, "§263"),
            ("ⲙⲡⲁⲧⲉ", "prefix", "not yet", "not_yet", Dialect.SAHIDIC, "§266"),
            ("ⲙⲡⲁⲧⲉ", "prefix", "not yet", "not_yet", Dialect.BOHAIRIC, "§266"),
        ]
        for form, neg_type, meaning, scope, dialect, section in neg_perfects:
            key = f"{form}_{dialect.value}_prefix"
            self.negations[key] = NegationForm(
                form, neg_type, meaning, scope, dialect, section
            )

        # §319: AFFIRMATIVE "oui" (for completeness)

        affirmatives = [
            ("ⲥⲉ", "affirmative", "yes", None, Dialect.SAHIDIC, "§319"),
            ("ⲥⲉ", "affirmative", "yes", None, Dialect.LYCOPOLITAN, "§319"),
            ("ⲥⲉ", "affirmative", "yes", None, Dialect.BOHAIRIC, "§319"),
            ("ⲉⲥⲉ", "affirmative", "yes", None, Dialect.SAHIDIC, "§319"),
            ("ⲁⲥⲟ", "affirmative", "yes", None, Dialect.AKHMIMIC, "§319"),
            ("ⲁⲥⲁ", "affirmative", "yes", None, Dialect.BOHAIRIC, "§319"),
            ("ⲥⲏ", "affirmative", "yes", None, Dialect.FAYYUMIC, "§319"),
            ("ⲇⲥⲏ", "affirmative", "yes", None, Dialect.FAYYUMIC, "§319"),
        ]
        for form, neg_type, meaning, scope, dialect, section in affirmatives:
            self.negations[f"{form}_{dialect.value}_aff"] = NegationForm(
                form, neg_type, meaning, scope, dialect, section
            )

    def identify_negation(self, word: str, dialect: Optional[Dialect] = None) -> Optional[NegationForm]:
        """
        Identify if word contains negation morpheme.

        Args:
            word: Surface form
            dialect: Optional dialect hint

        Returns:
            NegationForm if found, else None

        Example:
            >>> analyzer.identify_negation("ⲙⲡⲉϥⲃⲱⲕ"form="ⲙⲡⲉ", type="prefix", meaning="not (perfect", ...)
        """
        target_dialect = dialect or self.dialect

        # Try longest matches first
        candidates = ["ⲙⲡⲁⲧⲉ", "ⲙⲉⲥⲱⲱⲉ", "ⲙⲉⲱⲱⲉ", "ⲙⲁⲱⲱⲉ", "ⲙⲉⲩⲩⲉ", "ⲙⲁⲩⲩⲉ",
                      "ⲱⲧⲉⲙ", "ⲙⲙⲟⲛ", "ⲙⲙⲁⲛ", "ⲙⲡⲱⲣ", "ⲙⲫⲱⲣ",
                      "ⲙⲡⲉ", "ⲙⲫⲉ", "ⲙⲡⲏ", "ⲧⲙⲛ", "ⲧⲙ", "ⲁⲛ",
                      "ⲉⲥⲉ", "ⲁⲥⲟ", "ⲁⲥⲁ", "ⲇⲥⲏ", "ⲥⲉ", "ⲥⲏ"]

        for candidate in candidates:
            if candidate in word:  # Can appear anywhere
                # Try dialect-specific
                key = f"{candidate}_{target_dialect.value}"
                if key in self.negations:
                    return self.negations[key]
                # Try with prefix suffix
                key_prefix = f"{candidate}_{target_dialect.value}_prefix"
                if key_prefix in self.negations:
                    return self.negations[key_prefix]
                # Try affirmative
                key_aff = f"{candidate}_{target_dialect.value}_aff"
                if key_aff in self.negations:
                    return self.negations[key_aff]
                # Try generic
                if candidate in self.negations:
                    return self.negations[candidate]

        return None

    def is_negative(self, word: str, dialect: Optional[Dialect] = None) -> bool:
        """Check if word contains negation."""
        result = self.identify_negation(word, dialect)
        return result is not None and result.neg_type != "affirmative"

    def is_affirmative(self, word: str, dialect: Optional[Dialect] = None) -> bool:
        """Check if word is affirmative particle."""
        result = self.identify_negation(word, dialect)
        return result is not None and result.neg_type == "affirmative"

    def extract_negation(self, word: str, dialect: Optional[Dialect] = None) -> Optional[Tuple[str, str]]:
        """
        Extract negation prefix and return (negation, remainder).

        Args:
            word: Full word
            dialect: Optional dialect

        Returns:
            (negation, remainder) or None

        Example:
            >>> analyzer.extract_negation("ⲙⲡⲉϥⲃⲱⲕ")
            ("ⲙⲡⲉ", "ϥⲃⲱⲕ")
        """
        result = self.identify_negation(word, dialect)
        if result and word.startswith(result.form):
            return (result.form, word[len(result.form):])
        return None


def create_negation_analyzer_till(dialect: Dialect = Dialect.SAHIDIC) -> CopticNegationTill:
    """Factory function to create negation analyzer."""
    return CopticNegationTill(dialect=dialect)


if __name__ == "__main__":
    # Quick test
    analyzer = create_negation_analyzer_till(dialect=Dialect.SAHIDIC)

    print("Testing negation recognition:")
    test_words = ["ⲙⲡⲉϥⲃⲱⲕ", "ⲁⲛ", "ⲧⲙⲃⲱⲕ", "ⲙⲙⲟⲛ", "ⲙⲉⲩⲩⲉ", "ⲥⲉ"]

    for word in test_words:
        result = analyzer.identify_negation(word)
        if result:
            scope_info = f", scope={result.scope}" if result.scope else ""
            print(f"✓ {word}: {result.form} [{result.neg_type}: \"{result.meaning}\"{scope_info}]")
        else:
            print(f"✗ {word}: No negation")
