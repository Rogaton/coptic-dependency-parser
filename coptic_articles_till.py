#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coptic Article Analyzer - Based on Walter Till's Dialectal Grammar
====================================================================

Extracts article patterns from Till §62-73 (L'ARTICLE).

Articles are THE most fundamental morphology - appear in every noun phrase!

Coverage:
- §62: Definite article (weak forms)
- §63: Definite article (complete forms)
- §64: Bohairic definite forms
- §65: Bohairic genitive plural
- §66: Indefinite article

Source: Walter Till, "Koptische Dialektgrammatik" (French translation)
        Sections §62-73 (L'ARTICLE)

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

from typing import Optional, Tuple, Dict
from dataclasses import dataclass
from coptic_dialect_handler import Dialect

@dataclass
class ArticleForm:
    """Represents an article form"""
    form: str              # Surface form (e.g., "ⲡ", "ⲧⲏ")
    article_type: str      # "definite" or "indefinite"
    gender: Optional[str]  # "Masc", "Fem", or None
    number: str            # "Sing" or "Plur"
    form_type: str         # "weak" (ⲡ-), "complete" (ⲡⲉ-), "full" (ⲡⲏ)
    dialect: Dialect       # Dialect
    source_section: str    # Till section


class CopticArticlesTill:
    """
    Analyzes Coptic articles based on Till §62-73.

    Articles appear in EVERY noun phrase - critical for parsing!

    Definite articles distinguish:
    - Gender: Masculine vs Feminine (singular only)
    - Number: Singular vs Plural
    - Form: Weak (ⲡ-) vs Complete (ⲡⲉ-) vs Full (ⲡⲏ)

    Example:
        analyzer = CopticArticlesTill(dialect=Dialect.SAHIDIC)
        result = analyzer.identify("ⲡⲣⲱⲙⲉ")  # "ⲡ" = def.masc.sg
    """

    def __init__(self, dialect: Dialect = Dialect.SAHIDIC):
        """Initialize analyzer."""
        self.dialect = dialect
        self._init_articles()

    def _init_articles(self):
        """Initialize article forms from Till §62-66."""
        self.articles: Dict[str, ArticleForm] = {}

        # §62: DEFINITE ARTICLE - Weak forms (before consonants)
        # "forme faible" - shortened before most words

        # Sahidic/Lycopolitan (§62)
        sahidic_def = [
            ("ⲡ", "definite", "Masc", "Sing", "weak", Dialect.SAHIDIC, "§62"),
            ("ⲧ", "definite", "Fem", "Sing", "weak", Dialect.SAHIDIC, "§62"),
            ("ⲛ", "definite", None, "Plur", "weak", Dialect.SAHIDIC, "§62"),
        ]
        for form, art_type, gender, number, form_type, dialect, section in sahidic_def:
            self.articles[f"{form}_{dialect.value}"] = ArticleForm(
                form, art_type, gender, number, form_type, dialect, section
            )
            # Also register without dialect for default matching
            if form not in self.articles:
                self.articles[form] = ArticleForm(
                    form, art_type, gender, number, form_type, dialect, section
                )

        # Bohairic (§62, §64)
        bohairic_def = [
            ("ⲫ", "definite", "Masc", "Sing", "weak", Dialect.BOHAIRIC, "§62"),
            ("ⲑ", "definite", "Fem", "Sing", "weak", Dialect.BOHAIRIC, "§62"),
            ("ⲛⲓ", "definite", None, "Plur", "weak", Dialect.BOHAIRIC, "§64"),
        ]
        for form, art_type, gender, number, form_type, dialect, section in bohairic_def:
            self.articles[f"{form}_{dialect.value}"] = ArticleForm(
                form, art_type, gender, number, form_type, dialect, section
            )

        # §63: COMPLETE FORMS (before consonant clusters)
        # "forme plus complète" - ⲡⲉ-, ⲧⲉ-, ⲛⲉ-

        complete_forms = [
            # Sahidic
            ("ⲡⲉ", "definite", "Masc", "Sing", "complete", Dialect.SAHIDIC, "§63"),
            ("ⲧⲉ", "definite", "Fem", "Sing", "complete", Dialect.SAHIDIC, "§63"),
            ("ⲛⲉ", "definite", None, "Plur", "complete", Dialect.SAHIDIC, "§63"),
            # Lycopolitan
            ("ⲡⲉ", "definite", "Masc", "Sing", "complete", Dialect.LYCOPOLITAN, "§63"),
            ("ⲧⲉ", "definite", "Fem", "Sing", "complete", Dialect.LYCOPOLITAN, "§63"),
            ("ⲛⲉ", "definite", None, "Plur", "complete", Dialect.LYCOPOLITAN, "§63"),
            # Akhmimic
            ("ⲡⲉ", "definite", "Masc", "Sing", "complete", Dialect.AKHMIMIC, "§63"),
            ("ⲧⲉ", "definite", "Fem", "Sing", "complete", Dialect.AKHMIMIC, "§63"),
            ("ⲛⲉ", "definite", None, "Plur", "complete", Dialect.AKHMIMIC, "§63"),
        ]
        for form, art_type, gender, number, form_type, dialect, section in complete_forms:
            key = f"{form}_{dialect.value}"
            self.articles[key] = ArticleForm(
                form, art_type, gender, number, form_type, dialect, section
            )

        # §64: BOHAIRIC COMPLETE FORMS (very frequent!)
        bohairic_complete = [
            ("ⲡⲓ", "definite", "Masc", "Sing", "complete", Dialect.BOHAIRIC, "§64"),
            ("ⲧⲓ", "definite", "Fem", "Sing", "complete", Dialect.BOHAIRIC, "§64"),
            ("ⲛⲓ", "definite", None, "Plur", "complete", Dialect.BOHAIRIC, "§64"),
        ]
        for form, art_type, gender, number, form_type, dialect, section in bohairic_complete:
            key = f"{form}_{dialect.value}"
            self.articles[key] = ArticleForm(
                form, art_type, gender, number, form_type, dialect, section
            )

        # §62: FULL FORMS (with eta)
        # Used with demonstratives, possessives, etc.
        full_forms = [
            # Sahidic/Lycopolitan
            ("ⲡⲏ", "definite", "Masc", "Sing", "full", Dialect.SAHIDIC, "§62"),
            ("ⲧⲏ", "definite", "Fem", "Sing", "full", Dialect.SAHIDIC, "§62"),
            ("ⲛⲏ", "definite", None, "Plur", "full", Dialect.SAHIDIC, "§62"),
            # Fayyumic
            ("ⲡⲣⲉ", "definite", "Masc", "Sing", "full", Dialect.FAYYUMIC, "§62"),
            # Bohairic
            ("ⲫⲏ", "definite", "Masc", "Sing", "full", Dialect.BOHAIRIC, "§62"),
            ("ⲑⲏ", "definite", "Fem", "Sing", "full", Dialect.BOHAIRIC, "§62"),
        ]
        for form, art_type, gender, number, form_type, dialect, section in full_forms:
            key = f"{form}_{dialect.value}"
            self.articles[key] = ArticleForm(
                form, art_type, gender, number, form_type, dialect, section
            )

        # §65: BOHAIRIC GENITIVE PLURAL
        # Special form: ⲛⲉⲛ- (when followed by genitive complement)
        self.articles["ⲛⲉⲛ_B"] = ArticleForm(
            "ⲛⲉⲛ", "definite", None, "Plur", "genitive",
            Dialect.BOHAIRIC, "§65"
        )

        # §66: INDEFINITE ARTICLE
        # Singular only: ⲟⲩ-, ⲟⲩⲁ- forms

        indefinite_forms = [
            # Sahidic
            ("ⲟⲩ", "indefinite", None, "Sing", "weak", Dialect.SAHIDIC, "§66"),
            ("ⲟⲩⲁ", "indefinite", None, "Sing", "full", Dialect.SAHIDIC, "§66"),
            # Bohairic
            ("ⲟⲩ", "indefinite", None, "Sing", "weak", Dialect.BOHAIRIC, "§66"),
            ("ⲟⲩⲁ", "indefinite", None, "Sing", "full", Dialect.BOHAIRIC, "§66"),
            ("ⲟⲩⲏⲓ", "indefinite", None, "Sing", "full", Dialect.BOHAIRIC, "§66"),
            # Other dialects
            ("ⲟⲩ", "indefinite", None, "Sing", "weak", Dialect.LYCOPOLITAN, "§66"),
            ("ⲟⲩ", "indefinite", None, "Sing", "weak", Dialect.AKHMIMIC, "§66"),
            ("ⲟⲩ", "indefinite", None, "Sing", "weak", Dialect.FAYYUMIC, "§66"),
        ]
        for form, art_type, gender, number, form_type, dialect, section in indefinite_forms:
            key = f"{form}_{dialect.value}"
            self.articles[key] = ArticleForm(
                form, art_type, gender, number, form_type, dialect, section
            )
            # Register common forms globally
            if form in ["ⲟⲩ", "ⲟⲩⲁ"] and form not in self.articles:
                self.articles[form] = ArticleForm(
                    form, art_type, gender, number, form_type, dialect, section
                )

    def identify(self, word: str, dialect: Optional[Dialect] = None) -> Optional[ArticleForm]:
        """
        Identify if word starts with an article.

        Args:
            word: Full word (e.g., "ⲡⲣⲱⲙⲉ", "ⲟⲩⲣⲱⲙⲉ")
            dialect: Optional dialect hint

        Returns:
            ArticleForm if article found, else None

        Example:
            >>> analyzer.identify("ⲡⲣⲱⲙⲉ")
            ArticleForm(form="ⲡ", type="definite", gender="Masc", ...)
        """
        target_dialect = dialect or self.dialect

        # Try dialect-specific matches first (longest to shortest)
        candidates = ["ⲡⲉ", "ⲧⲉ", "ⲛⲉ", "ⲡⲓ", "ⲧⲓ", "ⲛⲓ", "ⲫⲏ", "ⲑⲏ", "ⲛⲏ",
                      "ⲡⲏ", "ⲧⲏ", "ⲟⲩⲁ", "ⲟⲩⲏⲓ", "ⲛⲉⲛ", "ⲡⲣⲉ",
                      "ⲡ", "ⲧ", "ⲛ", "ⲫ", "ⲑ", "ⲟⲩ"]

        for candidate in candidates:
            if word.startswith(candidate):
                # Try dialect-specific first
                key = f"{candidate}_{target_dialect.value}"
                if key in self.articles:
                    return self.articles[key]
                # Fall back to generic
                if candidate in self.articles:
                    return self.articles[candidate]

        return None

    def extract_article(self, word: str, dialect: Optional[Dialect] = None) -> Optional[Tuple[str, str]]:
        """
        Extract article and return (article, remainder).

        Args:
            word: Full word
            dialect: Optional dialect

        Returns:
            (article, remainder) or None

        Example:
            >>> analyzer.extract_article("ⲡⲣⲱⲙⲉ")
            ("ⲡ", "ⲣⲱⲙⲉ")
        """
        result = self.identify(word, dialect)
        if result:
            return (result.form, word[len(result.form):])
        return None

    def is_definite(self, word: str, dialect: Optional[Dialect] = None) -> bool:
        """Check if word starts with definite article."""
        result = self.identify(word, dialect)
        return result is not None and result.article_type == "definite"

    def is_indefinite(self, word: str, dialect: Optional[Dialect] = None) -> bool:
        """Check if word starts with indefinite article."""
        result = self.identify(word, dialect)
        return result is not None and result.article_type == "indefinite"


def create_articles_analyzer_till(dialect: Dialect = Dialect.SAHIDIC) -> CopticArticlesTill:
    """Factory function to create articles analyzer."""
    return CopticArticlesTill(dialect=dialect)


if __name__ == "__main__":
    # Quick test
    analyzer = create_articles_analyzer_till(dialect=Dialect.SAHIDIC)

    print("Testing article recognition:")
    test_words = ["ⲡⲣⲱⲙⲉ", "ⲧⲥϩⲓⲙⲉ", "ⲛⲣⲱⲙⲉ", "ⲟⲩⲣⲱⲙⲉ", "ⲡⲉⲭⲥ"]

    for word in test_words:
        result = analyzer.identify(word)
        if result:
            gender_info = f", Gender={result.gender}" if result.gender else ""
            print(f"✓ {word}: {result.form} [{result.article_type}, {result.number}{gender_info}, {result.form_type}]")
        else:
            print(f"✗ {word}: No article")
