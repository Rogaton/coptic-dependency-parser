#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coptic Pronouns & Prepositions - Till's Dialectal Grammar (§122-172)

This module implements pronouns and prepositions from Walter Till's
"Koptische Dialektgrammatik" covering:
- §122-125: Demonstrative pronouns (ⲡⲁⲓ, ⲧⲁⲓ, ⲛⲁⲓ "this/that")
- §126-129: Possessive pronouns (ⲡⲁ-, ⲧⲁ-, ⲛⲁ- "my, your...")
- §130-145: Interrogatives & indefinites (ⲛⲓⲙ, ⲟⲩ, ⲗⲁⲁⲩ, ⲕⲉ)
- §146-172: Prepositions with pronominal forms (ⲉ, ⲛ, ϩⲛ, ⲉⲧⲃⲉ, etc.)

Author: André Linden (linden@bluewin.ch)
Date: 2025-11-09
Source: Till's Dialectal Grammar §122-172
License: CC BY-NC-SA 4.0
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from coptic_dialect_handler import Dialect, DialectalForm, DialectHandler


@dataclass
class PronounForm:
    """Represents a pronoun form with dialectal variations."""
    form: str
    pos: str
    features: Dict[str, str]
    dialect: Dialect
    source_section: Optional[str] = None


@dataclass
class PrepositionForm:
    """Represents a preposition with optional pronominal forms."""
    base_form: str
    pronominal_base: Optional[str]  # e.g., ⲉⲣⲟ= for ⲉ
    pos: str = "PREP"
    meaning: str = ""
    dialect: Dialect = Dialect.SAHIDIC
    source_section: Optional[str] = None


class CopticPronounsPrepositionsTill:
    """
    Handles Coptic pronouns and prepositions from Till's grammar.

    Covers §122-172:
    - Demonstrative pronouns (ⲡⲁⲓ, ⲧⲁⲓ, ⲛⲁⲓ)
    - Possessive pronouns (ⲡⲁ-, ⲧⲁ-, ⲛⲁ-)
    - Interrogatives (ⲛⲓⲙ, ⲟⲩ, ⲁϣ, ⲟⲩⲏⲣ)
    - Indefinites (ⲗⲁⲁⲩ, ⲟⲩⲟⲛ, ⲕⲉ)
    - Prepositions with pronominal suffixes
    """

    def __init__(self, dialect: Dialect = Dialect.SAHIDIC):
        """Initialize with specified dialect."""
        self.dialect = dialect
        self.dialect_handler = DialectHandler()

        # Initialize all pattern dictionaries
        self._init_demonstratives()
        self._init_possessives()
        self._init_interrogatives()
        self._init_indefinites()
        self._init_prepositions()
        self._init_adverbials()

    def _init_demonstratives(self):
        """Initialize demonstrative pronouns (§122-125)."""
        self.demonstratives = {}

        # §122: Basic demonstratives "this/that"
        # Sahidic
        self.demonstratives["ⲡⲁⲓ"] = ("ⲡⲁⲓ", "PDEM", {"Gender": "Masc", "Number": "Sing"}, "§122")
        self.demonstratives["ⲧⲁⲓ"] = ("ⲧⲁⲓ", "PDEM", {"Gender": "Fem", "Number": "Sing"}, "§122")
        self.demonstratives["ⲛⲁⲓ"] = ("ⲛⲁⲓ", "PDEM", {"Number": "Plur"}, "§122")

        # Bohairic
        self.demonstratives["ⲫⲁⲓ"] = ("ⲫⲁⲓ", "PDEM", {"Gender": "Masc", "Number": "Sing"}, "§122")
        self.demonstratives["ⲑⲁⲓ"] = ("ⲑⲁⲓ", "PDEM", {"Gender": "Fem", "Number": "Sing"}, "§122")

        # Akhmimic-Lycopolitan-Fayyumic
        self.demonstratives["ⲡⲉⲓ"] = ("ⲡⲉⲓ", "PDEM", {"Gender": "Masc", "Number": "Sing"}, "§122")
        self.demonstratives["ⲡⲉⲉⲓ"] = ("ⲡⲉⲉⲓ", "PDEM", {"Gender": "Masc", "Number": "Sing"}, "§122")
        self.demonstratives["ⲧⲉⲓ"] = ("ⲧⲉⲓ", "PDEM", {"Gender": "Fem", "Number": "Sing"}, "§122")
        self.demonstratives["ⲧⲉⲉⲓ"] = ("ⲧⲉⲉⲓ", "PDEM", {"Gender": "Fem", "Number": "Sing"}, "§122")
        self.demonstratives["ⲛⲉⲓ"] = ("ⲛⲉⲓ", "PDEM", {"Number": "Plur"}, "§122")
        self.demonstratives["ⲛⲉⲉⲓ"] = ("ⲛⲉⲉⲓ", "PDEM", {"Number": "Plur"}, "§122")

        # §123: ⲡⲏ "that one" (distal demonstrative)
        self.demonstratives["ⲡⲏ"] = ("ⲡⲏ", "PDEM", {"Gender": "Masc", "Number": "Sing", "Deixis": "Dist"}, "§123")
        self.demonstratives["ⲧⲏ"] = ("ⲧⲏ", "PDEM", {"Gender": "Fem", "Number": "Sing", "Deixis": "Dist"}, "§123")
        self.demonstratives["ⲛⲏ"] = ("ⲛⲏ", "PDEM", {"Number": "Plur", "Deixis": "Dist"}, "§123")
        self.demonstratives["ⲫⲏ"] = ("ⲫⲏ", "PDEM", {"Gender": "Masc", "Number": "Sing", "Deixis": "Dist"}, "§123")
        self.demonstratives["ⲑⲏ"] = ("ⲑⲏ", "PDEM", {"Gender": "Fem", "Number": "Sing", "Deixis": "Dist"}, "§123")

        # §125: ⲉⲧⲙⲙⲁⲩ "that one there" (distal emphatic)
        self.demonstratives["ⲉⲧⲙⲙⲁⲩ"] = ("ⲉⲧⲙⲙⲁⲩ", "PDEM", {"Deixis": "Dist", "Emphasis": "Yes"}, "§125")
        self.demonstratives["ⲉⲧⲉⲙⲙⲁⲩ"] = ("ⲉⲧⲉⲙⲙⲁⲩ", "PDEM", {"Deixis": "Dist", "Emphasis": "Yes"}, "§125")
        self.demonstratives["ⲉⲧⲙⲙⲟ"] = ("ⲉⲧⲙⲙⲟ", "PDEM", {"Deixis": "Dist", "Emphasis": "Yes"}, "§125")
        self.demonstratives["ⲉⲧⲙⲙⲉⲩ"] = ("ⲉⲧⲙⲙⲉⲩ", "PDEM", {"Deixis": "Dist", "Emphasis": "Yes"}, "§125")

    def _init_possessives(self):
        """Initialize possessive pronouns (§126-129)."""
        self.possessives = {}

        # §126: Possessive prefix "of -" (weak form before noun)
        # Sahidic/Lycopolitan/Fayyumic
        self.possessives["ⲡⲁ"] = ("ⲡⲁ", "POSS", {"Gender": "Masc", "Number": "Sing", "Form": "Prefix"}, "§126")
        self.possessives["ⲧⲁ"] = ("ⲧⲁ", "POSS", {"Gender": "Fem", "Number": "Sing", "Form": "Prefix"}, "§126")
        self.possessives["ⲛⲁ"] = ("ⲛⲁ", "POSS", {"Number": "Plur", "Form": "Prefix"}, "§126")

        # Bohairic
        self.possessives["ⲫⲁ"] = ("ⲫⲁ", "POSS", {"Gender": "Masc", "Number": "Sing", "Form": "Prefix"}, "§126")
        self.possessives["ⲑⲁ"] = ("ⲑⲁ", "POSS", {"Gender": "Fem", "Number": "Sing", "Form": "Prefix"}, "§126")

        # §127: Full possessive pronouns (strong form)
        # Sahidic/Akhmimic/Lycopolitan/Fayyumic
        self.possessives["ⲡⲱ"] = ("ⲡⲱ", "POSS", {"Gender": "Masc", "Form": "Full"}, "§127")
        self.possessives["ⲧⲱ"] = ("ⲧⲱ", "POSS", {"Gender": "Fem", "Form": "Full"}, "§127")
        self.possessives["ⲛⲟⲩ"] = ("ⲛⲟⲩ", "POSS", {"Number": "Plur", "Form": "Full"}, "§127")

        # Bohairic
        self.possessives["ⲫⲱ"] = ("ⲫⲱ", "POSS", {"Gender": "Masc", "Form": "Full"}, "§127")
        self.possessives["ⲑⲱ"] = ("ⲑⲱ", "POSS", {"Gender": "Fem", "Form": "Full"}, "§127")
        self.possessives["ⲛⲱⲩ"] = ("ⲛⲱⲩ", "POSS", {"Number": "Plur", "Form": "Full"}, "§127")

        # Special forms
        self.possessives["ⲡⲱⲓ"] = ("ⲡⲱⲓ", "POSS", {"Gender": "Masc", "Person": "1", "Number": "Sing"}, "§127")
        self.possessives["ⲫⲱⲓ"] = ("ⲫⲱⲓ", "POSS", {"Gender": "Masc", "Person": "1", "Number": "Sing"}, "§127")
        self.possessives["ⲛⲟⲩⲧⲛ"] = ("ⲛⲟⲩⲧⲛ", "POSS", {"Person": "2", "Number": "Plur", "Meaning": "yours"}, "§127")
        self.possessives["ⲛⲟⲩⲧⲉⲛ"] = ("ⲛⲟⲩⲧⲉⲛ", "POSS", {"Person": "2", "Number": "Plur", "Meaning": "yours"}, "§127")

    def _init_interrogatives(self):
        """Initialize interrogative pronouns (§130-135)."""
        self.interrogatives = {}

        # §130: ⲛⲓⲙ "who?" / "which?"
        self.interrogatives["ⲛⲓⲙ"] = ("ⲛⲓⲙ", "PINT", {"Meaning": "who/which"}, "§130")

        # §131: ⲟⲩ "what?"
        self.interrogatives["ⲟⲩ"] = ("ⲟⲩ", "PINT", {"Meaning": "what"}, "§131")
        self.interrogatives["ⲟ"] = ("ⲟ", "PINT", {"Meaning": "what"}, "§131")  # Akhmimic
        self.interrogatives["ⲉⲩ"] = ("ⲉⲩ", "PINT", {"Meaning": "what"}, "§131")  # Fayyumic
        self.interrogatives["ⲟⲩⲛ"] = ("ⲟⲩⲛ", "PINT", {"Meaning": "what"}, "§131")  # Fayyumic

        # §132: ⲁϣ "which?" / "which one?"
        self.interrogatives["ⲁϣ"] = ("ⲁϣ", "PINT", {"Meaning": "which"}, "§132")
        self.interrogatives["ⲉϣ"] = ("ⲉϣ", "PINT", {"Meaning": "which"}, "§132")  # Lycopolitan/Fayyumic
        self.interrogatives["ⲉϣϩ"] = ("ⲉϣϩ", "PINT", {"Meaning": "which"}, "§132")  # Akhmimic

        # §133: ⲟⲩⲏⲣ "how many?"
        self.interrogatives["ⲟⲩⲏⲣ"] = ("ⲟⲩⲏⲣ", "PINT", {"Meaning": "how_many"}, "§133")
        self.interrogatives["ⲟⲩⲏⲗ"] = ("ⲟⲩⲏⲗ", "PINT", {"Meaning": "how_many"}, "§133")  # Fayyumic

        # §134: ⲁϩⲣⲟ= "why?"
        self.interrogatives["ⲁϩⲣⲟ"] = ("ⲁϩⲣⲟ", "PINT", {"Meaning": "why"}, "§134")
        self.interrogatives["ⲁϫⲟ"] = ("ⲁϫⲟ", "PINT", {"Meaning": "why"}, "§134")  # Bohairic
        self.interrogatives["ⲁϩⲣⲁ"] = ("ⲁϩⲣⲁ", "PINT", {"Meaning": "why"}, "§134")  # Akhmimic/Lycopolitan

    def _init_indefinites(self):
        """Initialize indefinite pronouns (§136-145)."""
        self.indefinites = {}

        # §136-137: ⲗⲁⲁⲩ "someone/something" or "nothing" (in negation)
        self.indefinites["ⲗⲁⲁⲩ"] = ("ⲗⲁⲁⲩ", "PIND", {"Meaning": "someone/something"}, "§136")
        self.indefinites["ⲗⲁⲩⲉ"] = ("ⲗⲁⲩⲉ", "PIND", {"Meaning": "someone/something"}, "§136")  # Akhmimic/Lycopolitan
        self.indefinites["ϩⲗⲓ"] = ("ϩⲗⲓ", "PIND", {"Meaning": "someone/something"}, "§136")  # Bohairic
        self.indefinites["ϩⲗⲉⲓ"] = ("ϩⲗⲉⲓ", "PIND", {"Meaning": "someone/something"}, "§136")  # Akhmimic
        self.indefinites["ⲗⲁⲡⲥ"] = ("ⲗⲁⲡⲥ", "PIND", {"Meaning": "someone/something"}, "§136")  # Fayyumic
        self.indefinites["ⲗⲁⲡⲧ"] = ("ⲗⲁⲡⲧ", "PIND", {"Meaning": "someone/something"}, "§136")  # Fayyumic

        # §138: ⲟⲩⲟⲛ "someone/something"
        self.indefinites["ⲟⲩⲟⲛ"] = ("ⲟⲩⲟⲛ", "PIND", {"Meaning": "someone/something"}, "§138")
        self.indefinites["ⲟⲩⲁⲛ"] = ("ⲟⲩⲁⲛ", "PIND", {"Meaning": "someone/something"}, "§138")  # Akhmimic/Lycopolitan/Fayyumic
        self.indefinites["ϩⲁⲛⲟⲩⲟⲛ"] = ("ϩⲁⲛⲟⲩⲟⲛ", "PIND", {"Meaning": "quelques/some"}, "§138")  # Bohairic
        self.indefinites["ϩⲟⲉⲓⲛⲉ"] = ("ϩⲟⲉⲓⲛⲉ", "PIND", {"Meaning": "quelques/some"}, "§138")  # Sahidic
        self.indefinites["ϩⲁⲉⲓⲛⲉ"] = ("ϩⲁⲉⲓⲛⲉ", "PIND", {"Meaning": "quelques/some"}, "§138")  # Fayyumic

        # §139: ⲟⲩⲁ "one/someone"
        self.indefinites["ⲟⲩⲁ"] = ("ⲟⲩⲁ", "PIND", {"Meaning": "one/someone"}, "§139")
        self.indefinites["ⲟⲩⲁⲓ"] = ("ⲟⲩⲁⲓ", "PIND", {"Meaning": "one/someone"}, "§139")  # Bohairic
        self.indefinites["ⲟⲩⲉ"] = ("ⲟⲩⲉ", "PIND", {"Meaning": "one/someone"}, "§139")  # Akhmimic/Lycopolitan
        self.indefinites["ⲟⲩⲉⲓ"] = ("ⲟⲩⲉⲓ", "PIND", {"Meaning": "one/someone"}, "§139")  # Lycopolitan/Fayyumic/feminine
        self.indefinites["ⲟⲩⲉⲉⲓ"] = ("ⲟⲩⲉⲉⲓ", "PIND", {"Meaning": "one/someone"}, "§139")  # Fayyumic
        self.indefinites["ⲟⲩⲓ"] = ("ⲟⲩⲓ", "PIND", {"Meaning": "one/someone", "Gender": "Fem"}, "§139")  # Bohairic/Fayyumic fem
        self.indefinites["ⲟⲩⲉⲓⲥ"] = ("ⲟⲩⲉⲓⲥ", "PIND", {"Meaning": "one/someone", "Gender": "Fem"}, "§139")  # Akhmimic fem

        # §141: ⲛⲓⲙ "each/every" (after noun)
        self.indefinites["ⲛⲓⲃⲉⲛ"] = ("ⲛⲓⲃⲉⲛ", "PIND", {"Meaning": "each/every"}, "§141")  # Bohairic
        self.indefinites["ⲛⲓⲃⲓ"] = ("ⲛⲓⲃⲓ", "PIND", {"Meaning": "each/every"}, "§141")  # Fayyumic

        # §142-144: ⲕⲉ "other/another"
        self.indefinites["ⲕⲉ"] = ("ⲕⲉ", "PIND", {"Meaning": "other/another"}, "§142")
        self.indefinites["ⲕⲉⲧ"] = ("ⲕⲉⲧ", "PIND", {"Meaning": "other/another"}, "§142")
        self.indefinites["ⲭⲉⲧ"] = ("ⲭⲉⲧ", "PIND", {"Meaning": "other/another"}, "§142")  # Bohairic
        self.indefinites["ⲕⲏ"] = ("ⲕⲏ", "PIND", {"Meaning": "other/another"}, "§142")  # Fayyumic
        self.indefinites["ⲕⲏⲧ"] = ("ⲕⲏⲧ", "PIND", {"Meaning": "other/another"}, "§142")  # Fayyumic
        self.indefinites["ⲕⲉⲧⲥ"] = ("ⲕⲉⲧⲥ", "PIND", {"Meaning": "other/another", "Gender": "Fem"}, "§142")
        self.indefinites["ⲕⲉⲕⲟⲟⲩⲉ"] = ("ⲕⲉⲕⲟⲟⲩⲉ", "PIND", {"Meaning": "others", "Number": "Plur"}, "§142")
        self.indefinites["ⲕⲉⲕⲉⲟⲩⲉ"] = ("ⲕⲉⲕⲉⲟⲩⲉ", "PIND", {"Meaning": "others", "Number": "Plur"}, "§142")
        self.indefinites["ⲕⲉⲕⲁⲩⲉ"] = ("ⲕⲉⲕⲁⲩⲉ", "PIND", {"Meaning": "others", "Number": "Plur"}, "§142")
        self.indefinites["ⲕⲉⲭⲱⲟⲩⲛⲓ"] = ("ⲕⲉⲭⲱⲟⲩⲛⲓ", "PIND", {"Meaning": "others", "Number": "Plur"}, "§142")  # Bohairic
        self.indefinites["ⲕⲉϩⲓ"] = ("ⲕⲉϩⲓ", "PIND", {"Meaning": "another (house)"}, "§143")
        self.indefinites["ⲕⲉⲟⲩⲁ"] = ("ⲕⲉⲟⲩⲁ", "PIND", {"Meaning": "another one"}, "§143")

    def _init_prepositions(self):
        """Initialize prepositions (§146-170)."""
        self.prepositions = {}

        # §147: ⲁⲭⲛ "without"
        self.prepositions["ⲁⲭⲛ"] = PrepositionForm("ⲁⲭⲛ", "ⲁⲭⲛⲧ=", "PREP", "without", Dialect.SAHIDIC, "§147")
        self.prepositions["ⲁⲭⲛⲧ"] = PrepositionForm("ⲁⲭⲛⲧ", None, "PREP", "without", Dialect.SAHIDIC, "§147")
        self.prepositions["ⲁⲕⲛⲉ"] = PrepositionForm("ⲁⲕⲛⲉ", None, "PREP", "without", Dialect.BOHAIRIC, "§147")
        self.prepositions["ⲁⲧⲕⲛⲉ"] = PrepositionForm("ⲁⲧⲕⲛⲉ", None, "PREP", "without", Dialect.BOHAIRIC, "§147")
        self.prepositions["ⲁⲧⲕⲛⲟⲩ"] = PrepositionForm("ⲁⲧⲕⲛⲟⲩ", None, "PREP", "without", Dialect.BOHAIRIC, "§147")
        self.prepositions["ⲁⲭⲉⲛ"] = PrepositionForm("ⲁⲭⲉⲛ", "ⲁⲭⲉⲛⲧ=", "PREP", "without", Dialect.FAYYUMIC, "§147")

        # §148: ⲉ "to, toward" (VERY COMMON!)
        self.prepositions["ⲉ"] = PrepositionForm("ⲉ", "ⲉⲣⲟ=", "PREP", "to/toward", Dialect.SAHIDIC, "§148")
        self.prepositions["ⲉⲣⲟ"] = PrepositionForm("ⲉⲣⲟ", None, "PREP", "to/toward", Dialect.SAHIDIC, "§148")
        self.prepositions["ⲉⲗⲁϭ"] = PrepositionForm("ⲉⲗⲁϭ", None, "PREP", "to/toward", Dialect.FAYYUMIC, "§148")
        self.prepositions["ⲁ"] = PrepositionForm("ⲁ", "ⲁⲣⲁ=", "PREP", "to/toward", Dialect.AKHMIMIC, "§148")
        self.prepositions["ⲁⲣⲁ"] = PrepositionForm("ⲁⲣⲁ", None, "PREP", "to/toward", Dialect.AKHMIMIC, "§148")
        self.prepositions["ⲁⲣⲟ"] = PrepositionForm("ⲁⲣⲟ", None, "PREP", "to/toward", Dialect.AKHMIMIC, "§148")
        self.prepositions["ⲉⲗⲁ"] = PrepositionForm("ⲉⲗⲁ", None, "PREP", "to/toward", Dialect.FAYYUMIC, "§148")

        # §149: ⲉⲣⲁⲧ= "toward -"
        self.prepositions["ⲉⲣⲁⲧ"] = PrepositionForm("ⲉⲣⲁⲧ", None, "PREP", "toward", Dialect.SAHIDIC, "§149")
        self.prepositions["ⲁⲣⲉⲧ"] = PrepositionForm("ⲁⲣⲉⲧ", None, "PREP", "toward", Dialect.AKHMIMIC, "§149")
        self.prepositions["ⲉⲗⲉⲧ"] = PrepositionForm("ⲉⲗⲉⲧ", None, "PREP", "toward", Dialect.FAYYUMIC, "§149")

        # §150: ⲉⲧⲃⲉ "because of, concerning" (VERY COMMON!)
        self.prepositions["ⲉⲧⲃⲉ"] = PrepositionForm("ⲉⲧⲃⲉ", "ⲉⲧⲃⲏⲏⲧ=", "PREP", "because_of", Dialect.SAHIDIC, "§150")
        self.prepositions["ⲉⲧⲃⲏⲏⲧ"] = PrepositionForm("ⲉⲧⲃⲏⲏⲧ", None, "PREP", "because_of", Dialect.SAHIDIC, "§150")
        self.prepositions["ⲉⲧⲃⲏⲧ"] = PrepositionForm("ⲉⲧⲃⲏⲧ", None, "PREP", "because_of", Dialect.AKHMIMIC, "§150")
        self.prepositions["ⲉⲑⲃⲉ"] = PrepositionForm("ⲉⲑⲃⲉ", "ⲉⲑⲃⲏⲧ=", "PREP", "because_of", Dialect.BOHAIRIC, "§150")
        self.prepositions["ⲉⲑⲃⲏⲧ"] = PrepositionForm("ⲉⲑⲃⲏⲧ", None, "PREP", "because_of", Dialect.BOHAIRIC, "§150")

        # §151: ⲉⲭⲛ "on, upon" (direction)
        self.prepositions["ⲉⲭⲛ"] = PrepositionForm("ⲉⲭⲛ", "ⲉⲭⲱ=", "PREP", "on/upon", Dialect.SAHIDIC, "§151")
        self.prepositions["ⲉⲭⲉⲛ"] = PrepositionForm("ⲉⲭⲉⲛ", "ⲉⲭⲱ=", "PREP", "on/upon", Dialect.BOHAIRIC, "§151")
        self.prepositions["ⲁⲭⲛ"] = PrepositionForm("ⲁⲭⲛ", "ⲁⲭⲱ=", "PREP", "on/upon", Dialect.AKHMIMIC, "§151")
        self.prepositions["ⲉⲭⲱ"] = PrepositionForm("ⲉⲭⲱ", None, "PREP", "on/upon", Dialect.SAHIDIC, "§151")
        self.prepositions["ⲁⲭⲱ"] = PrepositionForm("ⲁⲭⲱ", None, "PREP", "on/upon", Dialect.AKHMIMIC, "§151")

        # §152: ⲉⲓⲥ "since, from"
        self.prepositions["ⲉⲓⲥ"] = PrepositionForm("ⲉⲓⲥ", None, "PREP", "since/from", Dialect.SAHIDIC, "§152")
        self.prepositions["ⲉⲥ"] = PrepositionForm("ⲉⲥ", None, "PREP", "since/from", Dialect.AKHMIMIC, "§152")
        self.prepositions["ⲓⲥ"] = PrepositionForm("ⲓⲥ", None, "PREP", "since/from", Dialect.BOHAIRIC, "§152")

        # §153: ⲙⲛ "with; and" (VERY COMMON!)
        self.prepositions["ⲙⲛ"] = PrepositionForm("ⲙⲛ", "ⲛⲙⲙⲁ=", "PREP", "with/and", Dialect.SAHIDIC, "§153")
        self.prepositions["ⲛⲙⲙⲁ"] = PrepositionForm("ⲛⲙⲙⲁ", None, "PREP", "with/and", Dialect.SAHIDIC, "§153")
        self.prepositions["ⲛⲉⲙ"] = PrepositionForm("ⲛⲉⲙ", "ⲛⲉⲙⲁ=", "PREP", "with/and", Dialect.BOHAIRIC, "§153")
        self.prepositions["ⲛⲉⲙⲁ"] = PrepositionForm("ⲛⲉⲙⲁ", None, "PREP", "with/and", Dialect.BOHAIRIC, "§153")
        self.prepositions["ⲛⲙⲙⲁ"] = PrepositionForm("ⲛⲙⲙⲁ", None, "PREP", "with/and", Dialect.AKHMIMIC, "§153")
        self.prepositions["ⲛⲉⲙⲉ"] = PrepositionForm("ⲛⲉⲙⲉ", None, "PREP", "with/and", Dialect.AKHMIMIC, "§153")
        self.prepositions["ⲛⲉⲙⲏ"] = PrepositionForm("ⲛⲉⲙⲏ", None, "PREP", "with/and", Dialect.FAYYUMIC, "§153")

        # §154: ⲙⲛⲛⲥⲁ "after" (temporal)
        self.prepositions["ⲙⲛⲛⲥⲁ"] = PrepositionForm("ⲙⲛⲛⲥⲁ", "ⲙⲛⲛⲥⲱ=", "PREP", "after", Dialect.SAHIDIC, "§154")
        self.prepositions["ⲙⲉⲛⲉⲛⲥⲁ"] = PrepositionForm("ⲙⲉⲛⲉⲛⲥⲁ", "ⲙⲉⲛⲉⲛⲥⲱ", "PREP", "after", Dialect.BOHAIRIC, "§154")
        self.prepositions["ⲙⲛⲛⲥⲉ"] = PrepositionForm("ⲙⲛⲛⲥⲉ", None, "PREP", "after", Dialect.AKHMIMIC, "§154")
        self.prepositions["ⲙⲛⲛⲥⲱϩ"] = PrepositionForm("ⲙⲛⲛⲥⲱϩ", None, "PREP", "after", Dialect.SAHIDIC, "§154")

        # §155: ⲙⲡⲉⲙⲧⲟ ⲉⲃⲟⲗ ⲛ "in presence of"
        # Complex prepositional phrase - will handle in phrase analysis

        # §156: ⲛ/ⲙⲙⲟ= "in, of" (VERY COMMON! - genitive replacement)
        self.prepositions["ⲛ"] = PrepositionForm("ⲛ", "ⲙⲙⲟ=", "PREP", "of/in", Dialect.SAHIDIC, "§156")
        self.prepositions["ⲙⲙⲟ"] = PrepositionForm("ⲙⲙⲟ", None, "PREP", "of/in", Dialect.SAHIDIC, "§156")
        self.prepositions["ⲙⲙⲁ"] = PrepositionForm("ⲙⲙⲁ", None, "PREP", "of/in", Dialect.AKHMIMIC, "§156")

        # §157: ⲛ/ⲛⲁ= dative "to/for" (VERY COMMON!)
        self.prepositions["ⲛⲁ"] = PrepositionForm("ⲛⲁ", None, "PREP", "to/for", Dialect.SAHIDIC, "§157")
        self.prepositions["ⲛⲉ"] = PrepositionForm("ⲛⲉ", None, "PREP", "to/for", Dialect.AKHMIMIC, "§157")
        self.prepositions["ⲛⲏ"] = PrepositionForm("ⲛⲏ", None, "PREP", "to/for", Dialect.FAYYUMIC, "§157")
        self.prepositions["ⲛⲁⲓ"] = PrepositionForm("ⲛⲁⲓ", None, "PREP", "to/for", Dialect.SAHIDIC, "§157")  # 1sg
        self.prepositions["ⲛⲏⲓ"] = PrepositionForm("ⲛⲏⲓ", None, "PREP", "to/for", Dialect.BOHAIRIC, "§157")  # 1sg
        self.prepositions["ⲛⲁⲩ"] = PrepositionForm("ⲛⲁⲩ", None, "PREP", "to/for", Dialect.SAHIDIC, "§157")  # 3pl
        self.prepositions["ⲛⲉⲩ"] = PrepositionForm("ⲛⲉⲩ", None, "PREP", "to/for", Dialect.AKHMIMIC, "§157")  # 3pl
        self.prepositions["ⲛⲏⲩ"] = PrepositionForm("ⲛⲏⲩ", None, "PREP", "to/for", Dialect.FAYYUMIC, "§157")  # 3pl
        self.prepositions["ⲛⲱⲟⲩ"] = PrepositionForm("ⲛⲱⲟⲩ", None, "PREP", "to/for", Dialect.BOHAIRIC, "§157")  # 3pl

        # §158: ⲛⲥⲁ/ⲛⲥⲱ= "after" (place), "except"
        self.prepositions["ⲛⲥⲁ"] = PrepositionForm("ⲛⲥⲁ", "ⲛⲥⲱ=", "PREP", "after/except", Dialect.SAHIDIC, "§158")
        self.prepositions["ⲛⲥⲱ"] = PrepositionForm("ⲛⲥⲱ", None, "PREP", "after/except", Dialect.SAHIDIC, "§158")
        self.prepositions["ⲥⲉ"] = PrepositionForm("ⲥⲉ", None, "PREP", "after/except", Dialect.AKHMIMIC, "§158")

        # §159: ⲛⲁϩⲣⲛ "in presence of" (person)
        self.prepositions["ⲛⲁϩⲣⲛ"] = PrepositionForm("ⲛⲁϩⲣⲛ", "ⲛⲁϩⲣⲁ=", "PREP", "before/in_presence", Dialect.SAHIDIC, "§159")
        self.prepositions["ⲛⲛⲁϩⲣⲛ"] = PrepositionForm("ⲛⲛⲁϩⲣⲛ", "ⲛⲛⲁϩⲣⲁ=", "PREP", "before/in_presence", Dialect.SAHIDIC, "§159")
        self.prepositions["ⲛⲁϩⲣⲉⲛ"] = PrepositionForm("ⲛⲁϩⲣⲉⲛ", None, "PREP", "before/in_presence", Dialect.BOHAIRIC, "§159")
        self.prepositions["ⲛⲛⲁϩⲣⲉⲛ"] = PrepositionForm("ⲛⲛⲁϩⲣⲉⲛ", None, "PREP", "before/in_presence", Dialect.BOHAIRIC, "§159")
        self.prepositions["ⲛⲁϩⲣⲁ"] = PrepositionForm("ⲛⲁϩⲣⲁ", None, "PREP", "before/in_presence", Dialect.SAHIDIC, "§159")
        self.prepositions["ⲛⲁϩⲣⲉ"] = PrepositionForm("ⲛⲁϩⲣⲉ", None, "PREP", "before/in_presence", Dialect.FAYYUMIC, "§159")

        # §160: ⲟⲩⲃⲉ "against"
        self.prepositions["ⲟⲩⲃⲉ"] = PrepositionForm("ⲟⲩⲃⲉ", "ⲟⲩⲃⲏ=", "PREP", "against", Dialect.SAHIDIC, "§160")
        self.prepositions["ⲟⲩⲃⲏ"] = PrepositionForm("ⲟⲩⲃⲏ", None, "PREP", "against", Dialect.FAYYUMIC, "§160")
        self.prepositions["ⲟⲩⲉ"] = PrepositionForm("ⲟⲩⲉ", None, "PREP", "against", Dialect.FAYYUMIC, "§160")
        self.prepositions["ⲟⲩⲏ"] = PrepositionForm("ⲟⲩⲏ", None, "PREP", "against", Dialect.FAYYUMIC, "§160")

        # §161: ⲟⲩⲧⲉ/ⲟⲩⲧⲱ= "between"
        self.prepositions["ⲟⲩⲧⲉ"] = PrepositionForm("ⲟⲩⲧⲉ", "ⲟⲩⲧⲱ=", "PREP", "between", Dialect.SAHIDIC, "§161")
        self.prepositions["ⲟⲩⲧⲱ"] = PrepositionForm("ⲟⲩⲧⲱ", None, "PREP", "between", Dialect.SAHIDIC, "§161")
        self.prepositions["ⲟⲩⲧⲱⲕ"] = PrepositionForm("ⲟⲩⲧⲱⲕ", None, "PREP", "between", Dialect.SAHIDIC, "§161")  # you
        self.prepositions["ⲟⲩⲧⲱϥ"] = PrepositionForm("ⲟⲩⲧⲱϥ", None, "PREP", "between", Dialect.SAHIDIC, "§161")  # him

        # §162: ϣⲁ= "until, toward"
        self.prepositions["ϣⲁ"] = PrepositionForm("ϣⲁ", None, "PREP", "until/toward", Dialect.SAHIDIC, "§162")

        # §163: ϣⲁ/ϣⲁⲣⲟ= "to, at"
        self.prepositions["ϣⲁⲣⲟ"] = PrepositionForm("ϣⲁⲣⲟ", None, "PREP", "to/at", Dialect.AKHMIMIC, "§163")
        self.prepositions["ϣⲁⲣⲁ"] = PrepositionForm("ϣⲁⲣⲁ", None, "PREP", "to/at", Dialect.AKHMIMIC, "§163")
        self.prepositions["ϣⲁⲁ"] = PrepositionForm("ϣⲁⲁ", None, "PREP", "to/at", Dialect.LYCOPOLITAN, "§163")
        self.prepositions["ϣϫⲗⲁϭ"] = PrepositionForm("ϣϫⲗⲁϭ", None, "PREP", "to/at", Dialect.FAYYUMIC, "§163")
        self.prepositions["ϩⲁⲣⲟ"] = PrepositionForm("ϩⲁⲣⲟ", None, "PREP", "to/at", Dialect.BOHAIRIC, "§163")

        # §164: ϩⲁ/ϩⲁⲣⲟ= "under; for" (VERY COMMON!)
        self.prepositions["ϩⲁ"] = PrepositionForm("ϩⲁ", "ϩⲁⲣⲟ=", "PREP", "under/for", Dialect.SAHIDIC, "§164")
        self.prepositions["ϫⲁ"] = PrepositionForm("ϫⲁ", "ϫⲁⲣⲟ=", "PREP", "under/for", Dialect.BOHAIRIC, "§164")
        self.prepositions["ⲑⲁ"] = PrepositionForm("ⲑⲁ", "ⲑⲁⲣⲟ=", "PREP", "under/for", Dialect.AKHMIMIC, "§164")
        self.prepositions["ϩⲁⲣⲟ"] = PrepositionForm("ϩⲁⲣⲟ", None, "PREP", "under/for", Dialect.SAHIDIC, "§164")
        self.prepositions["ϩⲁⲣⲁ"] = PrepositionForm("ϩⲁⲣⲁ", None, "PREP", "under/for", Dialect.LYCOPOLITAN, "§164")
        self.prepositions["ϩⲁⲗⲁ"] = PrepositionForm("ϩⲁⲗⲁ", None, "PREP", "under/for", Dialect.FAYYUMIC, "§164")
        self.prepositions["ϫⲁⲣⲟ"] = PrepositionForm("ϫⲁⲣⲟ", None, "PREP", "under/for", Dialect.BOHAIRIC, "§164")
        self.prepositions["ⲑⲁⲣⲟ"] = PrepositionForm("ⲑⲁⲣⲟ", None, "PREP", "under/for", Dialect.AKHMIMIC, "§164")
        self.prepositions["ⲑⲁⲣⲁ"] = PrepositionForm("ⲑⲁⲣⲁ", None, "PREP", "under/for", Dialect.AKHMIMIC, "§164")

        # §165: ϩⲓ/ϩⲓⲱⲱ= "on" (without movement) (VERY COMMON!)
        self.prepositions["ϩⲓ"] = PrepositionForm("ϩⲓ", "ϩⲓⲱⲱ=", "PREP", "on", Dialect.SAHIDIC, "§165")
        self.prepositions["ϩⲓⲱⲱ"] = PrepositionForm("ϩⲓⲱⲱ", None, "PREP", "on", Dialect.SAHIDIC, "§165")
        self.prepositions["ϩⲓⲱⲧ"] = PrepositionForm("ϩⲓⲱⲧ", None, "PREP", "on", Dialect.BOHAIRIC, "§165")

        # §166: ϩⲛ/ⲛϩⲏⲧ= "in; by; through" (EXTREMELY COMMON!)
        self.prepositions["ϩⲛ"] = PrepositionForm("ϩⲛ", "ⲛϩⲏⲧ=", "PREP", "in/by", Dialect.SAHIDIC, "§166")
        self.prepositions["ⲛϩⲏⲧ"] = PrepositionForm("ⲛϩⲏⲧ", None, "PREP", "in/by", Dialect.SAHIDIC, "§166")
        self.prepositions["ϩⲙ"] = PrepositionForm("ϩⲙ", "ⲛϩⲏⲧ=", "PREP", "in/by", Dialect.SAHIDIC, "§166")  # before ⲡ
        self.prepositions["ϫⲉⲛ"] = PrepositionForm("ϫⲉⲛ", "ⲛϫⲏⲧ=", "PREP", "in/by", Dialect.BOHAIRIC, "§166")
        self.prepositions["ⲛϫⲏⲧ"] = PrepositionForm("ⲛϫⲏⲧ", None, "PREP", "in/by", Dialect.BOHAIRIC, "§166")
        self.prepositions["ⲑⲉⲛ"] = PrepositionForm("ⲑⲉⲛ", "ⲛϩⲏⲧ=", "PREP", "in/by", Dialect.AKHMIMIC, "§166")

        # §167: ϩⲓⲧⲛ/ϩⲓⲧⲟⲟⲧ= "by, through" (passive agent)
        self.prepositions["ϩⲓⲧⲛ"] = PrepositionForm("ϩⲓⲧⲛ", "ϩⲓⲧⲟⲟⲧ=", "PREP", "by/through", Dialect.SAHIDIC, "§167")
        self.prepositions["ϩⲓⲧⲟⲟⲧ"] = PrepositionForm("ϩⲓⲧⲟⲟⲧ", None, "PREP", "by/through", Dialect.SAHIDIC, "§167")
        self.prepositions["ϩⲓⲧⲉⲛ"] = PrepositionForm("ϩⲓⲧⲉⲛ", "ϩⲓⲧⲟⲟⲧ=", "PREP", "by/through", Dialect.BOHAIRIC, "§167")
        self.prepositions["ϩⲓⲧⲁⲁⲧ"] = PrepositionForm("ϩⲓⲧⲁⲁⲧ", None, "PREP", "by/through", Dialect.FAYYUMIC, "§167")

        # §168: ϩⲓⲭⲛ/ϩⲓⲭⲱ= "on" (without movement)
        self.prepositions["ϩⲓⲭⲛ"] = PrepositionForm("ϩⲓⲭⲛ", "ϩⲓⲭⲱ=", "PREP", "on", Dialect.SAHIDIC, "§168")
        self.prepositions["ϩⲓⲭⲉⲛ"] = PrepositionForm("ϩⲓⲭⲉⲛ", "ϩⲓⲭⲱ=", "PREP", "on", Dialect.BOHAIRIC, "§168")
        self.prepositions["ϩⲓⲭⲱ"] = PrepositionForm("ϩⲓⲭⲱ", None, "PREP", "on", Dialect.SAHIDIC, "§168")
        # Variants with ϫ instead of ⲭ (different chi forms in manuscripts)
        self.prepositions["ϩⲓϫⲛ"] = PrepositionForm("ϩⲓϫⲛ", "ϩⲓϫⲱ=", "PREP", "on", Dialect.SAHIDIC, "§168")
        self.prepositions["ϩⲓϫⲱ"] = PrepositionForm("ϩⲓϫⲱ", None, "PREP", "on", Dialect.SAHIDIC, "§168")

        # §169: ϩⲓⲛ/ⲓⲥⲭⲉⲛ "since, from, starting from"
        self.prepositions["ϩⲓⲛ"] = PrepositionForm("ϩⲓⲛ", None, "PREP", "since/from", Dialect.SAHIDIC, "§169")
        self.prepositions["ϫⲓⲛ"] = PrepositionForm("ϫⲓⲛ", None, "PREP", "since/from", Dialect.AKHMIMIC, "§169")
        self.prepositions["ⲓⲥⲭⲉⲛ"] = PrepositionForm("ⲓⲥⲭⲉⲛ", None, "PREP", "since/from", Dialect.BOHAIRIC, "§169")

        # §170: Greek prepositions used in Coptic
        self.prepositions["ⲕⲁⲧⲁ"] = PrepositionForm("ⲕⲁⲧⲁ", "ⲕⲁⲧⲁⲣⲟ=", "PREP", "according_to", Dialect.SAHIDIC, "§170")
        self.prepositions["ⲕⲁⲧⲁⲣⲟ"] = PrepositionForm("ⲕⲁⲧⲁⲣⲟ", None, "PREP", "according_to", Dialect.SAHIDIC, "§170")
        self.prepositions["ⲕⲁⲧⲁⲗⲁ"] = PrepositionForm("ⲕⲁⲧⲁⲗⲁ", None, "PREP", "according_to", Dialect.FAYYUMIC, "§170")
        self.prepositions["ⲡⲁⲣⲁ"] = PrepositionForm("ⲡⲁⲣⲁ", "ⲡⲁⲣⲁⲣⲟ=", "PREP", "compared_to", Dialect.SAHIDIC, "§170")
        self.prepositions["ⲡⲁⲣⲁⲣⲟ"] = PrepositionForm("ⲡⲁⲣⲁⲣⲟ", None, "PREP", "compared_to", Dialect.SAHIDIC, "§170")
        self.prepositions["ⲡⲁⲣⲁⲣⲁ"] = PrepositionForm("ⲡⲁⲣⲁⲣⲁ", None, "PREP", "compared_to", Dialect.AKHMIMIC, "§170")

    def _init_adverbials(self):
        """Initialize adverbial expressions (§171-172)."""
        self.adverbials = {}

        # §171: Common adverbial expressions
        self.adverbials["ⲉⲃⲟⲗ"] = ("ⲉⲃⲟⲗ", "ADV", {"Meaning": "out/away"}, "§171")
        self.adverbials["ⲁⲃⲁⲗ"] = ("ⲁⲃⲁⲗ", "ADV", {"Meaning": "out/away"}, "§171")  # Akhmimic/Lycopolitan
        self.adverbials["ⲉⲃⲁⲗ"] = ("ⲉⲃⲁⲗ", "ADV", {"Meaning": "out/away"}, "§171")  # Fayyumic
        self.adverbials["ⲉϩⲟⲩⲛ"] = ("ⲉϩⲟⲩⲛ", "ADV", {"Meaning": "inside/in"}, "§171")
        self.adverbials["ⲁϩⲟⲩⲛ"] = ("ⲁϩⲟⲩⲛ", "ADV", {"Meaning": "inside/in"}, "§171")
        self.adverbials["ⲧⲉⲛⲟⲩ"] = ("ⲧⲉⲛⲟⲩ", "ADV", {"Meaning": "now"}, "§171")
        self.adverbials["ⲧⲛⲟⲩ"] = ("ⲧⲛⲟⲩ", "ADV", {"Meaning": "now"}, "§171")

    def identify_form(self, word: str) -> Optional[Tuple[str, str, Dict[str, str], str]]:
        """
        Identify if word is a pronoun or preposition.

        Returns: (lemma, pos, features, source_section) or None
        """
        # Check demonstratives
        if word in self.demonstratives:
            return self.demonstratives[word]

        # Check possessives
        if word in self.possessives:
            return self.possessives[word]

        # Check interrogatives
        if word in self.interrogatives:
            return self.interrogatives[word]

        # Check indefinites
        if word in self.indefinites:
            return self.indefinites[word]

        # Check prepositions
        if word in self.prepositions:
            prep = self.prepositions[word]
            return (prep.base_form, prep.pos, {"Meaning": prep.meaning}, prep.source_section)

        # Check adverbials
        if word in self.adverbials:
            return self.adverbials[word]

        return None


def create_pronouns_prepositions_analyzer_till(dialect: Dialect = Dialect.SAHIDIC) -> CopticPronounsPrepositionsTill:
    """
    Factory function to create a pronouns/prepositions analyzer for a specific dialect.

    Args:
        dialect: The Coptic dialect to use (default: Sahidic)

    Returns:
        CopticPronounsPrepositionsTill instance configured for the dialect
    """
    return CopticPronounsPrepositionsTill(dialect=dialect)


# Example usage
if __name__ == "__main__":
    # Test with Sahidic
    analyzer = create_pronouns_prepositions_analyzer_till()

    test_words = [
        "ⲡⲁⲓ",      # this (m.sg)
        "ⲛⲓⲙ",      # who?
        "ⲗⲁⲁⲩ",     # someone/something
        "ⲉⲧⲃⲉ",     # because of
        "ⲙⲛ",       # with/and
        "ⲉⲃⲟⲗ",     # out/away
        "ⲕⲉ",       # other/another
        "ⲛⲙⲙⲁ",     # with (pronominal form)
    ]

    print("Testing pronouns & prepositions analyzer (Till §122-172):\n")
    for word in test_words:
        result = analyzer.identify_form(word)
        if result:
            lemma, pos, feats, source = result
            feats_str = ", ".join(f"{k}={v}" for k, v in feats.items())
            print(f"{word:10s} → {lemma:10s} [{pos:6s}] ({feats_str}) [{source}]")
        else:
            print(f"{word:10s} → Not found")
