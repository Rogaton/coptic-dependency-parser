#!/usr/bin/env python3
"""
Coptic Dependency Tree Builder
===============================

Builds Universal Dependencies trees from Coptic text.

Key features:
- Uses morphology analyzer to segment proclitics
- Implements UD attachment algorithms
- Follows Coptic UD Guidelines v1.1.0

Example:
    builder = CopticTreeBuilder()
    tree = builder.build_tree(["ⲁϥⲃⲱⲕ"])
    print(tree.to_ascii_tree())
"""

from typing import List, Optional
from coptic_tree_structures import Token, MultiToken, DependencyTree
from coptic_morphology import CopticMorphologyAnalyzer, Segment


class CopticTreeBuilder:
    """
    Builds dependency trees from tokenized Coptic text.

    Follows the lexico-centric approach from Coptic UD Guidelines:
    - Lexical items are heads
    - Conjugation bases are auxiliaries
    - Prepositions are case markers
    - Infinitive is the verbal root
    """

    def __init__(self, prolog_engine=None):
        """
        Initialize tree builder.

        Args:
            prolog_engine: Optional Prolog engine for enhanced analysis
        """
        self.prolog = prolog_engine
        self.morph_analyzer = CopticMorphologyAnalyzer(prolog_engine)

    def build_tree(self, words: List[str], pos_tags: Optional[List[str]] = None) -> DependencyTree:
        """
        Build dependency tree from words.

        Args:
            words: List of word forms (may be fused forms like ⲁϥⲃⲱⲕ)
            pos_tags: Optional POS tags (for future use)

        Returns:
            DependencyTree object

        Example:
            >>> builder = CopticTreeBuilder()
            >>> tree = builder.build_tree(["ⲁϥⲃⲱⲕ"])
            >>> print(tree.to_ascii_tree())
            ⲃⲱⲕ (root)
            ├── ⲁ (aux)
            └── ϥ (nsubj)
        """
        # Step 1: Preprocess - segment proclitics
        tokens, multitokens = self._preprocess(words, pos_tags)

        # Step 2: Find root
        root_idx = self._find_root(tokens)
        if root_idx is not None:
            tokens[root_idx].head = 0
            tokens[root_idx].deprel = "root"
        else:
            # Fallback: make first token root
            tokens[0].head = 0
            tokens[0].deprel = "root"
            root_idx = 0

        # Step 3: Attach dependents (order matters!)
        self._attach_auxiliaries(tokens, root_idx)
        self._attach_subjects(tokens, root_idx)
        self._attach_objects(tokens, root_idx)
        self._attach_converters(tokens, root_idx)
        self._attach_case_markers(tokens)
        self._attach_modifiers(tokens, root_idx)

        # Step 4: Attach any remaining unattached tokens to root
        self._attach_remaining(tokens, root_idx)

        # Step 5: Create tree
        tree = DependencyTree(tokens=tokens, multitokens=multitokens)

        return tree

    def _preprocess(self, words: List[str], pos_tags: Optional[List[str]] = None) -> tuple:
        """
        Segment words into tokens using morphology analyzer.

        Args:
            words: List of word forms
            pos_tags: Optional POS tags

        Returns:
            Tuple of (tokens, multitokens)
        """
        tokens = []
        multitokens = []
        token_id = 1

        for i, word in enumerate(words):
            # Get POS hint if available
            pos_hint = pos_tags[i] if pos_tags and i < len(pos_tags) else None

            # Segment word
            segments = self.morph_analyzer.segment_word(word, pos_hint)

            if len(segments) == 1:
                # Simple token (no segmentation)
                seg = segments[0]
                token = Token(
                    id=token_id,
                    form=seg.form,
                    lemma=seg.lemma,
                    upos=self._to_universal_pos(seg.pos),
                    xpos=seg.pos,
                    feats=seg.feats.copy() if seg.feats else {},
                    head=-1,  # Placeholder (will be set later)
                    deprel="_"  # Placeholder
                )
                tokens.append(token)
                token_id += 1

            else:
                # Multi-token word (fused form)
                start_id = token_id
                subtoken_list = []

                for seg in segments:
                    token = Token(
                        id=token_id,
                        form=seg.form,
                        lemma=seg.lemma,
                        upos=self._to_universal_pos(seg.pos),
                        xpos=seg.pos,
                        feats=seg.feats.copy() if seg.feats else {},
                        head=-1,
                        deprel="_"
                    )
                    tokens.append(token)
                    subtoken_list.append(token)
                    token_id += 1

                # Create multitoken
                end_id = token_id - 1
                multitoken = MultiToken(
                    id_range=(start_id, end_id),
                    form=word,
                    subtokens=subtoken_list
                )
                multitokens.append(multitoken)

        return tokens, multitokens

    def _find_root(self, tokens: List[Token]) -> Optional[int]:
        """
        Find the main predicate (root) of the sentence.

        Priority:
        1. Main verb with conjugation base
        2. Existential predicate
        3. Nominal predicate with copula
        4. Stative verb
        5. First verb
        6. First noun

        Args:
            tokens: List of Token objects

        Returns:
            Index of root token (0-indexed) or None
        """
        # Priority 1: Verb with conjugation base (aux before it)
        for i in range(len(tokens)):
            if tokens[i].upos == "VERB" and i > 0:
                # Check if preceded by auxiliary
                if tokens[i-1].xpos in ["APST", "AAOR", "ACONJ", "APREC", "ACOND"]:
                    return i

        # Priority 2: Existential predicate
        for i, token in enumerate(tokens):
            if token.xpos == "EXIST":
                return i

        # Priority 3: Nominal predicate with copula
        for i in range(len(tokens) - 1):
            if tokens[i].upos == "NOUN" and tokens[i+1].xpos == "COP":
                return i

        # Priority 4: Stative verb
        for i, token in enumerate(tokens):
            if tokens[i].xpos == "VSTAT":
                return i

        # Priority 5: First verb
        for i, token in enumerate(tokens):
            if token.upos == "VERB":
                return i

        # Priority 6: First noun
        for i, token in enumerate(tokens):
            if token.upos in ["NOUN", "PROPN"]:
                return i

        # Fallback: None (caller will use first token)
        return None

    def _attach_auxiliaries(self, tokens: List[Token], root_idx: int):
        """
        Attach conjugation bases as aux to main verb.

        Pattern: AUX → aux to VERB

        Args:
            tokens: List of tokens
            root_idx: Index of root token
        """
        root = tokens[root_idx]

        # Look backward from root for conjugation base
        for i in range(root_idx - 1, -1, -1):
            token = tokens[i]

            # Conjugation base and imperative markers
            if token.xpos in ["APST", "AAOR", "ACONJ", "AOPT", "AJUS",
                            "ANEGPST", "ANEGAOR", "ANEGJUS", "ANEGOPT",
                            "APREC", "AFUTCONJ", "ANY", "ACOND",
                            "ACAUS",  # Include causative
                            "VIMP"]:  # Include imperative
                token.head = root_idx + 1  # +1 for 1-indexing
                token.deprel = "aux"
                break  # Only one main aux

            # Stop at sentence boundaries
            if token.upos == "PUNCT":
                break

        # Look forward for future auxiliary (ⲛⲁ)
        for i in range(root_idx + 1, len(tokens)):
            token = tokens[i]
            if token.xpos == "FUT":
                token.head = root_idx + 1
                token.deprel = "aux"
                break

    def _attach_subjects(self, tokens: List[Token], root_idx: int):
        """
        Attach subjects as nsubj to predicate.

        Key principle: Subject attaches to VERB, not auxiliary!

        Args:
            tokens: List of tokens
            root_idx: Index of root token
        """
        root = tokens[root_idx]

        # Look backward for pronoun between aux and verb
        for i in range(root_idx - 1, -1, -1):
            token = tokens[i]

            # Subject pronoun
            if token.xpos == "PPERS" and token.head == -1:
                token.head = root_idx + 1
                token.deprel = "nsubj"
                return

            # Nominal subject before aux
            if token.upos in ["NOUN", "PROPN"] and token.head == -1:
                # Check if followed by pronoun (dislocated pattern)
                has_pronoun = any(
                    t.xpos == "PPERS" and t.head == -1
                    for t in tokens[i+1:root_idx]
                )

                if has_pronoun:
                    token.head = root_idx + 1
                    token.deprel = "dislocated"
                else:
                    token.head = root_idx + 1
                    token.deprel = "nsubj"
                return

            # Stop at major boundaries
            if token.upos in ["PUNCT", "CCONJ"]:
                break

    def _attach_objects(self, tokens: List[Token], root_idx: int):
        """
        Attach direct objects as obj to verb.

        Patterns:
        1. V + N (direct object)
        2. V + PRON (pronominal object)
        3. V + ⲛ/ⲙ + N (object with accusative marker)

        Args:
            tokens: List of tokens
            root_idx: Index of root token
        """
        root = tokens[root_idx]

        # Look forward from verb
        for i in range(root_idx + 1, len(tokens)):
            token = tokens[i]

            if token.head != -1:  # Already attached
                continue

            # Direct nominal object
            if token.upos in ["NOUN", "PROPN"]:
                # Check if preceded by case marker
                if i > 0 and tokens[i-1].xpos == "PREP":
                    prep = tokens[i-1]
                    if prep.form in ["ⲛ", "ⲙ"] and prep.head == -1:
                        # Accusative case marker
                        prep.head = i + 1
                        prep.deprel = "case"
                        token.head = root_idx + 1
                        token.deprel = "obj"
                        return
                else:
                    # Direct object (no marker)
                    token.head = root_idx + 1
                    token.deprel = "obj"
                    return

            # Pronominal object (PPERO)
            if token.xpos == "PPERO":
                # Check for preposition
                if i > 0 and tokens[i-1].xpos == "PREP":
                    prep = tokens[i-1]
                    prep_form = prep.form
                    # Accusative marker
                    if prep_form in ["ⲙⲙⲟ", "ⲛ", "ⲙ"]:
                        prep.head = i + 1
                        prep.deprel = "case"
                        token.head = root_idx + 1
                        token.deprel = "obj"
                    else:
                        # Oblique preposition
                        prep.head = i + 1
                        prep.deprel = "case"
                        token.head = root_idx + 1
                        token.deprel = "obl"
                    return

            # Stop at punctuation or next verb
            if token.upos in ["PUNCT"] or (token.upos == "VERB" and token.id != root.id):
                break

    def _attach_converters(self, tokens: List[Token], root_idx: int):
        """
        Attach converters as mark to converted clause.

        Converters: CCIRC, CREL, CFOC, CPRET
        All receive deprel=mark

        Args:
            tokens: List of tokens
            root_idx: Index of root token
        """
        # Look backward for converter before root
        for i in range(root_idx - 1, -1, -1):
            token = tokens[i]

            if token.head != -1:  # Already attached
                continue

            if token.xpos in ["CCIRC", "CREL", "CFOC", "CPRET"]:
                token.head = root_idx + 1
                token.deprel = "mark"
                return  # Only one converter per clause

    def _attach_case_markers(self, tokens: List[Token]):
        """
        Attach prepositions as case to their nominal objects.

        Pattern: PREP + (DET) + N
        Direction: Noun governs preposition (lexico-centric)

        Args:
            tokens: List of tokens
        """
        for i, token in enumerate(tokens):
            if token.xpos == "PREP" and token.head == -1:
                # Find following noun (within 3 tokens)
                for j in range(i + 1, min(i + 4, len(tokens))):
                    next_token = tokens[j]

                    if next_token.upos in ["NOUN", "PROPN", "PRON"] and next_token.xpos != "PPERS":
                        # Preposition attaches to noun
                        token.head = j + 1
                        token.deprel = "case"
                        break

                    # Skip determiners
                    if next_token.upos == "DET":
                        continue

                    # Stop at other POS
                    break

    def _attach_modifiers(self, tokens: List[Token], root_idx: int):
        """
        Attach adverbial and other modifiers.

        Patterns:
        - ADV → advmod to verb/noun
        - Greek particles → advmod

        Args:
            tokens: List of tokens
            root_idx: Index of root token
        """
        root = tokens[root_idx]

        for i, token in enumerate(tokens):
            if token.head != -1:  # Already attached
                continue

            # Adverbs
            if token.upos == "ADV":
                token.head = root_idx + 1
                token.deprel = "advmod"

            # Greek particles (ⲇⲉ, ⲅⲁⲣ, etc.)
            if token.xpos == "PTC":
                token.head = root_idx + 1
                token.deprel = "advmod"

            # Determiners attach to following noun
            if token.upos == "DET" and i + 1 < len(tokens):
                next_token = tokens[i + 1]
                if next_token.upos in ["NOUN", "PROPN"]:
                    token.head = i + 2  # +1 for 1-indexing, +1 for next
                    token.deprel = "det"

            # Copula attaches to predicate (should be noun before it)
            if token.xpos == "COP" and i > 0:
                prev_token = tokens[i - 1]
                if prev_token.upos in ["NOUN", "PROPN", "PRON"]:
                    token.head = i  # Previous token (1-indexed)
                    token.deprel = "cop"

    def _attach_remaining(self, tokens: List[Token], root_idx: int):
        """
        Attach any remaining unattached tokens to root with 'dep' relation.

        Args:
            tokens: List of tokens
            root_idx: Index of root token
        """
        for i, token in enumerate(tokens):
            if token.head == -1 and i != root_idx:
                token.head = root_idx + 1
                token.deprel = "dep"

    def _to_universal_pos(self, xpos: str) -> str:
        """
        Map Scriptorium POS tag to Universal POS tag.

        Args:
            xpos: Scriptorium POS tag

        Returns:
            Universal POS tag
        """
        mapping = {
            # Auxiliaries
            "APST": "AUX", "AAOR": "AUX", "ACONJ": "AUX",
            "AOPT": "AUX", "AJUS": "AUX", "ANY": "AUX",
            "ANEGPST": "AUX", "ANEGAOR": "AUX", "ANEGJUS": "AUX", "ANEGOPT": "AUX",
            "APREC": "AUX", "AFUTCONJ": "AUX",
            "ACAUS": "AUX",  # Causative
            "ACOND": "SCONJ",  # Conditional
            "ALIM": "SCONJ",

            # Converters
            "CCIRC": "SCONJ",  # Circumstantial
            "CREL": "SCONJ",   # Relative
            "CFOC": "AUX",     # Focalizing (note: AUX not SCONJ per guidelines)
            "CPRET": "AUX",    # Preterit

            # Copula
            "COP": "PART",  # Note: PART not AUX per guidelines!

            # Imperatives
            "VIMP": "AUX",  # Imperative marker (like aux, not main verb)

            # Verbs
            "EXIST": "VERB",
            "V": "VERB", "VSTAT": "VERB", "VBD": "VERB",

            # Nominals
            "N": "NOUN", "NOUN": "NOUN",
            "NPROP": "PROPN",

            # Pronouns
            "PPERS": "PRON", "PPERO": "PRON", "PPERI": "PRON",
            "PINT": "PRON",

            # Determiners
            "ART": "DET", "PPOS": "DET", "PDEM": "DET",

            # Others
            "PREP": "ADP",
            "ADV": "ADV", "IMOD": "ADV",
            "CONJ": "CCONJ",
            "PTC": "PART",
            "NEG": "ADV",
            "NEG_VIMP": "PART",  # Negative imperative
            "NUM": "NUM",
            "PUNCT": "PUNCT",
            "FUT": "AUX",
        }

        return mapping.get(xpos, "X")  # X for unknown


def create_tree_builder(prolog_engine=None) -> CopticTreeBuilder:
    """
    Factory function to create tree builder.

    Args:
        prolog_engine: Optional Prolog engine

    Returns:
        CopticTreeBuilder instance
    """
    return CopticTreeBuilder(prolog_engine)
