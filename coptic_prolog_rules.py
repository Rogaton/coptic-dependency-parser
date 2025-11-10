#!/usr/bin/env python3
"""
Coptic Prolog Rules - Neural-Symbolic Integration
==================================================

Integrates Prolog logic programming with neural dependency parsing
to enhance parsing accuracy through explicit grammatical rules.

Uses PySwip (SWI-Prolog Python interface) for bidirectional integration.

Author: Coptic NLP Project
License: CC BY-NC-SA 4.0
"""

from pyswip import Prolog
import warnings
warnings.filterwarnings('ignore')


class CopticPrologRules:
    """
    Prolog-based grammatical rule engine for Coptic parsing validation
    and enhancement.
    """

    def __init__(self):
        """Initialize Prolog engine and load Coptic grammar rules"""
        self.prolog_initialized = False
        self.prolog = None

        # Initialize enhanced morphology analyzer (solves Lessons 11 & 13 bottleneck)
        try:
            from coptic_morphology import CopticMorphologyAnalyzer
            self.morphology_analyzer = CopticMorphologyAnalyzer()
            print("✓ Enhanced morphology analyzer loaded (L11 & L13 fix)")
        except ImportError:
            self.morphology_analyzer = None
            print("ℹ Enhanced morphology not available (using Prolog-only)")

        self._initialize_prolog()

    def _initialize_prolog(self):
        """Initialize SWI-Prolog and define Coptic grammatical rules"""
        try:
            # Initialize pyswip Prolog instance
            self.prolog = Prolog()

            # Define Coptic-specific grammatical rules
            self._load_coptic_grammar()

            self.prolog_initialized = True
            print("✓ Prolog engine initialized successfully")

        except Exception as e:
            print(f"⚠️  Warning: Prolog initialization failed: {e}")
            print("   Parser will continue without Prolog validation")
            self.prolog_initialized = False

    def _load_dependency_grammar(self):
        """
        Load dependency-based grammar rules from coptic_grammar.pl
        and Coptic lexicon from coptic_lexicon.pl

        This loads the modern dependency grammar formalism, adapted from the DCG-based DETECT5.PRO error detector and checker for French L2 (André Linden 1991).
        """
        try:
            from pathlib import Path

            # Get path to DCG grammar file
            # Note: The grammar file will load the lexicon automatically via ensure_loaded
            current_dir = Path(__file__).parent
            grammar_file = current_dir / "coptic_grammar.pl"

            # Load grammar rules (which will load the lexicon)
            if grammar_file.exists():
                # Convert path to Prolog-compatible format
                grammar_path = str(grammar_file.absolute()).replace('\\', '/')

                # Load the module
                query = f"consult('{grammar_path}')"
                list(self.prolog.query(query))

                print(f"✓ DCG grammar rules and lexicon loaded from {grammar_file.name}")
                self.dcg_loaded = True
            else:
                print(f"ℹ  DCG grammar file not found at {grammar_file}")
                self.dcg_loaded = False

        except Exception as e:
            print(f"⚠️  Warning: Could not load DCG grammar: {e}")
            self.dcg_loaded = False

    def _load_coptic_grammar(self):
        """Load Coptic linguistic rules into Prolog"""

        # Try to load DCG grammar file if it exists
        self._load_dependency_grammar()

        # ===================================================================
        # COPTIC MORPHOLOGICAL RULES
        # ===================================================================

        # Article system: definite articles
        self.prolog.assertz("definite_article('ⲡ')")      # masculine singular
        self.prolog.assertz("definite_article('ⲧ')")      # feminine singular
        self.prolog.assertz("definite_article('ⲛ')")      # plural
        self.prolog.assertz("definite_article('ⲡⲉ')")     # masculine singular (variant)
        self.prolog.assertz("definite_article('ⲧⲉ')")     # feminine singular (variant)
        self.prolog.assertz("definite_article('ⲛⲉ')")     # plural (variant)

        # Pronominal system - Independent pronouns
        self.prolog.assertz("independent_pronoun('ⲁⲛⲟⲕ')")     # I
        self.prolog.assertz("independent_pronoun('ⲛⲧⲟⲕ')")     # you (m.sg)
        self.prolog.assertz("independent_pronoun('ⲛⲧⲟ')")      # you (f.sg)
        self.prolog.assertz("independent_pronoun('ⲛⲧⲟϥ')")     # he
        self.prolog.assertz("independent_pronoun('ⲛⲧⲟⲥ')")     # she
        self.prolog.assertz("independent_pronoun('ⲁⲛⲟⲛ')")     # we
        self.prolog.assertz("independent_pronoun('ⲛⲧⲱⲧⲛ')")    # you (pl)
        self.prolog.assertz("independent_pronoun('ⲛⲧⲟⲟⲩ')")    # they

        # Suffix pronouns (enclitic)
        self.prolog.assertz("suffix_pronoun('ⲓ')")   # my/me
        self.prolog.assertz("suffix_pronoun('ⲕ')")   # your (m.sg)
        self.prolog.assertz("suffix_pronoun('ϥ')")   # his/him
        self.prolog.assertz("suffix_pronoun('ⲥ')")   # her
        self.prolog.assertz("suffix_pronoun('ⲛ')")   # our/us
        self.prolog.assertz("suffix_pronoun('ⲧⲛ')")  # your (pl)
        self.prolog.assertz("suffix_pronoun('ⲟⲩ')")  # their/them

        # Coptic verbal system - Conjugation bases (tense/aspect markers)
        self.prolog.assertz("conjugation_base('ⲁ')")      # Perfect (aorist)
        self.prolog.assertz("conjugation_base('ⲛⲉ')")     # Imperfect/past
        self.prolog.assertz("conjugation_base('ϣⲁ')")     # Future/conditional
        self.prolog.assertz("conjugation_base('ⲙⲡⲉ')")    # Negative perfect
        self.prolog.assertz("conjugation_base('ⲙⲛ')")     # Negative existential
        self.prolog.assertz("conjugation_base('ⲉⲣϣⲁⲛ')")  # Conditional

        # ===================================================================
        # CIRCUMSTANTIAL CONVERSION
        # ===================================================================

        # Circumstantial converters - mark subordinate temporal/causal clauses
        self.prolog.assertz("circumstantial_converter('ⲉ')")     # e- (with pronouns)
        self.prolog.assertz("circumstantial_converter('ⲉⲣⲉ')")   # epe- (with nouns)

        # Circumstantial with suffix pronouns (ⲉⲓ-, ⲉⲕ-, ⲉϥ-, ⲉⲥ-, etc.)
        # These are compound forms: converter + pronoun as single unit
        self.prolog.assertz("circumstantial_pronoun('ⲉⲓ', first, sing)")     # when I
        self.prolog.assertz("circumstantial_pronoun('ⲉⲕ', second, sing)")    # when you (m)
        self.prolog.assertz("circumstantial_pronoun('ⲉ', second, sing)")     # when you (f)
        self.prolog.assertz("circumstantial_pronoun('ⲉϥ', third, masc)")     # when he
        self.prolog.assertz("circumstantial_pronoun('ⲉⲥ', third, fem)")      # when she
        self.prolog.assertz("circumstantial_pronoun('ⲉⲛ', first, plur)")     # when we
        self.prolog.assertz("circumstantial_pronoun('ⲉⲧⲉⲧⲛ', second, plur)") # when you (pl)
        self.prolog.assertz("circumstantial_pronoun('ⲉⲩ', third, plur)")     # when they

        # Pattern: Circumstantial + Verb (with pronominal subject)
        # Example: ⲉϥⲥⲱⲧⲙ "when/while he hears"
        self.prolog.assertz("""
            circumstantial_clause(Converter, Verb) :-
                circumstantial_pronoun(Converter, _, _),
                verb_compatible(Verb)
        """)

        # Pattern: ⲉⲣⲉ- + Nominal Subject + Verb
        # Example: ⲉⲣⲉⲡⲣⲱⲙⲉⲥⲱⲧⲙ "when the man hears"
        self.prolog.assertz("""
            circumstantial_nominal_clause(Converter, Subject, Verb) :-
                Converter = 'ⲉⲣⲉ',
                (noun_compatible(Subject) ; definite_article(Subject)),
                verb_compatible(Verb)
        """)

        # Circumstantial of Preterit (nested): ⲉ- + ⲁ- + pronoun + verb
        # Example: ⲉⲁϥⲥⲱⲧⲙ "when he heard"
        self.prolog.assertz("""
            circumstantial_preterit(Circ, Pret, Subject, Verb) :-
                circumstantial_converter(Circ),
                Pret = 'ⲁ',
                suffix_pronoun(Subject),
                verb_compatible(Verb)
        """)

        # Negative circumstantial: ⲉⲛ-...-ⲁⲛ or ⲉⲙⲡ-...-ⲁⲛ
        self.prolog.assertz("negative_circumstantial('ⲉⲛ')")    # e-N-
        self.prolog.assertz("negative_circumstantial('ⲉⲙⲡ')")   # e-Mn-

        print("✓ Circumstantial conversion rules loaded")

        # ===================================================================
        # RELATIVE CONVERSION
        # ===================================================================

        # Relative converter - marks relative clauses modifying nouns/pronouns
        # Unlike English, Coptic uses a converter (not relative pronouns who/which/that)
        # The converter signals: "modified by the following complete statement"
        self.prolog.assertz("relative_converter('ⲉⲛⲧ')")     # ENT- basic form
        self.prolog.assertz("relative_converter('ⲉⲧ')")      # ET- short form

        # Relative converter with pronouns (compound forms)
        # ⲉⲛⲧⲁ- = relative + preterit marker (who/which [did])
        self.prolog.assertz("relative_preterit_compound('ⲉⲛⲧⲁϥ', third, masc)")   # who he [did]
        self.prolog.assertz("relative_preterit_compound('ⲉⲛⲧⲁⲥ', third, fem)")    # who she [did]
        self.prolog.assertz("relative_preterit_compound('ⲉⲛⲧⲁⲓ', first, sing)")   # who I [did]
        self.prolog.assertz("relative_preterit_compound('ⲉⲛⲧⲁⲛ', first, plur)")   # who we [did]
        self.prolog.assertz("relative_preterit_compound('ⲉⲛⲧⲁⲧⲉⲧⲛ', second, plur)") # who you(pl) [did]
        self.prolog.assertz("relative_preterit_compound('ⲉⲛⲧⲁⲩ', third, plur)")   # who they [did]

        # Short forms with ⲉⲧ-
        self.prolog.assertz("relative_preterit_compound('ⲉⲧⲁϥ', third, masc)")
        self.prolog.assertz("relative_preterit_compound('ⲉⲧⲁⲥ', third, fem)")

        # Pattern 1: Noun/Pronoun + ⲉⲛⲧ + Complete Clause
        # Example: ⲡⲣⲱⲙⲉ ⲉⲛⲧⲁϥⲕⲱⲧ "the man who built"
        self.prolog.assertz("""
            relative_clause(Head, Converter, Verb) :-
                (noun_compatible(Head) ; definite_article(Head) ; independent_pronoun(Head)),
                relative_converter(Converter),
                verb_compatible(Verb)
        """)

        # Pattern 2: Noun + Relative-Preterit Compound + Verb
        # Example: ⲡⲣⲱⲙⲉ ⲉⲛⲧⲁϥⲕⲱⲧ "the man who built"
        # (where ⲉⲛⲧⲁϥ is a single token: converter + preterit + pronoun)
        self.prolog.assertz("""
            relative_preterit_clause(Head, Compound, Verb) :-
                (noun_compatible(Head) ; definite_article(Head)),
                relative_preterit_compound(Compound, _, _),
                verb_compatible(Verb)
        """)

        # Pattern 3: Article alone as head (substantivized relative)
        # Example: ⲧⲉⲛⲧⲁϥⲕⲱⲧ "the one who built" (feminine)
        # "The one" is expressed by definite article alone before converter
        self.prolog.assertz("""
            substantivized_relative(Article, Converter) :-
                definite_article(Article),
                relative_converter(Converter)
        """)

        # Negative relative: ⲉⲧⲉ...ⲁⲛ
        self.prolog.assertz("negative_relative_converter('ⲉⲧⲉ')")

        self.prolog.assertz("""
            negative_relative_clause(Head, Converter, Verb, Neg) :-
                (noun_compatible(Head) ; definite_article(Head)),
                negative_relative_converter(Converter),
                verb_compatible(Verb),
                Neg = 'ⲁⲛ'
        """)

        print("✓ Relative conversion rules loaded")

        # ===================================================================
        # CONDITIONAL SENTENCES
        # ===================================================================

        # Three types of conditionals in Coptic:
        # (1) Presupposed/possible fact: "if/since X is true, then Y is true"
        # (2) Generalization: "if/whenever X is true, Y is/will be true"
        # (3) Contrary to fact: "if X were true, then Y would be true"

        # ===================================================================
        # TYPE 1: PRESUPPOSED OR POSSIBLE FACT (§150)
        # ===================================================================

        # Conditional markers for presupposed/possible fact
        self.prolog.assertz("conditional_presupposed('ⲉⲛⲉⲓ')")         # since, inasmuch as
        self.prolog.assertz("conditional_presupposed('ⲉⲛⲉⲓⲇⲏ')")       # since, inasmuch as
        self.prolog.assertz("conditional_presupposed('ⲉⲛⲉⲓⲇⲏⲡⲉⲣ')")     # since, inasmuch as
        self.prolog.assertz("conditional_presupposed('ⲉϣⲱⲡⲉ')")        # if (as may be the case)
        self.prolog.assertz("conditional_presupposed('ⲉϣϫⲉⲡⲉ')")       # if (as may be the case)
        self.prolog.assertz("conditional_presupposed('ⲕⲁⲛ')")          # even if
        self.prolog.assertz("conditional_presupposed('ⲕⲁⲛⲉϣϫⲉ')")      # even if
        self.prolog.assertz("conditional_presupposed('ⲉⲃⲟⲗϫⲉ')")       # because
        self.prolog.assertz("conditional_presupposed('ⲉⲧⲃⲉϫⲉ')")       # because

        # Pattern: Conditional marker + clause → then clause
        self.prolog.assertz("""
            conditional_presupposed_clause(Marker, Clause) :-
                conditional_presupposed(Marker),
                verb_compatible(Clause)
        """)

        # ===================================================================
        # TYPE 2: GENERALIZATION (§151)
        # ===================================================================

        # Conditional markers for generalization (if ever, whenever)
        self.prolog.assertz("conditional_generalization('ⲉϣⲱⲡⲉ')")     # if ever, whenever
        self.prolog.assertz("conditional_generalization('ⲉⲣϣⲁⲛ')")     # if, whenever
        self.prolog.assertz("conditional_generalization('ⲉⲣϣⲁⲛ')")     # if (already defined)
        self.prolog.assertz("conditional_generalization('ⲕⲁⲛ')")       # even if

        # Pattern: If ever X, then Y will be
        self.prolog.assertz("""
            conditional_generalization_clause(Marker, IfClause, ThenMarker) :-
                conditional_generalization(Marker),
                verb_compatible(IfClause),
                (ThenMarker = 'ⲛⲁ' ; ThenMarker = 'ϣⲁ')
        """)

        # ===================================================================
        # TYPE 3: CONTRARY TO FACT (§152)
        # ===================================================================

        # (a) Present tense contrary to fact: "if X were..., Y would..."
        # If-clause: circumstantial preterit ⲉⲛⲉⲣⲉ-, ⲉⲛⲉ-
        self.prolog.assertz("contrary_to_fact_present('ⲉⲛⲉⲣⲉ')")      # if... were (with noun subject)
        self.prolog.assertz("contrary_to_fact_present('ⲉⲛⲉ')")        # if... were

        # Then-clause markers: ⲛⲁ- (durative), ⲛⲉ- (other types), ⲛⲉⲣⲉ-
        self.prolog.assertz("contrary_then_marker('ⲛⲁ')")             # would (durative)
        self.prolog.assertz("contrary_then_marker('ⲛⲉ')")             # would (preterit)
        self.prolog.assertz("contrary_then_marker('ⲛⲉⲣⲉ')")           # would (with noun)

        # Pattern: If X were true (but isn't), then Y would be true
        self.prolog.assertz("""
            contrary_to_fact_present_clause(IfMarker, ThenMarker) :-
                contrary_to_fact_present(IfMarker),
                contrary_then_marker(ThenMarker)
        """)

        # (b) Past tense contrary to fact: "if X had..., Y would have..."
        # If-clause: ⲉⲛⲉⲛⲧⲁ- (affirmative), ⲉⲛⲉⲙⲡⲉ- (negative)
        self.prolog.assertz("contrary_to_fact_past_aff('ⲉⲛⲉⲛⲧⲁ')")    # if... had (affirmative)
        self.prolog.assertz("contrary_to_fact_past_neg('ⲉⲛⲉⲙⲡⲉ')")    # if... had not (negative)

        # Then-clause markers: ⲉϣϫⲛⲉ, ⲉϣϫⲉ, ⲛⲉⲉⲓϣⲡⲉ + past tense
        self.prolog.assertz("contrary_past_then('ⲉϣϫⲛⲉ')")            # would have
        self.prolog.assertz("contrary_past_then('ⲉϣϫⲉ')")             # would have
        self.prolog.assertz("contrary_past_then('ⲛⲉⲉⲓϣⲡⲉ')")          # would have

        # Pattern: If X had been true (but wasn't), Y would have been true
        self.prolog.assertz("""
            contrary_to_fact_past_clause(IfMarker, ThenMarker) :-
                (contrary_to_fact_past_aff(IfMarker) ; contrary_to_fact_past_neg(IfMarker)),
                contrary_past_then(ThenMarker)
        """)

        print("✓ Conditional sentence rules loaded")

        # ===================================================================
        # NON-DURATIVE CONJUGATION BASES
        # ===================================================================

        # Non-durative verbal sentence: Base + Subject + Infinitive
        # Five main clause conjugation bases (§76)

        # ===================================================================
        # 1. PAST/PRETERIT (PERFECTIVE) - Most common! (§77)
        # ===================================================================

        # Affirmative: ⲁ- (a-)
        # Meaning: Past narration OR present perfect ("he went" or "he has gone")

        # Compound forms: conjugation base + suffix pronoun as single unit
        self.prolog.assertz("past_affirmative('ⲁⲓ', first, sing)")       # I
        self.prolog.assertz("past_affirmative('ⲁⲕ', second, sing, masc)") # you (m)
        self.prolog.assertz("past_affirmative('ⲁⲣ', second, sing, fem)")  # you (f) - variant
        self.prolog.assertz("past_affirmative('ⲁⲣⲉ', second, sing, fem)") # you (f)
        self.prolog.assertz("past_affirmative('ⲁϥ', third, masc)")        # he
        self.prolog.assertz("past_affirmative('ⲁⲥ', third, fem)")         # she
        self.prolog.assertz("past_affirmative('ⲁⲛ', first, plur)")        # we
        self.prolog.assertz("past_affirmative('ⲁⲧⲉⲧⲛ', second, plur)")    # you (pl)
        self.prolog.assertz("past_affirmative('ⲁⲩ', third, plur)")        # they

        # Separated form with nominal subject
        self.prolog.assertz("past_base_separated('ⲁ')")  # ⲁ + noun + verb

        # Pattern: Past compound + Infinitive
        self.prolog.assertz("""
            past_affirmative_pattern(Compound, Verb) :-
                past_affirmative(Compound, _, _),
                verb_compatible(Verb)
        """)

        # Negative: ⲙⲡⲉ- (mpe-)
        self.prolog.assertz("past_negative('ⲙⲡⲉⲓ', first, sing)")
        self.prolog.assertz("past_negative('ⲙⲡⲉⲕ', second, sing, masc)")
        self.prolog.assertz("past_negative('ⲙⲡⲉ', second, sing, fem)")
        self.prolog.assertz("past_negative('ⲙⲡⲉϥ', third, masc)")
        self.prolog.assertz("past_negative('ⲙⲡⲉⲥ', third, fem)")
        self.prolog.assertz("past_negative('ⲙⲡⲉⲛ', first, plur)")
        self.prolog.assertz("past_negative('ⲙⲡⲉⲧⲉⲧⲛ', second, plur)")
        self.prolog.assertz("past_negative('ⲙⲡⲟⲩ', third, plur)")

        self.prolog.assertz("""
            past_negative_pattern(Compound, Verb) :-
                past_negative(Compound, _, _),
                verb_compatible(Verb)
        """)

        # ===================================================================
        # 2. 'NOT YET' (§78)
        # ===================================================================

        # ⲙⲡⲁⲧⲉ- (mpate-) - "has not yet..." (with expectation)
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧⲓ', first, sing)")
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧⲕ', second, sing, masc)")
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧⲉ', second, sing, fem)")
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧϥ', third, masc)")
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧⲥ', third, fem)")
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧⲛ', first, plur)")
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧⲉⲧⲛ', second, plur)")
        self.prolog.assertz("not_yet('ⲙⲡⲁⲧⲟⲩ', third, plur)")

        self.prolog.assertz("""
            not_yet_pattern(Compound, Verb) :-
                not_yet(Compound, _, _),
                verb_compatible(Verb)
        """)

        # ===================================================================
        # 3. AORIST (§79) - Unique Coptic feature!
        # ===================================================================

        # ϣⲁⲣⲉ- (share-) affirmative / ⲙⲉⲣⲉ- (mere-) negative
        # Tenseless: forms complete sentence without expressing tense
        # Uses: (1) timeless truths, (2) past narration (storytelling)

        # Affirmative
        self.prolog.assertz("aorist_affirmative('ϣⲁⲓ', first, sing)")
        self.prolog.assertz("aorist_affirmative('ϣⲁⲕ', second, sing, masc)")
        self.prolog.assertz("aorist_affirmative('ϣⲁⲣⲉ', second, sing, fem)")
        self.prolog.assertz("aorist_affirmative('ϣⲁϥ', third, masc)")
        self.prolog.assertz("aorist_affirmative('ϣⲁⲥ', third, fem)")
        self.prolog.assertz("aorist_affirmative('ϣⲁⲛ', first, plur)")
        self.prolog.assertz("aorist_affirmative('ϣⲁⲧⲉⲧⲛ', second, plur)")
        self.prolog.assertz("aorist_affirmative('ϣⲁⲩ', third, plur)")

        self.prolog.assertz("""
            aorist_affirmative_pattern(Compound, Verb) :-
                aorist_affirmative(Compound, _, _),
                verb_compatible(Verb)
        """)

        # Negative
        self.prolog.assertz("aorist_negative('ⲙⲉⲓ', first, sing)")
        self.prolog.assertz("aorist_negative('ⲙⲉⲕ', second, sing, masc)")
        self.prolog.assertz("aorist_negative('ⲙⲉⲣⲉ', second, sing, fem)")
        self.prolog.assertz("aorist_negative('ⲙⲉϥ', third, masc)")
        self.prolog.assertz("aorist_negative('ⲙⲉⲥ', third, fem)")
        self.prolog.assertz("aorist_negative('ⲙⲉⲛ', first, plur)")
        self.prolog.assertz("aorist_negative('ⲙⲉⲧⲉⲧⲛ', second, plur)")
        self.prolog.assertz("aorist_negative('ⲙⲉⲩ', third, plur)")

        self.prolog.assertz("""
            aorist_negative_pattern(Compound, Verb) :-
                aorist_negative(Compound, _, _),
                verb_compatible(Verb)
        """)

        # ===================================================================
        # 4. OPTATIVE (§76, details in §81-82)
        # ===================================================================

        # ⲉⲣⲉ- (ere-) affirmative / ⲛⲛⲉ- (nne-) negative
        # Meaning: "shall/might..."
        self.prolog.assertz("optative_marker('ⲉⲣⲉ')")
        self.prolog.assertz("optative_marker('ⲛⲛⲉ')")

        # ===================================================================
        # 5. JUSSIVE (§76, details in §81-82)
        # ===================================================================

        # ⲙⲁⲣⲉ- (mare-) affirmative / ⲙⲡⲣⲧⲣⲉ- (mprtre-) negative
        # Meaning: "let him...", "he ought to..."
        self.prolog.assertz("jussive_affirmative('ⲙⲁⲣⲉ')")
        self.prolog.assertz("jussive_negative('ⲙⲡⲣⲧⲣⲉ')")

        print("✓ Non-durative conjugation bases loaded")

        # ===================================================================
        # DURATIVE SENTENCE, INFINITIVE, AND STATIVE
        # ===================================================================
        # The durative (present tense) expresses ongoing action or state

        # DURATIVE/PRESENT TENSE PATTERNS
        # ================================
        # Affirmative durative with pronominal subject
        # Pattern: ϥ-/ⲥ- + INFINITIVE (he/she does...)
        self.prolog.assertz("durative_present('ϥ', third, masc)")    # he (does)
        self.prolog.assertz("durative_present('ⲥ', third, fem)")     # she (does)
        self.prolog.assertz("durative_present('ϯ', first, sing)")    # I (do)
        self.prolog.assertz("durative_present('ⲕ', second, masc)")   # you (do) m.
        self.prolog.assertz("durative_present('ⲧⲉ', second, fem)")   # you (do) f.
        self.prolog.assertz("durative_present('ⲥⲉ', third, plur)")   # they (do)
        self.prolog.assertz("durative_present('ⲧⲛ', first, plur)")   # we (do)
        self.prolog.assertz("durative_present('ⲧⲉⲧⲛ', second, plur)") # you (do) pl.

        # Durative with nominal subject: ⲉⲣⲉ- + NOUN + INFINITIVE
        self.prolog.assertz("durative_nominal_marker('ⲉⲣⲉ')")      # ere- (with nouns)
        self.prolog.assertz("durative_nominal_marker('ⲉⲣ')")       # er- (variant)

        # Negative durative: ⲛ- + SUBJECT + INFINITIVE + ⲁⲛ
        self.prolog.assertz("durative_negative_prefix('ⲛ')")       # n- negative prefix
        self.prolog.assertz("durative_negative_suffix('ⲁⲛ')")      # an negative suffix

        # INFINITIVE PATTERNS (§69)
        # =========================
        # Coptic infinitives are verbal nouns
        # Common infinitive markers and forms
        self.prolog.assertz("infinitive_marker('ⲉ')")              # e- (to)
        self.prolog.assertz("infinitive_marker('ⲣ')")              # r- (to do)

        # Common infinitives
        self.prolog.assertz("infinitive('ⲃⲱⲕ')")                   # to go
        self.prolog.assertz("infinitive('ⲥⲱⲧⲙ')")                  # to hear
        self.prolog.assertz("infinitive('ⲉⲓ')")                    # to come
        self.prolog.assertz("infinitive('ⲛⲁⲩ')")                   # to see
        self.prolog.assertz("infinitive('ϫⲱ')")                    # to say
        self.prolog.assertz("infinitive('ϯ')")                     # to give
        self.prolog.assertz("infinitive('ϫⲓ')")                    # to take
        self.prolog.assertz("infinitive('ⲙⲟⲩ')")                   # to die

        # STATIVE PATTERNS (§70)
        # ======================
        # Statives express resultant state (similar to perfect or passive)
        # Pattern: ϥ + STATIVE (he is in state of...)
        self.prolog.assertz("stative('ⲙⲟⲩⲧ')")                    # be dead
        self.prolog.assertz("stative('ⲟⲛϩ')")                     # be alive
        self.prolog.assertz("stative('ⲟⲩⲱⲙ')")                    # be eaten
        self.prolog.assertz("stative('ⲥⲱⲧⲙ')")                    # be heard (can be inf or stative)

        print("✓ Durative sentence, infinitive, and stative loaded")

        # ===================================================================
        # FOCALIZING CONVERSION
        # ===================================================================
        # Focalizing (cleft sentences) emphasizes a particular constituent
        # Pattern: FOCUSED_ELEMENT + ⲡⲉ/ⲧⲉ/ⲛⲉ + Relative_Clause
        # Example: "It is X that..." or "X is the one who..."

        # Focalizing copulas (same as regular copulas but in focusing function)
        self.prolog.assertz("focus_copula('ⲡⲉ', masc, sing)")      # it is (m.sg)
        self.prolog.assertz("focus_copula('ⲧⲉ', fem, sing)")       # it is (f.sg)
        self.prolog.assertz("focus_copula('ⲛⲉ', plur, plur)")      # it is (pl)

        # Focalizing pattern with relative converter
        # Structure: [FOCUSED] + [COPULA] + [ⲉⲛⲧ/ⲉⲧ] + [CLAUSE]
        # The focused element is fronted and identified with copula
        self.prolog.assertz("focalizing_marker('ⲛⲧⲟϥ')")          # ntof - "it is he"
        self.prolog.assertz("focalizing_marker('ⲛⲧⲟⲥ')")          # ntos - "it is she"
        self.prolog.assertz("focalizing_marker('ⲁⲛⲟⲕ')")          # anok - "it is I"

        # Second tense (focalizing on verb): ⲛⲧⲁϥ- forms
        # These focus on the ACTION rather than the subject
        self.prolog.assertz("second_tense('ⲛⲧⲁϥ', third, masc)")   # (it was) he (who did)
        self.prolog.assertz("second_tense('ⲛⲧⲁⲥ', third, fem)")    # (it was) she (who did)
        self.prolog.assertz("second_tense('ⲛⲧⲁⲓ', first, sing)")   # (it was) I (who did)
        self.prolog.assertz("second_tense('ⲛⲧⲁⲕ', second, masc)")  # (it was) you (who did)
        self.prolog.assertz("second_tense('ⲛⲧⲁⲣⲉ', second, fem)")  # (it was) you (who did) f.
        self.prolog.assertz("second_tense('ⲛⲧⲁⲩ', third, plur)")   # (it was) they (who did)

        print("✓ Focalizing conversion loaded")

        # ===================================================================
        # IMPERATIVES AND BOUND INFINITIVES
        # ===================================================================
        # The imperative expresses commands, requests, prohibitions

        # IMPERATIVE PATTERNS
        # ===================
        # Affirmative imperative: ⲁⲣⲓ- prefix
        # Pattern: ⲁⲣⲓ- + INFINITIVE (Do [verb]!)
        self.prolog.assertz("imperative_affirmative('ⲁⲣⲓ')")          # ari- basic form

        # With pronominal suffixes for "you" (singular/plural)
        self.prolog.assertz("imperative_affirmative('ⲁⲣⲓⲕ', second, masc)")   # you (m) do!
        self.prolog.assertz("imperative_affirmative('ⲁⲣⲓⲧⲉ', second, fem)")   # you (f) do!
        self.prolog.assertz("imperative_affirmative('ⲁⲣⲓⲧⲛ', second, plur)")  # you (pl) do!

        # Negative imperative/prohibition: ⲙⲡⲣ- prefix
        # Pattern: ⲙⲡⲣ- + INFINITIVE (Do not [verb]!)
        self.prolog.assertz("imperative_negative('ⲙⲡⲣ')")            # mpr- basic form

        # With pronominal suffixes
        self.prolog.assertz("imperative_negative('ⲙⲡⲣⲕ', second, masc)")    # you (m) don't!
        self.prolog.assertz("imperative_negative('ⲙⲡⲣⲧⲉ', second, fem)")    # you (f) don't!
        self.prolog.assertz("imperative_negative('ⲙⲡⲣⲧⲛ', second, plur)")   # you (pl) don't!

        # Simple imperative (bare infinitive as command)
        # Some common verbs can be used as imperatives without prefix
        self.prolog.assertz("imperative_simple('ⲁⲙⲟⲩ')")           # come!
        self.prolog.assertz("imperative_simple('ⲃⲱⲕ')")            # go!
        self.prolog.assertz("imperative_simple('ⲥⲱⲧⲙ')")           # listen!

        # BOUND INFINITIVE PATTERNS (§91-93)
        # ===================================
        # Infinitives in bound state (with direct object)
        # Pattern: VERB + ⲉ- + INFINITIVE or VERB + ⲙⲙⲟ- + PRONOUN
        self.prolog.assertz("infinitive_marker_bound('ⲉ')")         # e- before infinitive
        self.prolog.assertz("infinitive_marker_bound('ⲙⲙⲟ')")      # mmo- before pronoun obj

        print("✓ Imperatives and bound infinitives loaded")

        # ===================================================================
        # CAUSATIVE AND PASSIVE
        # ===================================================================
        # Causatives express "cause X to do Y" or "make X happen"
        # Passives express "be [verb]ed"

        # CAUSATIVE INFINITIVE (§111-112)
        # ================================
        # Pattern: ⲧⲣⲉ- + SUBJECT + INFINITIVE
        # Meaning: "cause [subject] to [verb]" or "make [subject] [verb]"

        # With pronominal suffixes
        self.prolog.assertz("causative('ⲧⲣⲉ')")                     # tre- basic form
        self.prolog.assertz("causative('ⲧⲣⲁ', first, sing)")        # make me...
        self.prolog.assertz("causative('ⲧⲣⲉⲕ', second, masc)")      # make you (m)...
        self.prolog.assertz("causative('ⲧⲣⲉⲧⲉ', second, fem)")      # make you (f)...
        self.prolog.assertz("causative('ⲧⲣⲉϥ', third, masc)")       # make him...
        self.prolog.assertz("causative('ⲧⲣⲉⲥ', third, fem)")        # make her...
        self.prolog.assertz("causative('ⲧⲣⲉⲛ', first, plur)")       # make us...
        self.prolog.assertz("causative('ⲧⲣⲉⲧⲛ', second, plur)")     # make you (pl)...
        self.prolog.assertz("causative('ⲧⲣⲉⲩ', third, plur)")       # make them...

        # Causative with nominal subject: ⲧⲣⲉ- + NOUN + INFINITIVE
        self.prolog.assertz("causative_nominal('ⲧⲣⲉ')")             # tre- + noun

        # PASSIVE/DYNAMIC PASSIVE (§113-114)
        # ===================================
        # Passive expresses "be [verb]ed" or "get [verb]ed"
        # Pattern: Various formations depending on verb type

        # Common passive auxiliary
        self.prolog.assertz("passive_marker('ⲟⲩⲁϩ')")              # ouah- passive marker

        # Reflexive/middle constructions (can have passive meaning)
        self.prolog.assertz("reflexive_marker('ⲙⲙⲓⲛ')")           # mmin- self/reflexive

        print("✓ Causative and passive constructions loaded")

        # Auxiliary verbs (copulas)
        self.prolog.assertz("copula('ⲡⲉ')")          # is (m.sg)
        self.prolog.assertz("copula('ⲧⲉ')")          # is (f.sg)
        self.prolog.assertz("copula('ⲛⲉ')")          # are (pl)

        # ===================================================================
        # COPTIC SYNTACTIC RULES
        # ===================================================================

        # Noun phrase structure rules
        # Valid NP structure: Article + Noun
        self.prolog.assertz("valid_np(Article, Noun) :- definite_article(Article), noun_compatible(Noun)")

        # Helper: Any word can be a noun (simplified)
        self.prolog.assertz("noun_compatible(_)")

        # Definiteness agreement rule - In Coptic, definiteness is marked by articles
        self.prolog.assertz("requires_definiteness(Noun, Article) :- definite_article(Article)")

        # Tripartite nominal sentence pattern
        # Coptic tripartite pattern: Subject - Copula - Predicate
        # Example: ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ (I am God)
        self.prolog.assertz("tripartite_sentence(Subject, Copula, Predicate) :- independent_pronoun(Subject), copula(Copula), noun_compatible(Predicate)")

        # Verbal sentence patterns
        # Verbal sentence: Conjugation + Subject + Verb
        self.prolog.assertz("verbal_sentence(Conj, Subject, Verb) :- conjugation_base(Conj), (independent_pronoun(Subject) ; definite_article(Subject)), verb_compatible(Verb)")

        # Helper: Any word can be a verb (simplified)
        self.prolog.assertz("verb_compatible(_)")

        # ===================================================================
        # DEPENDENCY VALIDATION RULES
        # ===================================================================

        # Validate subject-verb relationship
        self.prolog.assertz("valid_subject_verb(Subject, Verb, SubjPOS, VerbPOS) :- member(SubjPOS, ['PRON', 'NOUN', 'PROPN']), member(VerbPOS, ['VERB', 'AUX'])")

        # Validate determiner-noun relationship
        self.prolog.assertz("valid_det_noun(Det, Noun, DetPOS, NounPOS) :- DetPOS = 'DET', member(NounPOS, ['NOUN', 'PROPN'])")

        # Validate modifier relationships
        self.prolog.assertz("valid_modifier(Head, Modifier, ModPOS) :- member(ModPOS, ['ADJ', 'ADV', 'DET'])")

        # Validate punctuation assignments - content words should NOT be punct
        # Only actual punctuation marks (PUNCT POS tag) should have punct relation
        self.prolog.assertz("invalid_punct(Word, POS, Relation) :- Relation = 'punct', member(POS, ['VERB', 'NOUN', 'PRON', 'PROPN', 'DET', 'ADJ', 'ADV', 'AUX', 'NUM'])")

        # ===================================================================
        # ERROR CORRECTION RULES
        # ===================================================================

        # Suggest correct relation for DET (determiner)
        # DET before NOUN should be 'det' relation
        self.prolog.assertz("suggest_correction('DET', _, 'det')")

        # Suggest correct relation for PRON (pronoun)
        # PRON is typically subject (nsubj), object (obj), or possessive
        self.prolog.assertz("suggest_correction('PRON', 'VERB', 'nsubj')")  # Pronoun before verb = subject
        self.prolog.assertz("suggest_correction('PRON', 'AUX', 'nsubj')")   # Pronoun before aux = subject
        self.prolog.assertz("suggest_correction('PRON', _, 'nsubj')")       # Default for pronoun

        # Suggest correct relation for NOUN
        self.prolog.assertz("suggest_correction('NOUN', 'VERB', 'obj')")    # Noun after verb = object
        self.prolog.assertz("suggest_correction('NOUN', 'AUX', 'nsubj')")   # Noun after copula = predicate nominal
        self.prolog.assertz("suggest_correction('NOUN', _, 'obl')")         # Default for noun

        # Suggest correct relation for VERB
        # Main verbs are often root, ccomp (complement clause), or advcl (adverbial clause)
        self.prolog.assertz("suggest_correction('VERB', 'SCONJ', 'ccomp')") # Verb after subordinator = complement
        self.prolog.assertz("suggest_correction('VERB', 'VERB', 'ccomp')")  # Verb after verb = complement
        self.prolog.assertz("suggest_correction('VERB', _, 'root')")        # Default for verb

        # Suggest correct relation for AUX (auxiliary/copula)
        self.prolog.assertz("suggest_correction('AUX', _, 'cop')")          # Copula relation

        # Suggest correct relation for ADJ (adjective)
        self.prolog.assertz("suggest_correction('ADJ', 'NOUN', 'amod')")    # Adjective modifying noun

        # Suggest correct relation for ADV (adverb)
        self.prolog.assertz("suggest_correction('ADV', _, 'advmod')")       # Adverbial modifier

        # Suggest correct relation for NUM (number)
        self.prolog.assertz("suggest_correction('NUM', 'NOUN', 'nummod')") # Number modifying noun
        self.prolog.assertz("suggest_correction('NUM', _, 'obl')")         # Default for number (temporal/oblique)

        # ===================================================================
        # MORPHOLOGICAL ANALYSIS RULES
        # ===================================================================

        # Clitic attachment patterns
        self.prolog.assertz("has_suffix_pronoun(Word, Base, Suffix) :- atom_concat(Base, Suffix, Word), suffix_pronoun(Suffix), atom_length(Base, BaseLen), BaseLen > 0")

        # Article stripping for lemmatization
        self.prolog.assertz("strip_article(Word, Lemma) :- definite_article(Article), atom_concat(Article, Lemma, Word), atom_length(Lemma, LemmaLen), LemmaLen > 0")

        # If no article found, word is its own lemma
        self.prolog.assertz("strip_article(Word, Word) :- \\+ (definite_article(Article), atom_concat(Article, _, Word))")

        print("✓ Coptic grammatical rules loaded into Prolog")

    # ===================================================================
    # PYTHON INTERFACE METHODS
    # ===================================================================

    def validate_dependency(self, head_word, dep_word, head_pos, dep_pos, relation):
        """
        Validate a dependency relation using Prolog rules

        Args:
            head_word: The head word text
            dep_word: The dependent word text
            head_pos: POS tag of head
            dep_pos: POS tag of dependent
            relation: Dependency relation (nsubj, obj, det, etc.)

        Returns:
            dict: Validation result with status and suggestions
        """
        if not self.prolog_initialized:
            return {"valid": True, "message": "Prolog not available"}

        try:
            result = {"valid": True, "warnings": [], "suggestions": []}

            # Check subject-verb relationships
            if relation in ['nsubj', 'csubj']:
                query = f"valid_subject_verb('{dep_word}', '{head_word}', '{dep_pos}', '{head_pos}')"
                query_result = list(self.prolog.query(query))
                if not query_result:
                    result["warnings"].append(
                        f"Unusual subject-verb: {dep_word} ({dep_pos}) → {head_word} ({head_pos})"
                    )

            # Check determiner-noun relationships
            elif relation == 'det':
                query = f"valid_det_noun('{dep_word}', '{head_word}', '{dep_pos}', '{head_pos}')"
                query_result = list(self.prolog.query(query))
                if not query_result:
                    result["warnings"].append(
                        f"Unusual det-noun: {dep_word} → {head_word}"
                    )

            # Check for incorrect punctuation assignments and suggest corrections
            query = f"invalid_punct('{dep_word}', '{dep_pos}', '{relation}')"
            query_result = list(self.prolog.query(query))
            if query_result:
                # Query for suggested correction
                correction_query = f"suggest_correction('{dep_pos}', '{head_pos}', Suggestion)"
                correction_result = list(self.prolog.query(correction_query))

                if correction_result and 'Suggestion' in correction_result[0]:
                    suggested_rel = correction_result[0]['Suggestion']
                    result["warnings"].append(
                        f"⚠️  PARSER ERROR: '{dep_word}' ({dep_pos}) incorrectly labeled as 'punct' → SUGGESTED: '{suggested_rel}'"
                    )
                    result["suggestions"].append({
                        "word": dep_word,
                        "pos": dep_pos,
                        "incorrect": relation,
                        "suggested": suggested_rel,
                        "head_pos": head_pos
                    })
                else:
                    result["warnings"].append(
                        f"⚠️  PARSER ERROR: '{dep_word}' ({dep_pos}) incorrectly labeled as 'punct' - should be a content relation"
                    )

            return result

        except Exception as e:
            return {"valid": True, "message": f"Validation error: {e}"}

    def check_tripartite_pattern(self, words, pos_tags):
        """
        Check if a sentence follows the Coptic tripartite nominal pattern

        Args:
            words: List of word forms
            pos_tags: List of POS tags

        Returns:
            dict: Pattern analysis results
        """
        if not self.prolog_initialized or len(words) < 3:
            return {"is_tripartite": False}

        try:
            # Check for tripartite pattern: Pronoun - Copula - Noun
            subj, cop, pred = words[0], words[1], words[2]

            query = f"tripartite_sentence('{subj}', '{cop}', '{pred}')"
            query_result = list(self.prolog.query(query))
            is_tripartite = len(query_result) > 0

            return {
                "is_tripartite": is_tripartite,
                "pattern": f"{subj} - {cop} - {pred}" if is_tripartite else None,
                "description": "Tripartite nominal sentence" if is_tripartite else None
            }

        except Exception as e:
            return {"is_tripartite": False, "error": str(e)}

    def analyze_morphology(self, word, use_enhanced=True):
        """
        Analyze word morphology using Prolog rules + enhanced proclitic segmentation

        Args:
            word: Coptic word to analyze
            use_enhanced: Use enhanced morphology analyzer for proclitics (Lessons 11 & 13 fix)

        Returns:
            dict: Morphological analysis with optional segmentation
        """
        if not self.prolog_initialized:
            return {"word": word, "analyzed": False}

        try:
            analysis = {"word": word, "components": []}

            # ENHANCED: Try proclitic segmentation first (solves L11 & L13 bottleneck)
            if use_enhanced and hasattr(self, 'morphology_analyzer'):
                segments = self.morphology_analyzer.segment_word(word)
                if len(segments) > 1:
                    # Multi-token word detected!
                    analysis["segmented"] = True
                    analysis["segments"] = [
                        {
                            "form": seg.form,
                            "lemma": seg.lemma,
                            "pos": seg.pos,
                            "feats": seg.feats
                        }
                        for seg in segments
                    ]
                    return analysis

            # Check for definite article (original Prolog-based)
            article_query = f"strip_article('{word}', Lemma)"
            results = list(self.prolog.query(article_query))
            if results:
                result = results[0]
                if 'Lemma' in result:
                    lemma = result['Lemma']
                    if lemma != word:
                        analysis["has_article"] = True
                        analysis["lemma"] = lemma
                        analysis["article"] = word.replace(lemma, '')

            # Check for suffix pronouns (original Prolog-based)
            suffix_query = f"has_suffix_pronoun('{word}', Base, Suffix)"
            results = list(self.prolog.query(suffix_query))
            if results:
                result = results[0]
                analysis["has_suffix"] = True
                analysis["base"] = result.get('Base')
                analysis["suffix"] = result.get('Suffix')

            return analysis

        except Exception as e:
            return {"word": word, "error": str(e)}

    def validate_parse_tree(self, words, pos_tags, heads, deprels):
        """
        Validate an entire parse tree using Prolog constraints

        Args:
            words: List of word forms
            pos_tags: List of POS tags
            heads: List of head indices
            deprels: List of dependency relations

        Returns:
            dict: Overall validation results with warnings and suggestions
        """
        if not self.prolog_initialized:
            return {"validated": False, "reason": "Prolog not available"}

        try:
            results = {
                "validated": True,
                "warnings": [],
                "suggestions": [],
                "patterns_found": []
            }

            # Check for tripartite pattern (basic assertz-based)
            tripartite = self.check_tripartite_pattern(words, pos_tags)
            if tripartite.get("is_tripartite"):
                results["patterns_found"].append(tripartite)

            # ===================================================================
            # CHECK FOR CIRCUMSTANTIAL PATTERNS
            # ===================================================================

            if len(words) >= 2:
                first_word = words[0]

                # Check for circumstantial with pronominal subject (ⲉⲓ-, ⲉⲕ-, ⲉϥ-, etc.)
                if len(words) >= 2:
                    # Query if first word is circumstantial pronoun + verb pattern
                    query = f"circumstantial_clause('{first_word}', '{words[1]}')"
                    try:
                        circ_results = list(self.prolog.query(query))
                        if circ_results:
                            # Get person/number info
                            info_query = f"circumstantial_pronoun('{first_word}', Person, Number)"
                            info = list(self.prolog.query(info_query))
                            person = info[0].get('Person') if info else 'unknown'
                            number = info[0].get('Number') if info else 'unknown'

                            results["patterns_found"].append({
                                "type": "circumstantial",
                                "description": f"Circumstantial clause (temporal/causal)",
                                "pattern": f"{first_word}-{words[1]}",
                                "converter": first_word,
                                "person": person,
                                "number": number,
                                "meaning": "when/while",
                            })
                    except Exception as e:
                        pass  # Query failed, not a circumstantial

                # Check for circumstantial with nominal subject (ⲉⲣⲉ- + noun + verb)
                if first_word == 'ⲉⲣⲉ' and len(words) >= 3:
                    query = f"circumstantial_nominal_clause('{first_word}', '{words[1]}', '{words[2]}')"
                    try:
                        if list(self.prolog.query(query)):
                            results["patterns_found"].append({
                                "type": "circumstantial_nominal",
                                "description": "Circumstantial with nominal subject",
                                "pattern": f"{first_word} {words[1]} {words[2]}...",
                                "converter": "ⲉⲣⲉ",
                                "subject": words[1],
                                "verb": words[2],
                                "meaning": "when/while [noun] [verbs]",
                            })
                    except Exception as e:
                        pass

                # Check for circumstantial of preterit (ⲉⲁϥⲥⲱⲧⲙ "when he heard")
                if first_word == 'ⲉ' and len(words) >= 4:
                    if words[1] == 'ⲁ':  # Preterit marker
                        query = f"circumstantial_preterit('{words[0]}', '{words[1]}', '{words[2]}', '{words[3]}')"
                        try:
                            if list(self.prolog.query(query)):
                                results["patterns_found"].append({
                                    "type": "circumstantial_preterit",
                                    "description": "Circumstantial of preterit (nested)",
                                    "pattern": f"{words[0]}-{words[1]}-{words[2]}-{words[3]}",
                                    "meaning": "when [subject] [past verb]",
                                    "note": "Nested construction: circumstantial + preterit",
                                    })
                        except Exception as e:
                            pass

                # Check for negative circumstantial (ⲉⲛ-, ⲉⲙⲡ-)
                if first_word in ['ⲉⲛ', 'ⲉⲙⲡ']:
                    # Check if sentence ends with ⲁⲛ (negative marker)
                    if 'ⲁⲛ' in words:
                        results["patterns_found"].append({
                            "type": "negative_circumstantial",
                            "description": "Negative circumstantial clause",
                            "pattern": f"{first_word}-...-ⲁⲛ",
                            "converter": first_word,
                            "meaning": "when/while not",
                        })

            # ===================================================================
            # CHECK FOR RELATIVE CLAUSE PATTERNS
            # ===================================================================

            # Look for relative converters anywhere in the sentence
            # (relative clauses modify a preceding noun)
            for i, word in enumerate(words):
                # Check for basic relative converter (ⲉⲛⲧ, ⲉⲧ)
                if word in ['ⲉⲛⲧ', 'ⲉⲧ']:
                    if i > 0 and i < len(words) - 1:  # Must have head noun before and verb after
                        head_noun = words[i-1]
                        following_word = words[i+1]

                        query = f"relative_clause('{head_noun}', '{word}', '{following_word}')"
                        try:
                            if list(self.prolog.query(query)):
                                results["patterns_found"].append({
                                    "type": "relative_clause",
                                    "description": "Relative clause modifying noun",
                                    "pattern": f"{head_noun} {word} {following_word}...",
                                    "head": head_noun,
                                    "converter": word,
                                    "meaning": "the [noun] who/which/that...",
                                    "note": "Converter signals: 'modified by following complete statement'",
                                })
                        except Exception as e:
                            pass

                    # Check for substantivized relative (article + converter)
                    # Example: ⲧⲉⲛⲧ = "the one (fem) who"
                    elif i == 0 and len(words) >= 2:
                        query = f"substantivized_relative('{word}', '{words[i+1]}')"
                        try:
                            if list(self.prolog.query(query)):
                                results["patterns_found"].append({
                                    "type": "substantivized_relative",
                                    "description": "Substantivized relative (article as head)",
                                    "pattern": f"{word} {words[i+1]}...",
                                    "meaning": "the one who/which...",
                                    "note": "Article alone functions as head noun",
                                })
                        except Exception as e:
                            pass

                # Check for compound relative-preterit forms (ⲉⲛⲧⲁϥ, ⲉⲧⲁϥ, etc.)
                # These combine: relative converter + preterit + pronoun
                if i > 0 and i < len(words) - 1:
                    head_noun = words[i-1]
                    query = f"relative_preterit_compound('{word}', Person, Number)"
                    try:
                        compound_results = list(self.prolog.query(query))
                        if compound_results and len(words) > i + 1:
                            person = compound_results[0].get('Person', 'unknown')
                            number = compound_results[0].get('Number', 'unknown')

                            # Check if follows a noun
                            clause_query = f"relative_preterit_clause('{head_noun}', '{word}', '{words[i+1]}')"
                            if list(self.prolog.query(clause_query)):
                                results["patterns_found"].append({
                                    "type": "relative_preterit",
                                    "description": "Relative clause with preterit (past action)",
                                    "pattern": f"{head_noun} {word} {words[i+1]}...",
                                    "head": head_noun,
                                    "compound": word,
                                    "person": person,
                                    "number": number,
                                    "meaning": "the [noun] who [did]...",
                                    "note": "Compound form: relative+preterit+pronoun",
                                })
                    except Exception as e:
                        pass

                # Check for negative relative (ⲉⲧⲉ...ⲁⲛ)
                if word == 'ⲉⲧⲉ' and 'ⲁⲛ' in words[i:]:
                    if i > 0:
                        head_noun = words[i-1]
                        results["patterns_found"].append({
                            "type": "negative_relative",
                            "description": "Negative relative clause",
                            "pattern": f"{head_noun} ⲉⲧⲉ...ⲁⲛ",
                            "head": head_noun,
                            "converter": "ⲉⲧⲉ",
                            "meaning": "the [noun] who/which does not...",
                        })

            # ===================================================================
            # CHECK FOR CONDITIONAL SENTENCE PATTERNS
            # ===================================================================

            for i, word in enumerate(words):
                # TYPE 1: Presupposed/Possible Fact (§150)
                # Markers: ⲉⲛⲉⲓ, ⲉⲛⲉⲓⲇⲏ, ⲉϣⲱⲡⲉ, etc.
                query = f"conditional_presupposed('{word}')"
                try:
                    if list(self.prolog.query(query)):
                        results["patterns_found"].append({
                            "type": "conditional_presupposed",
                            "description": "Conditional: presupposed/possible fact",
                            "pattern": f"{word} [if-clause]...",
                            "marker": word,
                            "meaning": "since/if X is true, then Y is true",
                            "note": "Expresses presupposed or possible fact",
                        })
                except Exception as e:
                    pass

                # TYPE 2: Generalization (§151)
                # Markers: ⲉϣⲱⲡⲉ, ⲉⲣϣⲁⲛ, ⲕⲁⲛ
                query = f"conditional_generalization('{word}')"
                try:
                    if list(self.prolog.query(query)):
                        # Check if there's a then-clause marker (ⲛⲁ, ϣⲁ) in the sentence
                        has_then = any(w in ['ⲛⲁ', 'ϣⲁ'] for w in words[i:])
                        results["patterns_found"].append({
                            "type": "conditional_generalization",
                            "description": "Conditional: generalization",
                            "pattern": f"{word} [if ever]... → [then]...",
                            "marker": word,
                            "meaning": "if ever/whenever X, then Y will be",
                            "has_then_marker": has_then,
                            "note": "Expresses general truth or habitual action",
                        })
                except Exception as e:
                    pass

                # TYPE 3a: Contrary to Fact - PRESENT (§152)
                # If-clause: ⲉⲛⲉⲣⲉ, ⲉⲛⲉ
                query = f"contrary_to_fact_present('{word}')"
                try:
                    if list(self.prolog.query(query)):
                        # Look for then-clause marker (ⲛⲁ, ⲛⲉ, ⲛⲉⲣⲉ)
                        then_markers = [w for w in words[i:] if w in ['ⲛⲁ', 'ⲛⲉ', 'ⲛⲉⲣⲉ']]
                        results["patterns_found"].append({
                            "type": "contrary_to_fact_present",
                            "description": "Conditional: contrary to fact (present)",
                            "pattern": f"{word} [if were]... → ⲛⲁ/ⲛⲉ [would]...",
                            "if_marker": word,
                            "then_markers": then_markers if then_markers else None,
                            "meaning": "if X were true (but isn't), then Y would be",
                            "note": "Present tense counterfactual",
                        })
                except Exception as e:
                    pass

                # TYPE 3b: Contrary to Fact - PAST (§152)
                # If-clause: ⲉⲛⲉⲛⲧⲁ (aff), ⲉⲛⲉⲙⲡⲉ (neg)
                if word in ['ⲉⲛⲉⲛⲧⲁ', 'ⲉⲛⲉⲙⲡⲉ']:
                    query_type = "contrary_to_fact_past_aff" if word == 'ⲉⲛⲉⲛⲧⲁ' else "contrary_to_fact_past_neg"
                    query = f"{query_type}('{word}')"
                    try:
                        if list(self.prolog.query(query)):
                            # Look for then-clause marker (ⲉϣϫⲛⲉ, ⲉϣϫⲉ, ⲛⲉⲉⲓϣⲡⲉ)
                            then_markers = [w for w in words[i:] if w in ['ⲉϣϫⲛⲉ', 'ⲉϣϫⲉ', 'ⲛⲉⲉⲓϣⲡⲉ']]
                            polarity = "affirmative" if word == 'ⲉⲛⲉⲛⲧⲁ' else "negative"
                            results["patterns_found"].append({
                                "type": "contrary_to_fact_past",
                                "description": f"Conditional: contrary to fact - past ({polarity})",
                                "pattern": f"{word} [if had]... → ⲉϣϫⲛⲉ [would have]...",
                                "if_marker": word,
                                "polarity": polarity,
                                "then_markers": then_markers if then_markers else None,
                                "meaning": "if X had been true (but wasn't), Y would have been",
                                "note": "Past tense counterfactual",
                                })
                    except Exception as e:
                        pass

            # ===================================================================
            # CHECK FOR NON-DURATIVE CONJUGATION PATTERNS
            # ===================================================================

            for i, word in enumerate(words):
                # 1. PAST AFFIRMATIVE (ⲁϥ-, ⲁⲥ-, etc.) - Most common!
                query = f"past_affirmative('{word}', Person, Number)"
                try:
                    results_past = list(self.prolog.query(query))
                    if results_past and i < len(words) - 1:
                        person = results_past[0].get('Person', 'unknown')
                        number = results_past[0].get('Number', 'unknown')
                        verb = words[i+1] if i+1 < len(words) else None

                        results["patterns_found"].append({
                            "type": "past_affirmative",
                            "description": "Past/Preterit conjugation (affirmative)",
                            "pattern": f"{word} {verb}..." if verb else f"{word}...",
                            "conjugation": word,
                            "person": person,
                            "number": number,
                            "meaning": "past narration OR present perfect",
                            "example": "ⲁϥⲃⲱⲕ = 'he went' or 'he has gone'",
                        })
                except Exception as e:
                    pass

                # 2. PAST NEGATIVE (ⲙⲡⲉϥ-, ⲙⲡⲉⲥ-, etc.)
                query = f"past_negative('{word}', Person, Number)"
                try:
                    results_neg = list(self.prolog.query(query))
                    if results_neg and i < len(words) - 1:
                        person = results_neg[0].get('Person', 'unknown')
                        number = results_neg[0].get('Number', 'unknown')

                        results["patterns_found"].append({
                            "type": "past_negative",
                            "description": "Past/Preterit conjugation (negative)",
                            "pattern": f"{word} [verb]...",
                            "conjugation": word,
                            "person": person,
                            "number": number,
                            "meaning": "did not / has not",
                        })
                except Exception as e:
                    pass

                # 3. 'NOT YET' (ⲙⲡⲁⲧⲉ-, etc.)
                query = f"not_yet('{word}', Person, Number)"
                try:
                    results_notyet = list(self.prolog.query(query))
                    if results_notyet:
                        person = results_notyet[0].get('Person', 'unknown')
                        number = results_notyet[0].get('Number', 'unknown')

                        results["patterns_found"].append({
                            "type": "not_yet",
                            "description": "'Not yet' aspect (with expectation)",
                            "pattern": f"{word} [verb]...",
                            "conjugation": word,
                            "person": person,
                            "number": number,
                            "meaning": "has not yet... (but might/will)",
                            "example": "ⲙⲡⲁⲧⲉⲧⲁⲟⲩⲛⲟⲩⲉⲓ = 'my hour has not yet come'",
                        })
                except Exception as e:
                    pass

                # 4. AORIST AFFIRMATIVE (ϣⲁϥ-, ϣⲁⲥ-, etc.) - Unique Coptic feature!
                query = f"aorist_affirmative('{word}', Person, Number)"
                try:
                    results_aorist = list(self.prolog.query(query))
                    if results_aorist:
                        person = results_aorist[0].get('Person', 'unknown')
                        number = results_aorist[0].get('Number', 'unknown')

                        results["patterns_found"].append({
                            "type": "aorist_affirmative",
                            "description": "Aorist (tenseless/timeless)",
                            "pattern": f"{word} [verb]...",
                            "conjugation": word,
                            "person": person,
                            "number": number,
                            "meaning": "tenseless - timeless truth OR past narration",
                            "note": "Distinctly Coptic device - no English equivalent!",
                            "example": "ϣⲁⲣⲉⲟⲩϣⲏⲣⲉ ⲛⲥⲟⲫⲟⲥ ⲉⲩⲫⲣⲁⲛⲉ ⲙⲡⲉϥⲉⲓⲱⲧ = 'a wise son makes his father glad'",
                        })
                except Exception as e:
                    pass

                # 5. AORIST NEGATIVE (ⲙⲉϥ-, ⲙⲉⲥ-, etc.)
                query = f"aorist_negative('{word}', Person, Number)"
                try:
                    results_aorist_neg = list(self.prolog.query(query))
                    if results_aorist_neg:
                        person = results_aorist_neg[0].get('Person', 'unknown')
                        number = results_aorist_neg[0].get('Number', 'unknown')

                        results["patterns_found"].append({
                            "type": "aorist_negative",
                            "description": "Aorist negative (tenseless)",
                            "pattern": f"{word} [verb]...",
                            "conjugation": word,
                            "person": person,
                            "number": number,
                            "meaning": "does not / did not (tenseless)",
                        })
                except Exception as e:
                    pass

                # 6. OPTATIVE (ⲉⲣⲉ-, ⲛⲛⲉ-)
                if word in ['ⲉⲣⲉ', 'ⲛⲛⲉ']:
                    polarity = "affirmative" if word == 'ⲉⲣⲉ' else "negative"
                    results["patterns_found"].append({
                        "type": "optative",
                        "description": f"Optative mood ({polarity})",
                        "pattern": f"{word} [subject] [verb]...",
                        "marker": word,
                        "meaning": "shall / might",
                    })

                # 7. JUSSIVE (ⲙⲁⲣⲉ-, ⲙⲡⲣⲧⲣⲉ-)
                if word in ['ⲙⲁⲣⲉ', 'ⲙⲡⲣⲧⲣⲉ']:
                    polarity = "affirmative" if word == 'ⲙⲁⲣⲉ' else "negative"
                    results["patterns_found"].append({
                        "type": "jussive",
                        "description": f"Jussive mood ({polarity})",
                        "pattern": f"{word} [subject] [verb]...",
                        "marker": word,
                        "meaning": "let him... / ought to...",
                    })

            # ===================================================================
            # DURATIVE, INFINITIVE, STATIVE DETECTION
            # ===================================================================
            # Check for durative (present tense) patterns
            for i, word in enumerate(words):
                # 1. DURATIVE PRESENT (ϥ-, ⲥ-, ϯ-, etc. + infinitive)
                query = f"durative_present('{word}', Person, Number)"
                try:
                    results_durative = list(self.prolog.query(query))
                    if results_durative:
                        person = results_durative[0].get('Person', 'unknown')
                        number = results_durative[0].get('Number', 'unknown')

                        results["patterns_found"].append({
                            "type": "durative_present",
                            "description": "Durative/Present tense",
                            "pattern": f"{word} [infinitive]...",
                            "conjugation": word,
                            "person": person,
                            "number": number,
                            "meaning": "does / is doing (present ongoing action)",
                            "example": "ϥⲥⲱⲧⲙ = 'he hears/is hearing'",
                        })
                except Exception as e:
                    pass

                # 2. DURATIVE NOMINAL (ⲉⲣⲉ- + noun + infinitive)
                query = f"durative_nominal_marker('{word}')"
                try:
                    results_durative_nom = list(self.prolog.query(query))
                    if results_durative_nom and i + 2 < len(words):
                        results["patterns_found"].append({
                            "type": "durative_nominal",
                            "description": "Durative with nominal subject",
                            "pattern": f"{word} [noun] [infinitive]...",
                            "marker": word,
                            "meaning": "X does / is doing",
                            "example": "ⲉⲣⲉⲡⲣⲱⲙⲉⲥⲱⲧⲙ = 'the man hears'",
                        })
                except Exception as e:
                    pass

                # 3. INFINITIVE (verbal noun)
                query = f"infinitive('{word}')"
                try:
                    results_inf = list(self.prolog.query(query))
                    if results_inf:
                        results["patterns_found"].append({
                            "type": "infinitive",
                            "description": "Infinitive (verbal noun)",
                            "pattern": word,
                            "infinitive": word,
                            "meaning": "to [verb] / [verb]-ing",
                            "note": "Functions as a noun",
                        })
                except Exception as e:
                    pass

                # 4. STATIVE (resultant state)
                query = f"stative('{word}')"
                try:
                    results_stat = list(self.prolog.query(query))
                    if results_stat:
                        results["patterns_found"].append({
                            "type": "stative",
                            "description": "Stative (resultant state)",
                            "pattern": f"[subject] {word}",
                            "stative": word,
                            "meaning": "be in state of [verb]ed",
                            "note": "Expresses resultant state (like perfect or passive)",
                            "example": "ϥⲙⲟⲩⲧ = 'he is dead'",
                        })
                except Exception as e:
                    pass

            # ===================================================================
            # FOCALIZING CONVERSION DETECTION
            # ===================================================================
            # Check for focalizing (cleft sentence) patterns
            for i, word in enumerate(words):
                # 1. FOCUS COPULA (ⲡⲉ/ⲧⲉ/ⲛⲉ in focusing function)
                query = f"focus_copula('{word}', Gender, Number)"
                try:
                    results_focus = list(self.prolog.query(query))
                    if results_focus and i + 1 < len(words):
                        gender = results_focus[0].get('Gender', 'unknown')
                        number = results_focus[0].get('Number', 'unknown')

                        # Check if followed by relative converter (ⲉⲛⲧ/ⲉⲧ)
                        next_word = words[i + 1] if i + 1 < len(words) else ""
                        is_relative = next_word in ['ⲉⲛⲧ', 'ⲉⲧ', 'ⲉⲛⲧⲁ', 'ⲉⲧⲁ']

                        if is_relative:
                            results["patterns_found"].append({
                                "type": "focalizing_cleft",
                                "description": "Focalizing/Cleft sentence",
                                "pattern": f"[focused_element] {word} {next_word} [clause]...",
                                "copula": word,
                                "gender": gender,
                                "number": number,
                                "meaning": "It is X that... / X is the one who...",
                                "note": "Emphasizes a particular constituent",
                                "example": "ⲁⲛⲟⲕ ⲡⲉ ⲡⲉⲛⲧⲁϥⲉⲓ = 'It is I who came'",
                            })
                except Exception as e:
                    pass

                # 2. FOCALIZING MARKER (ⲛⲧⲟϥ/ⲛⲧⲟⲥ/ⲁⲛⲟⲕ emphatic)
                query = f"focalizing_marker('{word}')"
                try:
                    results_foc_marker = list(self.prolog.query(query))
                    if results_foc_marker:
                        results["patterns_found"].append({
                            "type": "focalizing_marker",
                            "description": "Emphatic pronoun (focalizing)",
                            "pattern": f"{word} [copula] ...",
                            "marker": word,
                            "meaning": "It is he/she/I (emphatic focus)",
                        })
                except Exception as e:
                    pass

                # 3. SECOND TENSE (ⲛⲧⲁϥ- focuses on action)
                query = f"second_tense('{word}', Person, Number)"
                try:
                    results_second = list(self.prolog.query(query))
                    if results_second:
                        person = results_second[0].get('Person', 'unknown')
                        number = results_second[0].get('Number', 'unknown')

                        results["patterns_found"].append({
                            "type": "second_tense",
                            "description": "Second tense (action focus)",
                            "pattern": f"{word} [verb]...",
                            "conjugation": word,
                            "person": person,
                            "number": number,
                            "meaning": "It was [subject] who [did]...",
                            "note": "Focuses on the ACTION, not the subject",
                            "example": "ⲛⲧⲁϥⲉⲓ = '(it was that) he came' (emphasis on coming)",
                        })
                except Exception as e:
                    pass

            # ===================================================================
            # IMPERATIVE DETECTION
            # ===================================================================
            # Check for imperative patterns
            for i, word in enumerate(words):
                # 1. AFFIRMATIVE IMPERATIVE (ⲁⲣⲓ-)
                query = f"imperative_affirmative('{word}')"
                try:
                    results_imp_aff = list(self.prolog.query(query))
                    if results_imp_aff:
                        # Check if has person/number info
                        if len(results_imp_aff[0]) > 0:
                            person = results_imp_aff[0].get('Person', 'second')
                            number = results_imp_aff[0].get('Number', 'any')
                        else:
                            person = 'second'
                            number = 'any'

                        results["patterns_found"].append({
                            "type": "imperative_affirmative",
                            "description": "Affirmative imperative (command)",
                            "pattern": f"{word} [infinitive]...",
                            "marker": word,
                            "person": person,
                            "number": number,
                            "meaning": "Do [verb]!",
                            "example": "ⲁⲣⲓⲡⲓⲥⲧⲉⲩⲉ = 'Believe!'",
                        })
                except Exception as e:
                    pass

                # 2. NEGATIVE IMPERATIVE/PROHIBITION (ⲙⲡⲣ-)
                query = f"imperative_negative('{word}')"
                try:
                    results_imp_neg = list(self.prolog.query(query))
                    if results_imp_neg:
                        # Check if has person/number info
                        if len(results_imp_neg[0]) > 0:
                            person = results_imp_neg[0].get('Person', 'second')
                            number = results_imp_neg[0].get('Number', 'any')
                        else:
                            person = 'second'
                            number = 'any'

                        results["patterns_found"].append({
                            "type": "imperative_negative",
                            "description": "Negative imperative (prohibition)",
                            "pattern": f"{word} [infinitive]...",
                            "marker": word,
                            "person": person,
                            "number": number,
                            "meaning": "Do not [verb]!",
                            "example": "ⲙⲡⲣⲕⲁⲁⲧ = 'Do not leave (it)!'",
                        })
                except Exception as e:
                    pass

                # 3. SIMPLE IMPERATIVE (bare verb as command)
                query = f"imperative_simple('{word}')"
                try:
                    results_imp_simple = list(self.prolog.query(query))
                    if results_imp_simple:
                        results["patterns_found"].append({
                            "type": "imperative_simple",
                            "description": "Simple imperative (bare verb)",
                            "pattern": word,
                            "verb": word,
                            "meaning": "[Verb]! (direct command)",
                            "example": "ⲁⲙⲟⲩ = 'Come!' or ⲃⲱⲕ = 'Go!'",
                        })
                except Exception as e:
                    pass

            # ===================================================================
            # CAUSATIVE AND PASSIVE DETECTION
            # ===================================================================
            # Check for causative and passive patterns
            for i, word in enumerate(words):
                # 1. CAUSATIVE (ⲧⲣⲉ- cause/make)
                query = f"causative('{word}')"
                try:
                    results_caus = list(self.prolog.query(query))
                    if results_caus:
                        # Check if has person/number info
                        if len(results_caus[0]) > 0:
                            person = results_caus[0].get('Person', 'any')
                            number = results_caus[0].get('Number', 'any')
                        else:
                            person = 'any'
                            number = 'any'

                        results["patterns_found"].append({
                            "type": "causative",
                            "description": "Causative construction",
                            "pattern": f"{word} [subject/object] [infinitive]...",
                            "marker": word,
                            "person": person,
                            "number": number,
                            "meaning": "cause [X] to [verb] / make [X] [verb]",
                            "note": "Expresses causation - making someone do something",
                            "example": "ⲧⲣⲉϥⲙⲟⲩ = 'cause him to die' or 'kill him'",
                        })
                except Exception as e:
                    pass

                # 2. CAUSATIVE NOMINAL (ⲧⲣⲉ- + noun)
                query = f"causative_nominal('{word}')"
                try:
                    results_caus_nom = list(self.prolog.query(query))
                    if results_caus_nom and i + 1 < len(words):
                        results["patterns_found"].append({
                            "type": "causative_nominal",
                            "description": "Causative with nominal subject",
                            "pattern": f"{word} [noun] [infinitive]...",
                            "marker": word,
                            "meaning": "cause [noun] to [verb]",
                            "example": "ⲧⲣⲉⲡⲣⲱⲙⲉⲙⲟⲩ = 'cause the man to die'",
                        })
                except Exception as e:
                    pass

                # 3. PASSIVE MARKER
                query = f"passive_marker('{word}')"
                try:
                    results_pass = list(self.prolog.query(query))
                    if results_pass:
                        results["patterns_found"].append({
                            "type": "passive",
                            "description": "Passive construction",
                            "pattern": f"{word} [verb/participle]...",
                            "marker": word,
                            "meaning": "be [verb]ed / get [verb]ed",
                            "note": "Dynamic passive - expresses action happening to subject",
                        })
                except Exception as e:
                    pass

            # NOTE: DCG validation removed - validate_parse_tree/4 predicate not implemented
            # The grammar file (coptic_grammar.pl) contains dependency patterns, not DCG rules
            # Individual pattern validation (tripartite, causative, etc.) provides comprehensive coverage
            #
            # if hasattr(self, 'dcg_loaded') and self.dcg_loaded:
            #     try:
            #         dcg_results = self._validate_with_dcg(words, pos_tags, heads, deprels)
            #         if dcg_results and isinstance(dcg_results, dict):
            #             # Merge DCG results
            #             if "patterns_found" in dcg_results and dcg_results["patterns_found"]:
            #                 results["patterns_found"].extend(dcg_results["patterns_found"])
            #             if "warnings" in dcg_results and dcg_results["warnings"]:
            #                 results["warnings"].extend(dcg_results["warnings"])
            #     except Exception as e:
            #         print(f"Warning: DCG validation failed: {e}")
            #         # Continue with basic validation even if DCG fails

            # Validate each dependency (existing validation)
            for i, (word, pos, head, rel) in enumerate(zip(words, pos_tags, heads, deprels)):
                if head > 0 and head <= len(words):  # Not root
                    head_word = words[head - 1]
                    head_pos = pos_tags[head - 1]

                    validation = self.validate_dependency(head_word, word, head_pos, pos, rel)
                    if validation.get("warnings"):
                        results["warnings"].extend(validation["warnings"])

            return results

        except Exception as e:
            return {"validated": False, "error": str(e)}

    def _validate_with_dcg(self, words, pos_tags, heads, deprels):
        """
        Validate parse tree using DCG grammar rules

        Args:
            words: List of word tokens
            pos_tags: List of POS tags
            heads: List of head indices
            deprels: List of dependency relations

        Returns:
            dict: DCG validation results
        """
        try:
            # Convert Python lists to Prolog format
            words_pl = self._list_to_prolog_atoms(words)
            pos_pl = self._list_to_prolog_atoms(pos_tags)
            heads_pl = '[' + ','.join(map(str, heads)) + ']'
            deprels_pl = self._list_to_prolog_atoms(deprels)

            # Query the DCG validation predicate
            query = f"coptic_grammar:validate_parse_tree({words_pl}, {pos_pl}, {heads_pl}, {deprels_pl})"

            # Execute query - it asserts patterns and warnings
            list(self.prolog.query(query))

            # Retrieve patterns
            patterns = []
            pattern_query = "coptic_grammar:pattern_found(P)"
            try:
                for result in self.prolog.query(pattern_query):
                    if isinstance(result, dict) and 'P' in result:
                        pattern_data = result.get('P')
                        if pattern_data:
                            formatted = self._format_prolog_term(pattern_data)
                            patterns.append(formatted)
            except Exception as e:
                print(f"Warning: Error retrieving patterns: {e}")

            # Retrieve warnings
            warnings = []
            warning_query = "coptic_grammar:warning(W)"
            try:
                for result in self.prolog.query(warning_query):
                    if isinstance(result, dict) and 'W' in result:
                        warning_data = result.get('W')
                        if warning_data:
                            formatted = self._format_prolog_term(warning_data)
                            warnings.append(formatted)
            except Exception as e:
                print(f"Warning: Error retrieving warnings: {e}")

            # Clean up dynamic predicates
            try:
                list(self.prolog.query("coptic_grammar:retractall(pattern_found(_))"))
                list(self.prolog.query("coptic_grammar:retractall(warning(_))"))
            except Exception as e:
                print(f"Warning: Error cleaning up Prolog predicates: {e}")

            return {
                "patterns_found": patterns,
                "warnings": warnings
            }

        except Exception as e:
            print(f"DCG validation error: {e}")
            import traceback
            traceback.print_exc()
            return {
                "patterns_found": [],
                "warnings": []
            }

    def _list_to_prolog_atoms(self, python_list):
        """
        Convert Python list of strings to Prolog list with properly quoted atoms

        Args:
            python_list: Python list of strings

        Returns:
            str: Prolog list syntax
        """
        if not python_list:
            return "[]"

        # Quote and escape each string
        items = []
        for item in python_list:
            # Escape single quotes
            escaped = str(item).replace("'", "\\'")
            items.append(f"'{escaped}'")

        return '[' + ','.join(items) + ']'

    def _format_prolog_term(self, term):
        """
        Format a Prolog term for Python display

        Args:
            term: Prolog term (can be atom, list, or compound)

        Returns:
            dict: Formatted representation (always a dict)
        """
        if isinstance(term, list):
            result = {}
            for item in term:
                if hasattr(item, 'name') and hasattr(item, 'args'):
                    # Compound term like pattern_name('...')
                    key = item.name
                    value = item.args[0] if len(item.args) > 0 else None
                    result[key] = str(value) if value is not None else ''
            return result if result else {'data': str(term)}
        elif isinstance(term, str):
            # Simple string/atom - wrap in dict
            return {'type': term, 'data': term}
        else:
            # Other types - convert to string and wrap
            return {'data': str(term)}

    def query_prolog(self, query_string):
        """
        Direct Prolog query interface for custom queries

        Args:
            query_string: Prolog query as string

        Returns:
            Query result or None
        """
        if not self.prolog_initialized:
            return None

        try:
            results = list(self.prolog.query(query_string))
            return results[0] if results else None
        except Exception as e:
            print(f"Prolog query error: {e}")
            return None

    def cleanup(self):
        """
        Cleanup Prolog engine and threads properly
        """
        if self.prolog_initialized and self.prolog is not None:
            try:
                # Try to properly halt the Prolog engine
                # This attempts to stop all Prolog threads
                try:
                    # Query halt to stop Prolog cleanly
                    list(self.prolog.query("halt"))
                except:
                    # halt will raise an exception as Prolog stops, which is expected
                    pass

                # Clean up the Prolog instance
                self.prolog = None
                self.prolog_initialized = False
                print("✓ Prolog engine cleaned up successfully")
            except Exception as e:
                print(f"Warning: Error during Prolog cleanup: {e}")


# ===================================================================
# CONVENIENCE FUNCTIONS
# ===================================================================

def create_prolog_engine():
    """Factory function to create and initialize Prolog engine"""
    return CopticPrologRules()


# ===================================================================
# EXAMPLE USAGE
# ===================================================================

if __name__ == "__main__":
    print("="*70)
    print("Coptic Prolog Rules - Test Suite")
    print("="*70)

    # Initialize engine
    prolog = create_prolog_engine()

    if not prolog.prolog_initialized:
        print("\n⚠️  Prolog not available. Cannot run tests.")
        exit(1)

    print("\n" + "="*70)
    print("TEST 1: Tripartite Pattern Recognition")
    print("="*70)

    # Test tripartite sentence: ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ (I am God)
    words = ['ⲁⲛⲟⲕ', 'ⲡⲉ', 'ⲡⲛⲟⲩⲧⲉ']
    pos_tags = ['PRON', 'AUX', 'NOUN']

    result = prolog.check_tripartite_pattern(words, pos_tags)
    print(f"\nInput: {' '.join(words)}")
    print(f"Result: {result}")

    print("\n" + "="*70)
    print("TEST 2: Morphological Analysis")
    print("="*70)

    # Test article stripping
    test_words = ['ⲡⲛⲟⲩⲧⲉ', 'ⲧⲃⲁϣⲟⲣ', 'ⲛⲣⲱⲙⲉ']
    for word in test_words:
        analysis = prolog.analyze_morphology(word)
        print(f"\nWord: {word}")
        print(f"Analysis: {analysis}")

    print("\n" + "="*70)
    print("TEST 3: Dependency Validation")
    print("="*70)

    # Test subject-verb relationship
    validation = prolog.validate_dependency(
        head_word='ⲡⲉ',
        dep_word='ⲁⲛⲟⲕ',
        head_pos='AUX',
        dep_pos='PRON',
        relation='nsubj'
    )
    print(f"\nDependency: ⲁⲛⲟⲕ (PRON) --nsubj--> ⲡⲉ (AUX)")
    print(f"Validation: {validation}")

    print("\n" + "="*70)
    print("TEST 4: Custom Prolog Query")
    print("="*70)

    # Test custom query
    result = prolog.query_prolog("definite_article(X)")
    print(f"\nQuery: definite_article(X)")
    print(f"Result: {result}")

    print("\n" + "="*70)
    print("All tests completed!")
    print("="*70)
