#!/usr/bin/env python3
"""
Coptic Prolog Rules - Neural-Symbolic Integration
==================================================

Integrates Prolog logic programming with neural dependency parsing
to enhance parsing accuracy through explicit grammatical rules.

Uses janus (SWI-Prolog Python interface) for bidirectional integration.

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

    def _load_coptic_grammar(self):
        """Load Coptic linguistic rules into Prolog"""

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

    def analyze_morphology(self, word):
        """
        Analyze word morphology using Prolog rules

        Args:
            word: Coptic word to analyze

        Returns:
            dict: Morphological analysis
        """
        if not self.prolog_initialized:
            return {"word": word, "analyzed": False}

        try:
            analysis = {"word": word, "components": []}

            # Check for definite article
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

            # Check for suffix pronouns
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

            # Check for tripartite pattern
            tripartite = self.check_tripartite_pattern(words, pos_tags)
            if tripartite.get("is_tripartite"):
                results["patterns_found"].append(tripartite)

            # Validate each dependency
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
