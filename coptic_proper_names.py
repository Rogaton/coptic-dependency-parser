#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coptic Proper Names - Common names to filter from grammatical analysis
========================================================================

Reduces false positives by excluding proper names from pattern matching.

Common false positives:
- Στέφανος (ⲥⲧⲉⲫⲁⲛⲟⲥ) → contains ⲁⲛ (negation)
- Ἰωάννης (ⲓⲱⲁⲛⲛⲏⲥ) → contains ⲁⲛ (negation)
- Εὐαγγέλιον (ⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ) → often with article ⲙⲡ- → ⲙⲡⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

from typing import Set

# Biblical and Christian names (Greek origin)
GREEK_NAMES = {
    # New Testament figures
    "ⲓⲏⲥⲟⲩⲥ",      # Jesus
    "ⲭⲣⲓⲥⲧⲟⲥ",      # Christ
    "ⲓⲱϩⲁⲛⲛⲏⲥ",    # John
    "ⲓⲱⲁⲛⲛⲏⲥ",     # John (variant)
    "ⲡⲉⲧⲣⲟⲥ",      # Peter
    "ⲡⲁⲩⲗⲟⲥ",      # Paul
    "ⲙⲁⲣⲓⲁ",       # Mary
    "ⲙⲁⲣⲓⲁⲙ",      # Mariam
    "ⲙⲁⲣⲑⲁ",       # Martha
    "ⲗⲁⲍⲁⲣⲟⲥ",     # Lazarus
    "ⲙⲁⲧⲑⲁⲓⲟⲥ",    # Matthew
    "ⲙⲁⲣⲕⲟⲥ",      # Mark
    "ⲗⲟⲩⲕⲁⲥ",      # Luke
    "ⲑⲱⲙⲁⲥ",       # Thomas
    "ⲁⲛⲇⲣⲉⲁⲥ",     # Andrew
    "ⲫⲓⲗⲓⲡⲡⲟⲥ",    # Philip
    "ⲥⲓⲙⲱⲛ",       # Simon
    "ⲓⲁⲕⲱⲃⲟⲥ",     # James

    # Saints and Church figures
    "ⲥⲧⲉⲫⲁⲛⲟⲥ",    # Stephen (contains ⲁⲛ!)
    "ⲁⲛⲧⲱⲛⲓⲟⲥ",    # Anthony (contains ⲁⲛ!)
    "ⲁⲑⲁⲛⲁⲥⲓⲟⲥ",   # Athanasius (contains ⲁⲛ!)
    "ⲃⲁⲥⲓⲗⲓⲟⲥ",    # Basil
    "ⲅⲣⲏⲅⲟⲣⲓⲟⲥ",   # Gregory
    "ⲉⲩⲥⲧⲁⲑⲓⲟⲥ",   # Eustathius
    "ⲑⲉⲟⲇⲱⲣⲟⲥ",    # Theodore
    "ⲕⲩⲣⲓⲗⲗⲟⲥ",    # Cyril
    "ⲛⲓⲕⲟⲗⲁⲟⲥ",    # Nicholas
    "ⲡⲁⲭⲱⲙⲓⲟⲥ",    # Pachomius
    "ⲙⲁⲕⲁⲣⲓⲟⲥ",    # Macarius
    "ⲙⲁⲝⲓⲙⲟⲥ",     # Maximus
    "ⲉⲡⲓⲫⲁⲛⲓⲟⲥ",   # Epiphanius
    "ⲇⲓⲟⲥⲕⲟⲣⲟⲥ",   # Dioscorus
    "ⲥⲉⲣⲁⲡⲓⲱⲛ",    # Serapion

    # Old Testament names
    "ⲁⲃⲣⲁϩⲁⲙ",     # Abraham
    "ⲙⲱⲩⲥⲏⲥ",      # Moses
    "ⲇⲁⲩⲉⲓⲇ",       # David
    "ⲥⲁⲗⲟⲙⲱⲛ",     # Solomon
    "ⲏⲥⲁⲓⲁⲥ",      # Isaiah (ⲏⲥⲁⲓⲁⲥ)
    "ⲓⲉⲣⲉⲙⲓⲁⲥ",    # Jeremiah
    "ⲇⲁⲛⲓⲏⲗ",       # Daniel
    "ⲉⲗⲓⲁⲥ",        # Elias/Elijah
    "ⲏⲗⲓⲁⲥ",        # Elias (variant) - ϩⲏⲗⲓⲁⲥ
    "ϩⲏⲗⲓⲁⲥ",       # Helias

    # Greco-Roman names
    "ⲁⲗⲉⲝⲁⲛⲇⲣⲟⲥ",  # Alexander
    "ⲕⲗⲏⲙⲏⲥ",      # Clement
    "ⲡⲓⲗⲁⲧⲟⲥ",     # Pilate
    "ⲕⲁⲓⲥⲁⲣ",      # Caesar
    "ⲇⲓⲟⲕⲗⲏⲧⲓⲁⲛⲟⲥ", # Diocletian (contains ⲁⲛ!)
}

# Egyptian names
EGYPTIAN_NAMES = {
    "ϣⲉⲛⲟⲩⲧⲉ",     # Shenoute
    "ⲡϣⲟⲓ",         # Pshoi
    "ⲡⲁϩⲱⲙ",        # Pahom/Pachomius (Egyptian form)
    "ⲡⲓⲥⲉⲛⲧⲓⲟⲥ",   # Pisentius
    "ⲁⲡⲁ",          # Apa (title, but often part of names)
    "ⲁⲃⲃⲁ",         # Abba (title)
}

# Common ecclesiastical/theological terms (not names, but cause false positives)
ECCLESIASTICAL_TERMS = {
    "ⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ",   # Gospel (contains ⲁⲛ when with article: ⲙⲡⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ)
    "ⲁⲅⲅⲉⲗⲟⲥ",      # Angel
    "ⲁⲡⲟⲥⲧⲟⲗⲟⲥ",    # Apostle
    "ⲇⲓⲁⲕⲟⲛⲟⲥ",     # Deacon (contains ⲁⲛ!)
    "ⲙⲁⲣⲧⲩⲣⲟⲥ",     # Martyr
    "ⲡⲣⲟⲫⲏⲧⲏⲥ",    # Prophet
    "ⲉⲡⲓⲥⲕⲟⲡⲟⲥ",   # Bishop
    "ⲡⲓⲥⲕⲟⲡⲟⲥ",    # Bishop (without ⲉ-)
    "ⲡⲣⲉⲥⲃⲩⲧⲉⲣⲟⲥ", # Presbyter
    "ⲙⲟⲛⲁⲭⲟⲥ",      # Monk (contains ⲁⲛ!)
    "ϩⲁⲅⲓⲟⲥ",       # Holy/Saint
    "ⲥⲁⲧⲁⲛⲁⲥ",      # Satan (contains ⲁⲛ!)
    "ⲥⲁⲧⲁⲛ",        # Satan (variant, contains ⲁⲛ!)
}

# Combine all
ALL_PROPER_NAMES = GREEK_NAMES | EGYPTIAN_NAMES | ECCLESIASTICAL_TERMS


def is_proper_name(word: str) -> bool:
    """
    Check if word is a known proper name or ecclesiastical term.

    Args:
        word: Coptic word to check

    Returns:
        True if word is a proper name/term, False otherwise
    """
    return word.lower() in ALL_PROPER_NAMES


def get_proper_name_filter() -> Set[str]:
    """
    Get the set of all proper names for filtering.

    Returns:
        Set of proper names in lowercase
    """
    return ALL_PROPER_NAMES


if __name__ == "__main__":
    # Test false positive cases
    test_words = ["ⲥⲧⲉⲫⲁⲛⲟⲥ", "ⲁⲛⲧⲱⲛⲓⲟⲥ", "ⲁⲑⲁⲛⲁⲥⲓⲟⲥ", "ⲙⲡⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ", "ⲉⲩⲁⲅⲅⲉⲗⲓⲟⲛ"]

    for word in test_words:
        if is_proper_name(word):
            print(f"✓ {word} → filtered (proper name)")
        elif "ⲁⲛ" in word:
            # Check if we're preventing false positive
            base = word.replace("ⲙⲡⲉ", "").replace("ⲙ", "")
            if is_proper_name(base):
                print(f"✓ {word} → filtered (base: {base})")
            else:
                print(f"✗ {word} → would be false positive (contains ⲁⲛ)")
        else:
            print(f"  {word} → not filtered")
