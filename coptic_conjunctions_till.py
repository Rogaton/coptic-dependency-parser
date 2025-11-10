#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coptic Conjunctions Analyzer - Based on Walter Till's Dialectal Grammar
========================================================================

Extracts conjunction patterns from Till §292-304 (LES CONJONCTIONS).

Conjunctions appear in ~40-50% of complex sentences!

Coverage:
- §292-296: ⲭⲉ subordinating conjunction and variants
- §297: Other conjunctions (ⲭⲓⲛ, ⲓⲥⲭⲉⲛ, ⲭⲛ)
- §298: Greek conjunctions (ϩⲓⲛⲁ, ⲙⲏⲡⲱⲥ, etc.)
- §300: Coordinating conjunctions (ⲁⲩⲱ, ⲁⲟⲩ, ⲟⲩⲟϩ)
- §301-303: ⲙⲛ/ⲛⲉⲙ comitative "with"

Pattern: Clause₁ + [CONJUNCTION] + Clause₂

Source: Walter Till, "Koptische Dialektgrammatik" (French translation)
        Sections §292-304 (LES CONJONCTIONS)

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

from typing import Optional, Dict
from dataclasses import dataclass
from coptic_dialect_handler import Dialect

@dataclass
class ConjunctionForm:
    """Represents a conjunction"""
    form: str              # Surface form
    conj_type: str         # "subordinating", "coordinating", "comitative"
    meaning: str           # Function
    subtype: Optional[str] # Additional classification
    dialect: Dialect       # Dialect
    source_section: str    # Till section

class CopticConjunctionsTill:
    """
    Analyzes Coptic conjunctions based on Till §292-304.

    Conjunctions are THE primary way to connect clauses in Coptic.

    Types:
    - Subordinating: ⲭⲉ "that", ⲭⲉⲕⲁⲁⲥ "afin que", etc.
    - Coordinating: ⲁⲩⲱ "and", ⲟⲩⲟϩ "and", etc.
    - Comitative: ⲙⲛ/ⲛⲉⲙ "with"

    Example:
        analyzer = CopticConjunctionsTill()
        result = analyzer.identify("ⲭⲉ")  # subordinating "that"
        result = analyzer.identify("ⲁⲩⲱ")  # coordinating "and"
    """

    def __init__(self, dialect: Dialect = Dialect.SAHIDIC):
        """Initialize analyzer."""
        self.dialect = dialect
        self._init_conjunctions()

    def _init_conjunctions(self):
        """Initialize conjunctions from §292-304."""
        self.conjunctions: Dict[str, ConjunctionForm] = {}

        # §292-296: ⲬⲈ - MAIN SUBORDINATING CONJUNCTION
        # Introduces object clauses (subject/object propositions)
        # "that" in English

        xe_forms = [
            # Basic form (all dialects)
            ("ⲭⲉ", "subordinating", "that", "object_clause", Dialect.SAHIDIC, "§292"),
            ("ⲭⲉ", "subordinating", "that", "object_clause", Dialect.BOHAIRIC, "§292"),
            ("ⲭⲉ", "subordinating", "that", "object_clause", Dialect.AKHMIMIC, "§292"),
            ("ⲭⲉ", "subordinating", "that", "object_clause", Dialect.LYCOPOLITAN, "§292"),
            ("ⲭⲉ", "subordinating", "that", "object_clause", Dialect.FAYYUMIC, "§292"),

            # §296: With Future II/III - conjunctive "afin que (so that)"
            ("ⲭⲉⲕⲁⲁⲥ", "subordinating", "so that", "purpose", Dialect.SAHIDIC, "§296"),
            ("ⲭⲉⲕⲁⲥⲉ", "subordinating", "so that", "purpose", Dialect.LYCOPOLITAN, "§296"),
            ("ⲭⲉⲕⲁⲥ", "subordinating", "so that", "purpose", Dialect.FAYYUMIC, "§296"),
            ("ⲭⲉⲕⲉⲉⲥ", "subordinating", "so that", "purpose", Dialect.FAYYUMIC, "§296"),
        ]

        for form, conj_type, meaning, subtype, dialect, section in xe_forms:
            key = f"{form}_{dialect.value}"
            self.conjunctions[key] = ConjunctionForm(
                form, conj_type, meaning, subtype, dialect, section
            )
            # Register common forms
            if form in ["ⲭⲉ", "ⲭⲉⲕⲁⲁⲥ", "ⲭⲉⲕⲁⲥⲉ", "ⲭⲉⲕⲁⲥ"]:
                self.conjunctions[form] = ConjunctionForm(
                    form, conj_type, meaning, subtype, dialect, section
                )

        # §297: OTHER SUBORDINATING CONJUNCTIONS
        other_subord = [
            ("ⲭⲓⲛ", "subordinating", "while", "temporal", Dialect.SAHIDIC, "§297"),
            ("ⲓⲥⲭⲉⲛ", "subordinating", "while", "temporal", Dialect.BOHAIRIC, "§297"),
            ("ⲭⲛ", "subordinating", "while", "temporal", Dialect.AKHMIMIC, "§297"),
            ("ⲉⲙⲡⲁⲧⲉ", "subordinating", "since", "temporal", Dialect.SAHIDIC, "§297"),
            ("ⲃⲉ", "subordinating", "but, thus", "contrast", Dialect.SAHIDIC, "§297"),
            ("ⲃⲏ", "subordinating", "but, thus", "contrast", Dialect.FAYYUMIC, "§297"),
            ("ⲭⲉ", "subordinating", "but, thus", "contrast", Dialect.BOHAIRIC, "§297"),
            ("ⲛⲧⲟⲩ", "subordinating", "not yet", "negation", Dialect.SAHIDIC, "§297"),
            ("ⲛⲧⲁⲩ", "subordinating", "not yet", "negation", Dialect.BOHAIRIC, "§297"),
            ("ⲛⲑⲟⲩ", "subordinating", "not yet", "negation", Dialect.SAHIDIC, "§297"),
            ("ⲙⲱⲱⲩ", "subordinating", "but, on the contrary", "contrast", Dialect.SAHIDIC, "§297"),
            ("ⲉⲱⲱⲩ", "subordinating", "but, on the contrary", "contrast", Dialect.BOHAIRIC, "§297"),
            ("ⲣⲱ", "subordinating", "but", "contrast", Dialect.SAHIDIC, "§297"),
            ("ⲣⲟⲩ", "subordinating", "yes, of course", "affirmation", Dialect.AKHMIMIC, "§297"),
            ("ⲗⲱ", "subordinating", "yes, of course", "affirmation", Dialect.FAYYUMIC, "§297"),
        ]

        for form, conj_type, meaning, subtype, dialect, section in other_subord:
            key = f"{form}_{dialect.value}"
            self.conjunctions[key] = ConjunctionForm(
                form, conj_type, meaning, subtype, dialect, section
            )
            # Register common forms
            if form in ["ⲭⲓⲛ", "ⲓⲥⲭⲉⲛ", "ⲭⲛ", "ⲉⲙⲡⲁⲧⲉ"]:
                self.conjunctions[form] = ConjunctionForm(
                    form, conj_type, meaning, subtype, dialect, section
                )

        # §298: GREEK CONJUNCTIONS
        greek_conj = [
            ("ϩⲓⲛⲁ", "subordinating", "so that", "purpose_greek", Dialect.SAHIDIC, "§298"),
            ("ⲙⲏⲡⲱⲥ", "subordinating", "lest", "purpose_negative", Dialect.SAHIDIC, "§298"),
            ("ⲙⲏⲡⲟⲧⲉ", "subordinating", "lest", "purpose_negative", Dialect.SAHIDIC, "§298"),
            ("ϩⲱⲥⲧⲉ", "subordinating", "so that", "result", Dialect.SAHIDIC, "§298"),
            ("ϩⲱⲥ", "subordinating", "as if", "comparison", Dialect.SAHIDIC, "§298"),
            ("ⲇⲉ", "coordinating", "but", "contrast", Dialect.SAHIDIC, "§298"),
            ("ⲅⲁⲣ", "coordinating", "for", "reason", Dialect.SAHIDIC, "§298"),
            ("ⲟⲩⲛ", "coordinating", "also", "addition", Dialect.SAHIDIC, "§298"),
            ("ⲟⲩⲇⲉ", "coordinating", "and not", "negative_coordination", Dialect.SAHIDIC, "§298"),
            ("ⲟⲩⲧⲉ", "coordinating", "either...or", "disjunction", Dialect.SAHIDIC, "§298"),
        ]

        for form, conj_type, meaning, subtype, dialect, section in greek_conj:
            key = f"{form}_{dialect.value}_greek"
            self.conjunctions[key] = ConjunctionForm(
                form, conj_type, meaning, subtype, dialect, section
            )
            # Register common forms
            self.conjunctions[form] = ConjunctionForm(
                form, conj_type, meaning, subtype, dialect, section
            )

        # §300: COORDINATING CONJUNCTIONS "AND"
        # Propositions are often not linked (asyndeton), but when they are:

        coord_and = [
            ("ⲁⲩⲱ", "coordinating", "and", "addition", Dialect.SAHIDIC, "§300"),
            ("ⲁⲟⲩ", "coordinating", "and", "addition", Dialect.AKHMIMIC, "§300"),
            ("ⲟⲩⲟϩ", "coordinating", "and", "addition", Dialect.BOHAIRIC, "§300"),
            ("ⲟⲩⲁϩϩⲛ", "coordinating", "and", "addition", Dialect.LYCOPOLITAN, "§300"),
            ("ⲟⲩⲁϩⲁ", "coordinating", "and", "addition", Dialect.LYCOPOLITAN, "§300"),
        ]

        for form, conj_type, meaning, subtype, dialect, section in coord_and:
            key = f"{form}_{dialect.value}"
            self.conjunctions[key] = ConjunctionForm(
                form, conj_type, meaning, subtype, dialect, section
            )
            # Register common forms
            self.conjunctions[form] = ConjunctionForm(
                form, conj_type, meaning, subtype, dialect, section
            )

        # §301-303: ⲘⲚ/ⲚⲈⲘ - COMITATIVE "WITH"
        # Note: ⲙⲛ overlaps with genitive marker!
        # Context distinguishes: preposition "with" vs genitive "of"

        comitative = [
            ("ⲙⲛ", "comitative", "with, avec", "comitative", Dialect.SAHIDIC, "§301"),
            ("ⲛⲉⲙ", "comitative", "with, avec", "comitative", Dialect.BOHAIRIC, "§301"),
            ("ⲛⲉⲙ", "comitative", "with, avec", "comitative", Dialect.AKHMIMIC, "§301"),
        ]

        for form, conj_type, meaning, subtype, dialect, section in comitative:
            key = f"{form}_{dialect.value}_comitative"
            self.conjunctions[key] = ConjunctionForm(
                form, conj_type, meaning, subtype, dialect, section
            )

    def identify(self, word: str, dialect: Optional[Dialect] = None) -> Optional[ConjunctionForm]:
        """
        Identify conjunction in word.

        Args:
            word: Surface form
            dialect: Optional dialect hint

        Returns:
            ConjunctionForm if found, else None

        Example:
            >>> analyzer.identify("ⲭⲉ")
            ConjunctionForm(form="ⲭⲉ", type="subordinating", meaning="that", ...)

            >>> analyzer.identify("ⲁⲩⲱ")
            ConjunctionForm(form="ⲁⲩⲱ", type="coordinating", meaning="and", ...)
        """
        target_dialect = dialect or self.dialect

        # Try exact match first
        if word in self.conjunctions:
            return self.conjunctions[word]

        # Try dialect-specific
        key = f"{word}_{target_dialect.value}"
        if key in self.conjunctions:
            return self.conjunctions[key]

        # Try with type suffix for comitative
        comit_key = f"{word}_{target_dialect.value}_comitative"
        if comit_key in self.conjunctions:
            return self.conjunctions[comit_key]

        # Try Greek suffix
        greek_key = f"{word}_{target_dialect.value}_greek"
        if greek_key in self.conjunctions:
            return self.conjunctions[greek_key]

        # Try substring match for longer forms
        for conj_form, conj_data in self.conjunctions.items():
            if isinstance(conj_data, ConjunctionForm) and conj_data.form in word:
                return conj_data

        return None

    def identify_subordinating(self, word: str, dialect: Optional[Dialect] = None) -> Optional[ConjunctionForm]:
        """
        Identify subordinating conjunction.

        Args:
            word: Surface form
            dialect: Optional dialect hint

        Returns:
            ConjunctionForm if found and type is subordinating, else None
        """
        result = self.identify(word, dialect)
        if result and result.conj_type == "subordinating":
            return result
        return None

    def identify_coordinating(self, word: str, dialect: Optional[Dialect] = None) -> Optional[ConjunctionForm]:
        """
        Identify coordinating conjunction.

        Args:
            word: Surface form
            dialect: Optional dialect hint

        Returns:
            ConjunctionForm if found and type is coordinating, else None
        """
        result = self.identify(word, dialect)
        if result and result.conj_type == "coordinating":
            return result
        return None

    def identify_comitative(self, word: str, dialect: Optional[Dialect] = None) -> Optional[ConjunctionForm]:
        """
        Identify comitative conjunction ("with").

        Args:
            word: Surface form
            dialect: Optional dialect hint

        Returns:
            ConjunctionForm if found and type is comitative, else None
        """
        result = self.identify(word, dialect)
        if result and result.conj_type == "comitative":
            return result
        return None

    def is_conjunction(self, word: str, dialect: Optional[Dialect] = None) -> bool:
        """
        Check if word is a conjunction.

        Args:
            word: Surface form
            dialect: Optional dialect hint

        Returns:
            True if conjunction found, else False
        """
        return self.identify(word, dialect) is not None


def create_conjunctions_analyzer_till(dialect: Dialect = Dialect.SAHIDIC) -> CopticConjunctionsTill:
    """Factory function to create conjunctions analyzer."""
    return CopticConjunctionsTill(dialect=dialect)


if __name__ == "__main__":
    # Quick test
    analyzer = create_conjunctions_analyzer_till(dialect=Dialect.SAHIDIC)

    print("Testing conjunction recognition:")
    print("\nSubordinating conjunctions (§292-297):")
    test_subord = ["ⲭⲉ", "ⲭⲉⲕⲁⲁⲥ", "ⲭⲓⲛ", "ⲓⲥⲭⲉⲛ", "ⲉⲙⲡⲁⲧⲉ"]

    for word in test_subord:
        result = analyzer.identify_subordinating(word)
        if result:
            subtype_str = f" [{result.subtype}]" if result.subtype else ""
            print(f"✓ {word}: {result.meaning}{subtype_str}")
        else:
            print(f"✗ {word}: Not found")

    print("\nCoordinating conjunctions (§300):")
    test_coord = ["ⲁⲩⲱ", "ⲁⲟⲩ", "ⲟⲩⲟϩ"]

    for word in test_coord:
        result = analyzer.identify_coordinating(word)
        if result:
            print(f"✓ {word}: {result.meaning}")
        else:
            print(f"✗ {word}: Not found")

    print("\nGreek conjunctions (§298):")
    test_greek = ["ϩⲓⲛⲁ", "ⲙⲏⲡⲱⲥ", "ϩⲱⲥⲧⲉ", "ⲇⲉ", "ⲅⲁⲣ"]

    for word in test_greek:
        result = analyzer.identify(word)
        if result:
            subtype_str = f" [{result.subtype}]" if result.subtype else ""
            print(f"✓ {word}: {result.meaning}{subtype_str}")
        else:
            print(f"✗ {word}: Not found")

    print("\nComitative (§301):")
    test_comit = ["ⲙⲛ", "ⲛⲉⲙ"]

    for word in test_comit:
        result = analyzer.identify_comitative(word)
        if result:
            print(f"✓ {word}: {result.meaning}")
        else:
            print(f"✗ {word}: Not found")
