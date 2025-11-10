#!/usr/bin/env python3
"""
Coptic Dialect Handler
======================

Handles dialect variations across the seven Coptic dialects based on
Walter Till's dialectal grammar.

Dialects:
    S - Sahidic (Standard literary dialect)
    B - Bohairic (Northern dialect, liturgical)
    A - Akhmimic (Upper Egypt)
    L - Lycopolitan/Subakhmimic (Middle Egypt)
    F - Fayyumic (Fayyum region)
    M - Middle Egyptian Coptic
    P - Proto-Sahidic

Source: Walter Till, "Koptische Dialektgrammatik" (French translation)

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass


class Dialect(Enum):
    """Coptic dialect identifiers (Till's notation)"""
    SAHIDIC = 'S'           # Standard literary dialect
    BOHAIRIC = 'B'          # Northern, liturgical
    AKHMIMIC = 'A'          # Upper Egypt
    LYCOPOLITAN = 'L'       # Middle Egypt (Subakhmimic)
    FAYYUMIC = 'F'          # Fayyum
    MIDDLE_EGYPTIAN = 'M'   # Middle Egyptian Coptic
    PROTO_SAHIDIC = 'P'     # Early Sahidic

    @classmethod
    def from_code(cls, code: str) -> 'Dialect':
        """Get dialect from single-letter code"""
        code_map = {d.value: d for d in cls}
        if code not in code_map:
            raise ValueError(f"Unknown dialect code: {code}")
        return code_map[code]

    @property
    def full_name(self) -> str:
        """Get full name of dialect"""
        names = {
            'S': 'Sahidic',
            'B': 'Bohairic',
            'A': 'Akhmimic',
            'L': 'Lycopolitan',
            'F': 'Fayyumic',
            'M': 'Middle Egyptian',
            'P': 'Proto-Sahidic'
        }
        return names[self.value]


@dataclass
class DialectalForm:
    """Represents a morpheme with dialectal variations"""
    base_form: str                          # Standard form (usually Sahidic)
    dialect_forms: Dict[Dialect, str]       # Dialect-specific forms
    pos: str                                # Part of speech
    features: Dict[str, str]                # Morphological features
    source_section: Optional[str] = None    # Till section reference (e.g., "§246")

    def get_form(self, dialect: Dialect) -> str:
        """Get form for specific dialect, fallback to base_form"""
        return self.dialect_forms.get(dialect, self.base_form)

    def get_all_forms(self) -> Set[str]:
        """Get all variant forms across dialects"""
        forms = {self.base_form}
        forms.update(self.dialect_forms.values())
        return forms

    def matches_form(self, form: str, dialect: Optional[Dialect] = None) -> bool:
        """Check if form matches this morpheme in any or specific dialect"""
        if dialect:
            return form == self.get_form(dialect)
        return form in self.get_all_forms()


class DialectHandler:
    """
    Manages dialectal variations in Coptic morphology and syntax.

    Example usage:
        handler = DialectHandler(default_dialect=Dialect.SAHIDIC)

        # Register a dialectal form
        handler.register_form(
            base_form="ⲁ",
            dialect_forms={Dialect.BOHAIRIC: "ⲁϥ"},
            pos="APST",
            features={},
            source_section="§246"
        )

        # Get form for specific dialect
        form = handler.get_morpheme("ⲁ", Dialect.BOHAIRIC)
    """

    def __init__(self, default_dialect: Dialect = Dialect.SAHIDIC):
        """
        Initialize dialect handler.

        Args:
            default_dialect: Default dialect for parsing (default: Sahidic)
        """
        self.default_dialect = default_dialect
        self.forms: Dict[str, List[DialectalForm]] = {}  # base_form -> [DialectalForm]
        self.form_index: Dict[str, List[DialectalForm]] = {}  # any_form -> [DialectalForm]

    def register_form(
        self,
        base_form: str,
        dialect_forms: Dict[Dialect, str],
        pos: str,
        features: Dict[str, str],
        source_section: Optional[str] = None
    ) -> DialectalForm:
        """
        Register a morpheme with dialectal variations.

        Args:
            base_form: Standard form (usually Sahidic)
            dialect_forms: Dictionary of dialect-specific forms
            pos: Part of speech tag
            features: Morphological features
            source_section: Reference to Till's grammar section

        Returns:
            Created DialectalForm object
        """
        df = DialectalForm(
            base_form=base_form,
            dialect_forms=dialect_forms,
            pos=pos,
            features=features,
            source_section=source_section
        )

        # Index by base form
        if base_form not in self.forms:
            self.forms[base_form] = []
        self.forms[base_form].append(df)

        # Index by all variant forms
        for form in df.get_all_forms():
            if form not in self.form_index:
                self.form_index[form] = []
            self.form_index[form].append(df)

        return df

    def get_morpheme(
        self,
        form: str,
        dialect: Optional[Dialect] = None
    ) -> Optional[DialectalForm]:
        """
        Look up morpheme by form.

        Args:
            form: Surface form to look up
            dialect: Target dialect (uses default if None)

        Returns:
            Matching DialectalForm or None
        """
        target_dialect = dialect or self.default_dialect

        # Look up in form index
        candidates = self.form_index.get(form, [])

        for df in candidates:
            if df.matches_form(form, target_dialect):
                return df

        return None

    def get_all_variants(self, base_form: str) -> List[str]:
        """Get all dialectal variants of a base form"""
        forms = self.forms.get(base_form, [])
        all_variants = set()
        for df in forms:
            all_variants.update(df.get_all_forms())
        return sorted(all_variants)

    def detect_dialect(self, text: str) -> List[Tuple[Dialect, float]]:
        """
        Attempt to detect dialect from text features.

        Args:
            text: Coptic text

        Returns:
            List of (Dialect, confidence_score) tuples, sorted by confidence

        Note: This is heuristic-based and may not be accurate for short texts.
        """
        scores: Dict[Dialect, float] = {d: 0.0 for d in Dialect}

        # Dialectal markers (Till's grammar provides these)
        markers = {
            # Bohairic markers
            Dialect.BOHAIRIC: ['ϯ', 'ⲑⲏⲛⲟⲩ', 'ⲁϥ'],

            # Sahidic markers
            Dialect.SAHIDIC: ['ⲁ', 'ⲙⲡⲉ', 'ⲛⲧⲉⲣⲉ'],

            # Akhmimic markers
            Dialect.AKHMIMIC: ['ⲧⲁ', 'ⲛⲁ'],

            # Lycopolitan markers
            Dialect.LYCOPOLITAN: ['ⲁⲗ', 'ⲛⲧⲁⲗ'],

            # Fayyumic markers
            Dialect.FAYYUMIC: ['ⲗⲓ', 'ⲛⲉ'],
        }

        # Count marker occurrences
        for dialect, marker_list in markers.items():
            for marker in marker_list:
                if marker in text:
                    scores[dialect] += text.count(marker)

        # Normalize scores
        total = sum(scores.values())
        if total > 0:
            for dialect in scores:
                scores[dialect] /= total

        # Return sorted by confidence
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

    def set_default_dialect(self, dialect: Dialect):
        """Change the default dialect"""
        self.default_dialect = dialect

    def get_supported_dialects(self) -> List[Dialect]:
        """Get list of all supported dialects"""
        return list(Dialect)

    def export_dialect_table(self, base_forms: List[str]) -> str:
        """
        Export dialectal variation table in markdown format.

        Args:
            base_forms: List of base forms to include

        Returns:
            Markdown table string
        """
        lines = ["| Base Form | POS | " + " | ".join(d.value for d in Dialect) + " |"]
        lines.append("|-----------|-----|" + "|".join("---" for _ in Dialect) + "|")

        for base_form in base_forms:
            forms = self.forms.get(base_form, [])
            for df in forms:
                row = [base_form, df.pos]
                for dialect in Dialect:
                    form = df.get_form(dialect)
                    row.append(form)
                lines.append("| " + " | ".join(row) + " |")

        return "\n".join(lines)


def create_dialect_handler(default_dialect: Dialect = Dialect.SAHIDIC) -> DialectHandler:
    """
    Factory function to create dialect handler.

    Args:
        default_dialect: Default dialect for parsing

    Returns:
        Initialized DialectHandler
    """
    return DialectHandler(default_dialect)


# Convenience functions
def get_dialect_from_code(code: str) -> Dialect:
    """Get dialect enum from single-letter code"""
    return Dialect.from_code(code)


def list_dialects() -> List[str]:
    """Get list of all dialect codes"""
    return [d.value for d in Dialect]
