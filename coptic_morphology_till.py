#!/usr/bin/env python3
"""
Coptic Morphology Analyzer - Based on Walter Till's Dialectal Grammar
======================================================================

Implements Till's comprehensive dialectal patterns for Coptic morphology.

Handles segmentation of fused proclitic forms into subtokens across all
seven Coptic dialects (S, B, A, L, F, M, P).

Key function: Segment words like ⲁϥⲃⲱⲕ into:
  - ⲁ (APST, past auxiliary) - Till §261
  - ϥ (PPERS, subject pronoun) - Till §113-121
  - ⲃⲱⲕ (V, main verb)

Source: Walter Till, "Koptische Dialektgrammatik" (French translation)
        Sections §245-268 (Prefixal Conjugation)

Author: André Linden (2025)
License: CC BY-NC-SA 4.0
"""

from typing import List, Tuple, Optional, Dict
from dataclasses import dataclass
from coptic_dialect_handler import Dialect, DialectHandler, DialectalForm


@dataclass
class Segment:
    """Represents one morpheme segment"""
    form: str      # Surface form (e.g., "ⲁ")
    lemma: str     # Lemma (e.g., "ⲁ")
    pos: str       # Scriptorium POS tag (e.g., "APST")
    feats: Dict[str, str]  # Morphological features
    dialect: Optional[Dialect] = None  # Specific dialect variant
    source_section: Optional[str] = None  # Till section reference


class CopticMorphologyAnalyzerTill:
    """
    Analyzes Coptic morphology based on Till's dialectal grammar.

    Supports all seven Coptic dialects: S, B, A, L, F, M, P

    Example:
        analyzer = CopticMorphologyAnalyzerTill(dialect=Dialect.SAHIDIC)
        segments = analyzer.segment_word("ⲁϥⲃⲱⲕ")
        # Returns: [Segment("ⲁ", "ⲁ", "APST", {}, Dialect.SAHIDIC, "§261"),
        #           Segment("ϥ", "ⲛⲧⲟϥ", "PPERS", {...}, source_section="§117"),
        #           Segment("ⲃⲱⲕ", "ⲃⲱⲕ", "V", {...})]
    """

    def __init__(self, dialect: Dialect = Dialect.SAHIDIC, prolog_engine=None):
        """
        Initialize analyzer.

        Args:
            dialect: Default dialect for parsing
            prolog_engine: Optional CopticPrologEngine for feature lookup
        """
        self.dialect = dialect
        self.prolog = prolog_engine
        self.dialect_handler = DialectHandler(default_dialect=dialect)
        self._init_patterns()

    def _init_patterns(self):
        """Initialize segmentation patterns from Till's grammar"""

        # §113-121: Personal pronouns (subject suffixes)
        # Till provides these as suffixes attached to conjugation bases
        self.pronouns = {
            "ⲓ": ("ⲁⲛⲟⲕ", "PPERS", {"Person": "1", "Number": "Sing"}),
            "ⲕ": ("ⲛⲧⲟⲕ", "PPERS", {"Person": "2", "Number": "Sing", "Gender": "Masc"}),
            "ⲧⲉ": ("ⲛⲧⲟ", "PPERS", {"Person": "2", "Number": "Sing", "Gender": "Fem"}),
            "ϥ": ("ⲛⲧⲟϥ", "PPERS", {"Person": "3", "Number": "Sing", "Gender": "Masc"}),
            "ⲥ": ("ⲛⲧⲟⲥ", "PPERS", {"Person": "3", "Number": "Sing", "Gender": "Fem"}),
            "ⲛ": ("ⲁⲛⲟⲛ", "PPERS", {"Person": "1", "Number": "Plur"}),
            "ⲧⲛ": ("ⲛⲧⲱⲧⲛ", "PPERS", {"Person": "2", "Number": "Plur"}),
            "ⲩ": ("ⲛⲧⲟⲟⲩ", "PPERS", {"Person": "3", "Number": "Plur"}),
        }

        # §248: Présent I (Present I - adverbial proposition, 180-182)
        # Durative present with infinitive
        self._register_prefix_pattern("present_i", {
            Dialect.SAHIDIC: "ⲉⲣⲉ",
            Dialect.LYCOPOLITAN: "ⲉⲣⲉ",
            Dialect.BOHAIRIC: "ⲁⲣⲉ",
            Dialect.AKHMIMIC: "ⲁⲣⲉ",  # Also ⲁ(ⲣⲉ)
            Dialect.FAYYUMIC: "ⲁⲗⲗⲉ",
        }, "APRES", "§248")

        # §249: Présent Consuétudinal I (Habitual present)
        # Expresses habitual action
        self._register_prefix_pattern("habitual_present", {
            Dialect.SAHIDIC: "ϣⲁⲣⲉ",
            Dialect.BOHAIRIC: "ϣⲁⲣⲉ",
            Dialect.LYCOPOLITAN: "ϣⲁⲣⲉ",
            Dialect.AKHMIMIC: "ⲥⲁⲣⲉ",
            Dialect.FAYYUMIC: "ϣⲁⲗⲗⲉ",
        }, "AHABPRES", "§249")

        # §250: Présent cons. I négatif (Negative habitual present)
        self._register_prefix_pattern("habitual_present_neg", {
            Dialect.SAHIDIC: "ⲙⲉⲣⲉ",  # Also SF: ⲙⲉ-
            Dialect.AKHMIMIC: "ⲙⲁⲣⲉ",
            Dialect.LYCOPOLITAN: "ⲙⲁⲣⲉ",
            Dialect.BOHAIRIC: "ⲙⲡⲁⲣⲉ",
            Dialect.FAYYUMIC: "ⲙⲉⲗⲉ",
        }, "ANEGHABPRES", "§250")

        # §251: Présent consuétudinal II (Habitual present II)
        # Like Présent cons. I with prefixes §248
        self._register_prefix_pattern("habitual_present_ii", {
            Dialect.SAHIDIC: "ⲉ",
            Dialect.BOHAIRIC: "ⲉ",
            Dialect.LYCOPOLITAN: "ⲉ",
            Dialect.AKHMIMIC: "ⲁ",
            Dialect.FAYYUMIC: "ⲛ",
        }, "AHABPRES2", "§251")

        # §252: Futur I (Future I - adverbial proposition)
        # Present II (§248) with future prefix ⲛⲁ
        self._register_prefix_pattern("future_i", {
            Dialect.SAHIDIC: "ⲉⲣⲉⲛⲁ",  # ⲉⲣⲉ-ⲛⲁ
            Dialect.LYCOPOLITAN: "ⲁⲣⲉⲛⲁ",  # Usually ⲁ instead of ⲛⲁ
            Dialect.BOHAIRIC: "ⲁⲣⲉⲛⲁ",
            Dialect.AKHMIMIC: "ⲁⲣⲉⲛⲁ",
            Dialect.FAYYUMIC: "ⲁⲗⲗⲉⲛⲉ",  # F: ⲛⲉ instead of ⲛⲁ
        }, "AFUT", "§252")

        # §253: Futur III (Future III - prediction, desire, order)
        self._register_prefix_pattern("future_iii", {
            Dialect.SAHIDIC: "ⲉⲣⲉ",
            Dialect.BOHAIRIC: "ⲉⲣⲉ",
            Dialect.AKHMIMIC: "ⲁⲁ",  # A: ⲁ-ⲁ-
            Dialect.LYCOPOLITAN: "ⲉⲣⲉⲁ",
            Dialect.FAYYUMIC: "ⲉⲗⲉ",
        }, "AFUT3", "§253")

        # §254: Futur III négatif
        self._register_prefix_pattern("future_iii_neg", {
            Dialect.SAHIDIC: "ⲛⲛⲉ",
            Dialect.BOHAIRIC: "ⲛⲛⲉ",
            Dialect.FAYYUMIC: "ⲛⲛⲉ",
            Dialect.AKHMIMIC: "ⲛⲉ",
            Dialect.LYCOPOLITAN: "ⲛⲉ",
        }, "ANEGFUT3", "§254")

        # §255: Optatif (Optative - desire/wish: "faire")
        self._register_prefix_pattern("optative", {
            Dialect.SAHIDIC: "ⲙⲁⲣⲉ",
            Dialect.BOHAIRIC: "ⲙⲁⲣⲉ",
            Dialect.AKHMIMIC: "ⲙⲁⲣⲉ",
            Dialect.LYCOPOLITAN: "ⲙⲁⲣⲉ",
            Dialect.FAYYUMIC: "ⲙⲁⲗⲉ",
        }, "AOPT", "§255")

        # §258: Final (Conjunctive future - "et ... fera")
        # Development of "afin que" sense
        self._register_prefix_pattern("final", {
            Dialect.SAHIDIC: "ⲧⲁⲣⲉ",
            Dialect.AKHMIMIC: "ⲧⲁⲣⲉ",
            Dialect.LYCOPOLITAN: "ⲧⲁⲣⲉ",
            Dialect.BOHAIRIC: "ⲧⲁⲣⲉ",  # Also in B
            Dialect.FAYYUMIC: "ⲧⲁⲗⲉ",
        }, "AFINAL", "§258")

        # §260: Jusqu'à (Until - "fait, respect. faisait")
        self._register_prefix_pattern("until", {
            Dialect.SAHIDIC: "ϣⲁⲛⲧⲉ",
            Dialect.LYCOPOLITAN: "ϣⲁⲛⲧⲉ",
            Dialect.FAYYUMIC: "ϣⲁⲛⲧⲉ",
            Dialect.BOHAIRIC: "ϣⲁⲧⲉ",
            Dialect.AKHMIMIC: "ϣⲁⲧⲉ",  # BA form
        }, "AUNTIL", "§260")

        # §261: Parfait I (Perfect I - Preterit, past tense)
        # Preterit ⲁ-; forms ⲁⲣⲉ (SB), ⲁⲣ- (A), ⲁⲗ (F)
        self._register_prefix_pattern("perfect_i", {
            Dialect.SAHIDIC: "ⲁⲣⲉ",
            Dialect.BOHAIRIC: "ⲁⲣⲉ",
            Dialect.AKHMIMIC: "ⲁⲣ",
            Dialect.FAYYUMIC: "ⲁⲗ",
        }, "APERF", "§261")

        # Simple preterit ⲁ (common to most dialects)
        self._register_prefix_pattern("perfect_i_simple", {
            Dialect.SAHIDIC: "ⲁ",
            Dialect.BOHAIRIC: "ⲁ",
            Dialect.AKHMIMIC: "ⲁ",
            Dialect.LYCOPOLITAN: "ⲁ",
            Dialect.FAYYUMIC: "ⲁ",
        }, "APST", "§261")

        # §263: Parfait I négatif (Negative perfect)
        self._register_prefix_pattern("perfect_i_neg", {
            Dialect.SAHIDIC: "ⲙⲡⲉ",
            Dialect.BOHAIRIC: "ⲙⲡⲉ",
            Dialect.AKHMIMIC: "ⲙⲡⲉ",
            Dialect.LYCOPOLITAN: "ⲙⲡⲉ",
            Dialect.FAYYUMIC: "ⲙⲡⲉ",
        }, "ANEGPST", "§263")

        # §264: Parfait II (Perfect II - temporal sense)
        # More frequent in BF
        self._register_prefix_pattern("perfect_ii", {
            Dialect.SAHIDIC: "ⲛⲧⲁ",
            Dialect.LYCOPOLITAN: "ⲛⲧⲁ",
            Dialect.FAYYUMIC: "ⲉⲧⲉⲁ",  # Also ⲁⲁ-, ⲉⲧⲁ-
            Dialect.BOHAIRIC: "ⲉⲧⲁ",
            Dialect.AKHMIMIC: "ⲛⲁ",
        }, "APERF2", "§264")

        # §265: Temporel (Temporal - "comme" or "après que")
        # Negative §315
        self._register_prefix_pattern("temporal", {
            Dialect.SAHIDIC: "ⲛⲧⲉⲣⲉ",
            Dialect.AKHMIMIC: "ⲛⲧⲁⲣⲉ",  # Also (ⲛ)ⲧⲁ,ⲣⲉ-
            Dialect.LYCOPOLITAN: "ⲛⲧⲁⲣⲉ",
            Dialect.FAYYUMIC: "ⲛⲧⲉⲗⲉ",
        }, "APREC", "§265")

        # §266: N'avai(en)t pas encore (Not yet)
        self._register_prefix_pattern("not_yet", {
            Dialect.SAHIDIC: "ⲙⲡⲁⲧⲉ",
            Dialect.LYCOPOLITAN: "ⲙⲡⲁⲧⲉ",
            Dialect.BOHAIRIC: "ⲙⲡⲁⲧⲉ",
        }, "ANEGNOTYET", "§266")

        # §267: Conjonctif (Conjunctive)
        # Often replaces subjunctive; follows conjunctions
        self._register_prefix_pattern("conjunctive", {
            Dialect.SAHIDIC: "ⲛⲧⲉ",
            Dialect.BOHAIRIC: "ⲛⲧⲉ",
            Dialect.LYCOPOLITAN: "ⲛⲧⲉ",
            Dialect.FAYYUMIC: "ⲛⲧⲉ",
            Dialect.AKHMIMIC: "ⲧⲉ",
        }, "ACONJ", "§267")

        # With suffix forms (§267: ⲛⲧⲁ, B: ⲛⲧⲁ, A: ⲧⲁ)
        self._register_prefix_pattern("conjunctive_suffix", {
            Dialect.SAHIDIC: "ⲛⲧⲁ",
            Dialect.LYCOPOLITAN: "ⲛⲧⲁ",
            Dialect.FAYYUMIC: "ⲛⲧⲁ",
            Dialect.BOHAIRIC: "ⲛⲧⲁ",
            Dialect.AKHMIMIC: "ⲧⲁ",
        }, "ACONJSUF", "§267")

        # §269-270: LE PASSÉ (Passive/Imperfect)
        # Particle ⲛⲉ conjugated (replaces adverbial past)
        self._register_prefix_pattern("imperfect", {
            Dialect.SAHIDIC: "ⲛⲉⲣⲉ",
            Dialect.LYCOPOLITAN: "ⲛⲉⲣⲉ",
            Dialect.BOHAIRIC: "ⲛⲁⲣⲉ",
            Dialect.AKHMIMIC: "ⲛⲁⲣⲉ",
            Dialect.FAYYUMIC: "ⲛⲛⲁⲗⲗⲉ",  # Also (ⲛ)ⲛⲁⲗⲗⲉ
        }, "AIMP", "§270")

        # §272-277: La proposition circonstancielle (Circumstantial)
        # §272: Basic circumstantial converter ⲉ- (temporal/modal)
        # Replaces subordinate conjunctions (comme, tandis que, si, etc.)
        self._register_prefix_pattern("circumstantial", {
            Dialect.SAHIDIC: "ⲉ",
            Dialect.BOHAIRIC: "ⲉ",
            Dialect.LYCOPOLITAN: "ⲉ",
            Dialect.AKHMIMIC: "ⲉ",
            Dialect.FAYYUMIC: "ⲉ",
        }, "CCIRC", "§272")

        # §274: Conjugated circumstantial (durée/simultanéité)
        # Replaces PC of PA affirmative. Very frequent in texts!
        self._register_prefix_pattern("circumstantial_durative", {
            Dialect.SAHIDIC: "ⲉⲣⲉ",
            Dialect.BOHAIRIC: "ⲉⲣⲉ",
            Dialect.LYCOPOLITAN: "ⲉⲣⲉ",
            Dialect.AKHMIMIC: "ⲉⲣⲉ",  # Also ⲉ- in AL
            Dialect.FAYYUMIC: "ⲉⲗⲉ",  # Also ⲉ-
        }, "ACIRCPRES", "§274")

        # §275: Circumstantial future (postériorité)
        # Note: Combines ⲉ- (circumstantial) + pronoun + ⲛⲁ/ⲛⲉ (future)
        # Examples: ⲉⲩⲛⲁⲥⲃⲧⲉ, ⲉⲕⲛⲁⲧⲱⲃϩ - segments as ⲉ + pronoun + ⲛⲁ + verb
        # §276-277: Periphrastic (ⲱⲱⲡⲉ) and inchoative (ⲉⲓ) are syntactic patterns

        # Object pronoun patterns (prepositional objects)
        self.object_pronouns = {
            "ⲙⲙⲟ": ("ⲛ", "PREP"),  # Accusative
            "ⲉⲣⲟ": ("ⲉ", "PREP"),  # To/toward
            "ⲛⲁ": ("ⲛⲁ", "PREP"),   # To/for
            "ϩⲁⲣⲟ": ("ϩⲁ", "PREP"), # Under
        }

        # §219-230: SUFFIXAL CONJUGATION (Quality/Stative verbs)
        # These verbs conjugate with subject suffix directly (no infinitive)
        self.quality_verbs = {
            # §220: Various meanings
            "ⲙⲉⲩⲉ": ("ⲙⲉⲩⲉ", "VSTAT", {"Meaning": "ne sais pas"}),  # S
            "ⲙⲉϩⲁ": ("ⲙⲉϩⲁ", "VSTAT", {"Meaning": "peut-être"}),   # A

            # §221: Quality verbs (big, good, beautiful, etc.)
            "ⲛⲁⲁ": ("ⲛⲁⲁ", "VSTAT", {"Meaning": "grand"}),  # SB
            "ⲛⲉⲉ": ("ⲛⲁⲁ", "VSTAT", {"Meaning": "grand"}),  # L
            "ⲛⲁⲛⲟⲩ": ("ⲛⲁⲛⲟⲩ", "VSTAT", {"Meaning": "bon"}),  # SAL F
            "ⲛⲁⲛⲉ": ("ⲛⲁⲛⲟⲩ", "VSTAT", {"Meaning": "bon"}),  # B
            "ⲛⲉⲥⲱ": ("ⲛⲉⲥⲱ", "VSTAT", {"Meaning": "beau"}),  # S
            "ⲛⲉⲥⲃⲱⲱ": ("ⲛⲉⲥⲱ", "VSTAT", {"Meaning": "beau"}),  # S
            "ⲛⲁϣⲉ": ("ⲛⲁϣⲉ", "VSTAT", {"Meaning": "nombreux"}),  # B also
            "ⲛⲉⲃⲱ": ("ⲛⲉⲃⲱ", "VSTAT", {"Meaning": "laid"}),  # S
            "ⲛⲁⲛⲟⲩⲥ": ("ⲛⲁⲛⲟⲩⲥ", "VSTAT", {"Meaning": "bon"}),  # A

            # §222: "say" (past quality)
            "ⲡⲉⲭⲉ": ("ⲡⲉⲭⲉ", "VSTAT", {"Meaning": "a dit"}),  # SBF
            "ⲡⲉⲭⲁ": ("ⲡⲉⲭⲉ", "VSTAT", {"Meaning": "a dit"}),  # F
            "ⲡⲁⲭⲉ": ("ⲡⲉⲭⲉ", "VSTAT", {"Meaning": "a dit"}),  # AL

            # §223: "different"
            "ⲟⲩⲱⲧ": ("ⲟⲩⲱⲧ", "VSTAT", {"Meaning": "différent"}),  # SAL
            "ⲟⲩⲉⲧ": ("ⲟⲩⲱⲧ", "VSTAT", {"Meaning": "différent"}),  # SB
            "ⲟⲩⲟⲧ": ("ⲟⲩⲱⲧ", "VSTAT", {"Meaning": "différent"}),  # B
            "ⲟⲩⲁⲧ": ("ⲟⲩⲱⲧ", "VSTAT", {"Meaning": "différent"}),  # F

            # §224: "want"
            "ⲍⲛⲉ": ("ⲍⲛⲉ", "VSTAT", {"Meaning": "veut"}),  # SB
            "ⲍⲛⲁ": ("ⲍⲛⲉ", "VSTAT", {"Meaning": "veut"}),  # AL
            "ⲍⲛⲏ": ("ⲍⲛⲉ", "VSTAT", {"Meaning": "veut"}),  # F

            # §225: "exists" (il est, il y a) - IMPORTANT!
            "ⲟⲩⲛ": ("ⲟⲩⲛ", "VSTAT", {"Meaning": "il y a"}),  # SAL
            "ⲟⲩⲟⲛ": ("ⲟⲩⲛ", "VSTAT", {"Meaning": "il y a"}),  # B
            "ⲟⲩⲁⲛ": ("ⲟⲩⲛ", "VSTAT", {"Meaning": "il y a"}),  # F
        }

        # §231-244: IMPERATIVE FORMS
        # Special imperative forms (not simple infinitives)
        self.imperative_forms = {
            # §232: "renounce"
            "ⲁⲗⲟⲕ": ("ⲁⲗⲟⲕ", "VIMP", "§232"),  # S, L (m.sg.)
            "ⲉⲗⲁⲕ": ("ⲁⲗⲟⲕ", "VIMP", "§232"),  # L (m.sg.)
            "ⲁⲗⲟ": ("ⲁⲗⲟⲕ", "VIMP", "§232"),   # S (f.sg.)
            "ⲁⲗⲱⲧⲛ": ("ⲁⲗⲟⲕ", "VIMP", "§232"), # SL (pl.)

            # §233: "come"
            "ⲁⲙⲟⲩ": ("ⲁⲙⲟⲩ", "VIMP", "§233"),  # (m.sg.)
            "ⲁⲙⲏ": ("ⲁⲙⲟⲩ", "VIMP", "§233"),   # A (m.sg.)
            "ⲁⲙⲓ": ("ⲁⲙⲟⲩ", "VIMP", "§233"),   # (f.sg.)
            "ⲁⲙⲏⲉⲓⲧⲁⲛ": ("ⲁⲙⲟⲩ", "VIMP", "§233"),  # S
            "ⲁⲙⲱⲓⲛⲓ": ("ⲁⲙⲟⲩ", "VIMP", "§233"),   # A
            "ⲁⲙⲏⲉⲓⲛⲉ": ("ⲁⲙⲟⲩ", "VIMP", "§233"),  # A, L

            # §234: "bring"
            "ⲁⲛⲉⲓⲛⲉ": ("ⲁⲛⲓ", "VIMP", "§234"),  # S, B
            "ⲁⲛⲓⲟⲩⲓ": ("ⲁⲛⲓ", "VIMP", "§234"),  # B
            "ⲁⲛⲓ": ("ⲁⲛⲓ", "VIMP", "§234"),     # SB LF
            "ⲁⲛⲓⲧ": ("ⲁⲛⲓ", "VIMP", "§234"),    # BF

            # §235: "see"
            "ⲁⲛⲁⲩ": ("ⲁⲛⲁⲩ", "VIMP", "§235"),  # SB
            "ⲁⲛⲉⲩ": ("ⲁⲛⲁⲩ", "VIMP", "§235"),  # LF

            # §236: "do" / "make"
            "ⲁⲣⲓⲣⲉ": ("ⲁⲣⲓ", "VIMP", "§236"),  # S, B
            "ⲁⲣⲓⲟⲩⲓ": ("ⲁⲣⲓ", "VIMP", "§236"), # B
            "ⲁⲣⲓ": ("ⲁⲣⲓ", "VIMP", "§236"),    # SBAL
            "ⲉⲣⲓ": ("ⲁⲣⲓ", "VIMP", "§236"),    # AL, F
            "ⲁⲁⲓ": ("ⲁⲣⲓ", "VIMP", "§236"),    # F, SAL
            "ⲁⲣⲓⲧ": ("ⲁⲣⲓ", "VIMP", "§236"),   # B
            "ⲁⲗⲓⲧ": ("ⲁⲣⲓ", "VIMP", "§236"),   # F

            # §237: "give" / "come"
            "ⲁⲩⲉⲓⲥ": ("ⲁⲩⲉⲓⲥ", "VIMP", "§237"),  # SLF
            "ⲁⲩⲓⲥ": ("ⲁⲩⲉⲓⲥ", "VIMP", "§237"),   # B
            "ⲁⲩⲉⲓ": ("ⲁⲩⲉⲓⲥ", "VIMP", "§237"),   # SAL
            "ⲁⲩ": ("ⲁⲩⲉⲓⲥ", "VIMP", "§237"),     # S

            # §238: "open"
            "ⲁⲟⲩⲱⲛ": ("ⲁⲟⲩⲱⲛ", "VIMP", "§238"),  # SBF
            "ⲁⲩⲉⲛ": ("ⲁⲟⲩⲱⲛ", "VIMP", "§238"),   # L
            "ⲉⲟⲩⲉⲛ": ("ⲁⲟⲩⲱⲛ", "VIMP", "§238"),  # A

            # §239: "say"
            "ⲁⲭⲓ": ("ⲁⲭⲓ", "VIMP", "§239"),   # S, BF
            "ⲁⲭⲉ": ("ⲁⲭⲓ", "VIMP", "§239"),   # BF, SAL F
            "ⲉⲭⲓ": ("ⲁⲭⲓ", "VIMP", "§239"),   # AL
            "ⲁⲭⲟ": ("ⲁⲭⲓ", "VIMP", "§239"),   # B

            # §240: "give"
            "ⲙⲁ": ("ⲙⲁ", "VIMP", "§240"),     # SAL, B
            "ⲙⲟⲓ": ("ⲙⲁ", "VIMP", "§240"),    # B
            "ⲙⲁⲓ": ("ⲙⲁ", "VIMP", "§240"),    # F
            "ⲙⲏⲓ": ("ⲙⲁ", "VIMP", "§240"),    # B, F
        }

        # Store all registered patterns for lookup
        self.conjugation_bases: Dict[str, Tuple[str, str]] = {}
        self._build_conjugation_index()

    def _register_prefix_pattern(
        self,
        pattern_id: str,
        dialect_forms: Dict[Dialect, str],
        pos_tag: str,
        source_section: str
    ):
        """Register a prefixal conjugation pattern with dialectal variations"""
        # Use Sahidic as base form (standard)
        base_form = dialect_forms.get(Dialect.SAHIDIC, list(dialect_forms.values())[0])

        self.dialect_handler.register_form(
            base_form=base_form,
            dialect_forms=dialect_forms,
            pos=pos_tag,
            features={},
            source_section=source_section
        )

    def _build_conjugation_index(self):
        """Build quick lookup index for conjugation bases"""
        # Get all forms from dialect handler
        for base_form, df_list in self.dialect_handler.forms.items():
            for df in df_list:
                # Index all variant forms
                for form in df.get_all_forms():
                    if form not in self.conjugation_bases:
                        self.conjugation_bases[form] = (df.pos, df.base_form)

    def segment_word(
        self,
        word: str,
        pos_hint: Optional[str] = None,
        dialect: Optional[Dialect] = None
    ) -> List[Segment]:
        """
        Segment a Coptic word into morphemes using Till's patterns.

        Args:
            word: Surface form (e.g., "ⲁϥⲃⲱⲕ")
            pos_hint: Optional POS tag hint
            dialect: Optional dialect override

        Returns:
            List of Segment objects

        Example:
            >>> analyzer.segment_word("ⲁϥⲃⲱⲕ", dialect=Dialect.SAHIDIC)
            [Segment("ⲁ", "ⲁ", "APST", {}, Dialect.SAHIDIC, "§261"),
             Segment("ϥ", "ⲛⲧⲟϥ", "PPERS", {...}, source_section="§117"),
             Segment("ⲃⲱⲕ", "ⲃⲱⲕ", "V", {})]
        """
        target_dialect = dialect or self.dialect

        # NEW: Try imperative forms (§231-244)
        result = self._try_imperative(word, target_dialect)
        if result:
            return result

        # NEW: Try quality/stative verbs (§219-230)
        result = self._try_quality_verb(word, target_dialect)
        if result:
            return result

        # Try verbal pattern (conjugation base + pronoun + verb)
        result = self._try_verbal_pattern(word, target_dialect)
        if result:
            return result

        # Try object pronoun pattern (e.g., ⲙⲙⲟϥ)
        result = self._try_object_pronoun(word, target_dialect)
        if result:
            return result

        # No segmentation found - return as single token
        return [Segment(
            form=word,
            lemma=word,
            pos=pos_hint or "UNKNOWN",
            feats={},
            dialect=target_dialect
        )]

    def _try_verbal_pattern(
        self,
        word: str,
        dialect: Dialect
    ) -> Optional[List[Segment]]:
        """
        Try to segment: CONJUGATION_BASE + PRONOUN + VERB

        Examples (Sahidic):
            ⲁϥⲃⲱⲕ → ⲁ + ϥ + ⲃⲱⲕ  (he went, §261)
            ⲉϥⲥⲱⲧⲙ → ⲉ + ϥ + ⲥⲱⲧⲙ (when he hears, §272)
            ⲛⲧⲉⲣⲉϥⲃⲱⲕ → ⲛⲧⲉⲣⲉ + ϥ + ⲃⲱⲕ (after he went, §265)
        """

        # Try conjugation bases (longest first to match greedy)
        for base_form in sorted(self.conjugation_bases.keys(), key=len, reverse=True):
            if not word.startswith(base_form):
                continue

            remainder = word[len(base_form):]
            if not remainder:
                continue

            base_pos, base_lemma = self.conjugation_bases[base_form]

            # Get dialectal form info
            df = self.dialect_handler.get_morpheme(base_form, dialect)
            source_section = df.source_section if df else None

            # Try to find pronoun at start of remainder
            for pron_form in sorted(self.pronouns.keys(), key=len, reverse=True):
                if not remainder.startswith(pron_form):
                    continue

                verb = remainder[len(pron_form):]
                if not verb or len(verb) < 2:  # Verb must be at least 2 chars
                    continue

                # Success! We found: base + pronoun + verb
                pron_lemma, pron_pos, pron_feats = self.pronouns[pron_form]

                return [
                    Segment(
                        form=base_form,
                        lemma=base_lemma,
                        pos=base_pos,
                        feats={},
                        dialect=dialect,
                        source_section=source_section
                    ),
                    Segment(
                        form=pron_form,
                        lemma=pron_lemma,
                        pos=pron_pos,
                        feats=pron_feats.copy(),
                        dialect=dialect,
                        source_section="§117"
                    ),
                    Segment(
                        form=verb,
                        lemma=verb,
                        pos="V",
                        feats={"VerbForm": "Fin"},
                        dialect=dialect
                    )
                ]

        return None

    def _try_imperative(
        self,
        word: str,
        dialect: Dialect
    ) -> Optional[List[Segment]]:
        """
        Try to match imperative forms (§231-244).

        Examples (Till):
            ⲁⲙⲟⲩ → "come!" (imperative)
            ⲁⲣⲓ → "do!" (imperative)
            ⲙⲁ → "give!" (imperative)
        """
        # Check if word is in imperative forms dictionary
        if word in self.imperative_forms:
            lemma, pos, source = self.imperative_forms[word]
            return [Segment(
                form=word,
                lemma=lemma,
                pos=pos,
                feats={"VerbForm": "Imp"},
                dialect=dialect,
                source_section=source
            )]

        return None

    def _try_quality_verb(
        self,
        word: str,
        dialect: Dialect
    ) -> Optional[List[Segment]]:
        """
        Try to match quality/stative verbs (§219-230).

        These verbs conjugate with subject suffixes directly (no infinitive).

        Examples (Till):
            ⲟⲩⲛ → "il y a" (existential)
            ⲛⲁⲁ → "grand" (quality: big)
            ⲡⲉⲭⲉ → "a dit" (quality: said)

        With suffixes:
            ⲟⲩⲛⲧⲁϥ → ⲟⲩⲛ + ⲧⲁ + ϥ (il a)
            ⲡⲉⲭⲁϥ → ⲡⲉⲭⲁ + ϥ (he said)
        """
        # Try to match quality verb stems
        for verb_form in sorted(self.quality_verbs.keys(), key=len, reverse=True):
            if not word.startswith(verb_form):
                continue

            remainder = word[len(verb_form):]
            lemma, pos, feats = self.quality_verbs[verb_form]

            # If no remainder, return the verb alone
            if not remainder:
                return [Segment(
                    form=word,
                    lemma=lemma,
                    pos=pos,
                    feats=feats.copy(),
                    dialect=dialect,
                    source_section="§219-230"
                )]

            # Check for suffix patterns (§226-227)
            # Pattern: VERB + ⲧⲁ/ⲧⲉ + PRONOUN (with nominal/pronominal subject)
            # Example: ⲟⲩⲛⲧⲁϥ → ⲟⲩⲛ + ⲧⲁ + ϥ
            if remainder.startswith("ⲧⲁ") or remainder.startswith("ⲧⲉ"):
                suffix = remainder[:2]  # ⲧⲁ or ⲧⲉ
                pron = remainder[2:]

                if pron in self.pronouns:
                    pron_lemma, pron_pos, pron_feats = self.pronouns[pron]
                    return [
                        Segment(
                            form=verb_form,
                            lemma=lemma,
                            pos=pos,
                            feats=feats.copy(),
                            dialect=dialect,
                            source_section="§226"
                        ),
                        Segment(
                            form=suffix,
                            lemma=suffix,
                            pos="PART",  # Particle linking verb to subject
                            feats={},
                            dialect=dialect
                        ),
                        Segment(
                            form=pron,
                            lemma=pron_lemma,
                            pos=pron_pos,
                            feats=pron_feats.copy(),
                            dialect=dialect
                        )
                    ]

            # Check for direct pronoun suffix (§220-225)
            # Some quality verbs can take direct suffixes
            # Example: ⲡⲉⲭⲁϥ → ⲡⲉⲭⲁ + ϥ
            if remainder in self.pronouns:
                pron_lemma, pron_pos, pron_feats = self.pronouns[remainder]
                return [
                    Segment(
                        form=verb_form,
                        lemma=lemma,
                        pos=pos,
                        feats=feats.copy(),
                        dialect=dialect,
                        source_section="§220-225"
                    ),
                    Segment(
                        form=remainder,
                        lemma=pron_lemma,
                        pos=pron_pos,
                        feats=pron_feats.copy(),
                        dialect=dialect
                    )
                ]

        return None

    def _try_object_pronoun(
        self,
        word: str,
        dialect: Dialect
    ) -> Optional[List[Segment]]:
        """
        Try to segment: PREP + PRONOUN (object pronouns)

        Examples:
            ⲙⲙⲟϥ → ⲙⲙⲟ + ϥ  (him, accusative)
            ⲉⲣⲟⲕ → ⲉⲣⲟ + ⲕ  (to you)
        """

        # Try object pronoun prefixes
        for prep_form in sorted(self.object_pronouns.keys(), key=len, reverse=True):
            if not word.startswith(prep_form):
                continue

            remainder = word[len(prep_form):]
            if not remainder:
                continue

            prep_lemma, prep_pos = self.object_pronouns[prep_form]

            # Check if remainder is a pronoun suffix
            if remainder in self.pronouns:
                pron_lemma, pron_pos, pron_feats = self.pronouns[remainder]

                return [
                    Segment(
                        form=prep_form,
                        lemma=prep_lemma,
                        pos=prep_pos,
                        feats={},
                        dialect=dialect
                    ),
                    Segment(
                        form=remainder,
                        lemma=pron_lemma,
                        pos="PPERO",
                        feats=pron_feats.copy(),
                        dialect=dialect
                    )
                ]

        return None

    def is_fused(self, word: str, dialect: Optional[Dialect] = None) -> bool:
        """
        Check if word is likely a fused form that needs segmentation.

        Args:
            word: Word to check
            dialect: Optional dialect

        Returns:
            True if word appears to be fused
        """
        target_dialect = dialect or self.dialect

        # Quick heuristic checks
        for base in self.conjugation_bases.keys():
            if word.startswith(base) and len(word) > len(base) + 1:
                return True

        for prep in self.object_pronouns.keys():
            if word.startswith(prep) and len(word) > len(prep):
                return True

        return False

    def get_multitoken_range(self, segments: List[Segment], start_id: int) -> Tuple[int, int]:
        """
        Calculate ID range for multi-token word.

        Args:
            segments: List of segments
            start_id: Starting token ID

        Returns:
            Tuple of (start_id, end_id) for CoNLL-U range notation
        """
        return (start_id, start_id + len(segments) - 1)


def create_morphology_analyzer_till(
    dialect: Dialect = Dialect.SAHIDIC,
    prolog_engine=None
) -> CopticMorphologyAnalyzerTill:
    """
    Factory function to create Till-based morphology analyzer.

    Args:
        dialect: Default dialect for parsing
        prolog_engine: Optional Prolog engine for enhanced feature lookup

    Returns:
        CopticMorphologyAnalyzerTill instance
    """
    return CopticMorphologyAnalyzerTill(dialect, prolog_engine)
