#!/usr/bin/env python3
"""
Coptic Dependency Tree Data Structures
======================================

Core classes for representing dependency trees in CoNLL-U format.

Based on:
- Universal Dependencies CoNLL-U format specification
- Coptic UD Guidelines v1.1.0 (Zeldes 2016)
"""

from dataclasses import dataclass, field
from typing import Union, List, Dict, Optional, Tuple


@dataclass
class Token:
    """
    Represents a single token in a dependency tree.

    Follows CoNLL-U format with 10 columns:
    ID FORM LEMMA UPOS XPOS FEATS HEAD DEPREL DEPS MISC

    Example:
        Token(id=3, form="ⲃⲱⲕ", lemma="ⲃⲱⲕ", upos="VERB", xpos="V",
              feats={"VerbForm": "Fin"}, head=0, deprel="root")
    """

    # CoNLL-U columns
    id: int                              # Token ID (1-indexed)
    form: str                            # Surface form
    lemma: str                           # Lemma (dictionary form)
    upos: str                            # Universal POS tag
    xpos: str                            # Language-specific POS (Scriptorium tag)
    feats: Optional[Dict[str, str]]      # Morphological features
    head: int                            # Head token ID (0 = root)
    deprel: str                          # Dependency relation
    deps: str = "_"                      # Enhanced dependencies (usually empty)
    misc: Optional[Dict[str, str]] = None  # Miscellaneous annotations

    def __post_init__(self):
        """Initialize empty dicts if None"""
        if self.feats is None:
            self.feats = {}
        if self.misc is None:
            self.misc = {}

    def to_conllu(self) -> str:
        """
        Convert token to CoNLL-U format line.

        Returns:
            Tab-separated string with 10 columns

        Example:
            "3\tⲃⲱⲕ\tⲃⲱⲕ\tVERB\tV\tVerbForm=Fin\t0\troot\t_\t_"
        """
        # Format features as key=value pairs
        if self.feats:
            feats_str = "|".join(f"{k}={v}" for k, v in sorted(self.feats.items()))
        else:
            feats_str = "_"

        # Format misc as key=value pairs
        if self.misc:
            misc_str = "|".join(f"{k}={v}" for k, v in sorted(self.misc.items()))
        else:
            misc_str = "_"

        return "\t".join([
            str(self.id),
            self.form,
            self.lemma,
            self.upos,
            self.xpos,
            feats_str,
            str(self.head),
            self.deprel,
            self.deps,
            misc_str
        ])

    @classmethod
    def from_conllu(cls, line: str) -> 'Token':
        """
        Parse a CoNLL-U line into a Token object.

        Args:
            line: Tab-separated CoNLL-U line

        Returns:
            Token object

        Example:
            Token.from_conllu("3\\tⲃⲱⲕ\\tⲃⲱⲕ\\tVERB\\tV\\tVerbForm=Fin\\t0\\troot\\t_\\t_")
        """
        parts = line.strip().split("\t")
        if len(parts) != 10:
            raise ValueError(f"Invalid CoNLL-U line: expected 10 columns, got {len(parts)}")

        # Parse ID (must be integer for regular token)
        token_id = int(parts[0])

        # Parse features
        feats = {}
        if parts[5] != "_":
            for feat in parts[5].split("|"):
                if "=" in feat:
                    k, v = feat.split("=", 1)
                    feats[k] = v

        # Parse misc
        misc = {}
        if parts[9] != "_":
            for item in parts[9].split("|"):
                if "=" in item:
                    k, v = item.split("=", 1)
                    misc[k] = v

        return cls(
            id=token_id,
            form=parts[1],
            lemma=parts[2],
            upos=parts[3],
            xpos=parts[4],
            feats=feats,
            head=int(parts[6]),
            deprel=parts[7],
            deps=parts[8],
            misc=misc
        )

    def __repr__(self) -> str:
        """Readable representation"""
        return f"Token(id={self.id}, form='{self.form}', deprel='{self.deprel}', head={self.head})"


@dataclass
class MultiToken:
    """
    Represents a fused surface form split into multiple syntactic tokens.

    Example: ⲁϥⲃⲱⲕ "he went" splits into:
        - Supertoken: 1-3 ⲁϥⲃⲱⲕ
        - Subtokens: 1=ⲁ (aux), 2=ϥ (nsubj), 3=ⲃⲱⲕ (root)

    CoNLL-U format:
        1-3  ⲁϥⲃⲱⲕ  _  _  _  _  _  _  _  _
        1    ⲁ      ⲁ  AUX ...
        2    ϥ      ⲛⲧⲟϥ PRON ...
        3    ⲃⲱⲕ    ⲃⲱⲕ VERB ...
    """

    id_range: Tuple[int, int]  # e.g., (1, 3) for "1-3"
    form: str                   # Surface form: ⲁϥⲃⲱⲕ
    subtokens: List[Token]      # List of Token objects

    def to_conllu(self) -> str:
        """
        Convert supertoken to CoNLL-U format line.

        Returns:
            Tab-separated string with ID range and form, rest are underscores

        Example:
            "1-3\tⲁϥⲃⲱⲕ\t_\t_\t_\t_\t_\t_\t_\t_"
        """
        start, end = self.id_range
        return f"{start}-{end}\t{self.form}\t" + "\t".join(["_"] * 8)

    @classmethod
    def from_conllu(cls, supertoken_line: str, subtoken_lines: List[str]) -> 'MultiToken':
        """
        Parse a multi-token word from CoNLL-U lines.

        Args:
            supertoken_line: Line with ID range (e.g., "1-3\\tⲁϥⲃⲱⲕ\\t_...")
            subtoken_lines: Lines for individual tokens

        Returns:
            MultiToken object
        """
        parts = supertoken_line.strip().split("\t")
        id_range_str = parts[0]
        form = parts[1]

        # Parse ID range
        start, end = map(int, id_range_str.split("-"))

        # Parse subtokens
        subtokens = [Token.from_conllu(line) for line in subtoken_lines]

        return cls(
            id_range=(start, end),
            form=form,
            subtokens=subtokens
        )

    def __repr__(self) -> str:
        """Readable representation"""
        start, end = self.id_range
        return f"MultiToken({start}-{end}, form='{self.form}', {len(self.subtokens)} subtokens)"


class DependencyTree:
    """
    Complete dependency tree for a Coptic sentence.

    Provides methods for:
    - Tree traversal (get children, ancestors, etc.)
    - CoNLL-U export
    - ASCII tree visualization
    - Tree validation

    Example:
        tree = DependencyTree(tokens, multitokens)
        print(tree.to_conllu(sent_id="s001", text="ⲁϥⲃⲱⲕ"))
        print(tree.to_ascii_tree())
    """

    def __init__(self,
                 tokens: List[Token],
                 multitokens: Optional[List[MultiToken]] = None,
                 metadata: Optional[Dict[str, str]] = None):
        """
        Initialize dependency tree.

        Args:
            tokens: List of Token objects (must include all subtokens)
            multitokens: Optional list of MultiToken objects
            metadata: Optional metadata (sent_id, text, etc.)
        """
        self.tokens = tokens
        self.multitokens = multitokens or []
        self.metadata = metadata or {}
        self.root = self._find_root()

    def _find_root(self) -> Token:
        """
        Find the root token (head=0).

        Returns:
            Root token

        Raises:
            ValueError: If no root found or multiple roots
        """
        roots = [t for t in self.tokens if t.head == 0]

        if len(roots) == 0:
            raise ValueError("No root found in tree!")
        if len(roots) > 1:
            raise ValueError(f"Multiple roots found: {roots}")

        return roots[0]

    def get_children(self, token_id: int) -> List[Token]:
        """
        Get all children of a token.

        Args:
            token_id: ID of parent token

        Returns:
            List of child tokens (may be empty)
        """
        return [t for t in self.tokens if t.head == token_id]

    def get_descendants(self, token_id: int) -> List[Token]:
        """
        Get all descendants (children, grandchildren, etc.) of a token.

        Args:
            token_id: ID of ancestor token

        Returns:
            List of descendant tokens
        """
        descendants = []
        children = self.get_children(token_id)
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_descendants(child.id))
        return descendants

    def get_ancestors(self, token_id: int) -> List[Token]:
        """
        Get all ancestors (parent, grandparent, etc.) up to root.

        Args:
            token_id: ID of token

        Returns:
            List of ancestor tokens (empty if token is root)
        """
        ancestors = []
        current = self.get_token_by_id(token_id)

        while current and current.head != 0:
            parent = self.get_token_by_id(current.head)
            if not parent:
                break
            ancestors.append(parent)
            current = parent

        return ancestors

    def get_token_by_id(self, token_id: int) -> Optional[Token]:
        """
        Get token by its ID.

        Args:
            token_id: Token ID (1-indexed)

        Returns:
            Token object or None if not found
        """
        for token in self.tokens:
            if token.id == token_id:
                return token
        return None

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate tree structure.

        Checks:
        - Exactly one root (head=0)
        - All heads point to valid tokens
        - No cycles
        - Tree is connected

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check for exactly one root
        roots = [t for t in self.tokens if t.head == 0]
        if len(roots) == 0:
            errors.append("No root token found")
        elif len(roots) > 1:
            errors.append(f"Multiple roots found: {[r.id for r in roots]}")

        # Check all heads are valid
        token_ids = {t.id for t in self.tokens}
        for token in self.tokens:
            if token.head != 0 and token.head not in token_ids:
                errors.append(f"Token {token.id} has invalid head {token.head}")

        # Check for cycles
        for token in self.tokens:
            visited = set()
            current = token
            while current.head != 0:
                if current.id in visited:
                    errors.append(f"Cycle detected involving token {current.id}")
                    break
                visited.add(current.id)
                current = self.get_token_by_id(current.head)
                if not current:
                    break

        return (len(errors) == 0, errors)

    def to_conllu(self,
                  sent_id: Optional[str] = None,
                  text: Optional[str] = None,
                  text_en: Optional[str] = None) -> str:
        """
        Export tree to CoNLL-U format.

        Args:
            sent_id: Sentence ID (optional, overrides metadata)
            text: Original text (optional, overrides metadata)
            text_en: English translation (optional)

        Returns:
            Multi-line string in CoNLL-U format

        Example:
            # sent_id = s001
            # text = ⲁϥⲃⲱⲕ
            1-3  ⲁϥⲃⲱⲕ  _  _  _  _  _  _  _  _
            1    ⲁ      ⲁ  AUX ...
            2    ϥ      ⲛⲧⲟϥ PRON ...
            3    ⲃⲱⲕ    ⲃⲱⲕ VERB ...

        """
        lines = []

        # Add metadata comments
        if sent_id or 'sent_id' in self.metadata:
            sid = sent_id or self.metadata['sent_id']
            lines.append(f"# sent_id = {sid}")

        if text_en or 'text_en' in self.metadata:
            ten = text_en or self.metadata['text_en']
            lines.append(f"# text_en = {ten}")

        if text or 'text' in self.metadata:
            txt = text or self.metadata['text']
            lines.append(f"# text = {txt}")

        # Interleave multitokens and tokens
        # Build index of multitoken ranges
        multitoken_map = {}
        for mt in self.multitokens:
            start, end = mt.id_range
            multitoken_map[start] = mt

        # Output tokens in order
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]

            # Check if this token starts a multitoken
            if token.id in multitoken_map:
                mt = multitoken_map[token.id]
                lines.append(mt.to_conllu())

            # Output token
            lines.append(token.to_conllu())
            i += 1

        lines.append("")  # Empty line after sentence
        return "\n".join(lines)

    def to_ascii_tree(self) -> str:
        """
        Simple ASCII tree visualization (no colors).

        Returns:
            Multi-line string with tree structure

        Example:
            ⲃⲱⲕ (root)
            ├── ⲁ (aux)
            └── ϥ (nsubj)
        """
        if not self.root:
            return "[Empty tree]"

        return self._render_subtree(self.root, prefix="", is_last=True)

    def _render_subtree(self, token: Token, prefix: str, is_last: bool) -> str:
        """
        Recursively render tree branches.

        Args:
            token: Current token to render
            prefix: Prefix string for indentation
            is_last: Whether this is the last child

        Returns:
            Rendered subtree as string
        """
        lines = []

        # Current node
        if token.head == 0:
            # Root node (no connector)
            lines.append(f"{token.form} ({token.deprel})")
        else:
            # Child node (with connector)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{token.form} ({token.deprel})")

        # Get and sort children by position
        children = sorted(self.get_children(token.id), key=lambda t: t.id)

        # Render children
        for i, child in enumerate(children):
            extension = "    " if is_last or token.head == 0 else "│   "
            child_is_last = (i == len(children) - 1)

            child_tree = self._render_subtree(
                child,
                prefix + extension if token.head != 0 else "",
                child_is_last
            )
            lines.append(child_tree)

        return "\n".join(lines)

    def __repr__(self) -> str:
        """Readable representation"""
        return f"DependencyTree({len(self.tokens)} tokens, root='{self.root.form}')"

    def __str__(self) -> str:
        """String representation shows ASCII tree"""
        return self.to_ascii_tree()


def read_conllu_file(file_path: str) -> List[DependencyTree]:
    """
    Read CoNLL-U file and parse into list of DependencyTree objects.

    Args:
        file_path: Path to CoNLL-U file

    Returns:
        List of DependencyTree objects (one per sentence)

    Example:
        trees = read_conllu_file("corpus.conllu")
        for tree in trees:
            print(tree.to_ascii_tree())
    """
    trees = []
    current_tokens = []
    current_multitokens = []
    current_metadata = {}
    pending_subtoken_lines = []
    current_multitoken_line = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip("\n")

            # Empty line = end of sentence
            if not line:
                if current_tokens:
                    tree = DependencyTree(
                        tokens=current_tokens,
                        multitokens=current_multitokens,
                        metadata=current_metadata
                    )
                    trees.append(tree)
                    current_tokens = []
                    current_multitokens = []
                    current_metadata = {}
                    pending_subtoken_lines = []
                    current_multitoken_line = None
                continue

            # Comment line = metadata
            if line.startswith("#"):
                if "=" in line:
                    key, value = line[1:].split("=", 1)
                    current_metadata[key.strip()] = value.strip()
                continue

            # Data line
            parts = line.split("\t")
            id_field = parts[0]

            # Multi-token word (e.g., "1-3")
            if "-" in id_field:
                current_multitoken_line = line
                pending_subtoken_lines = []
                continue

            # Regular token
            token = Token.from_conllu(line)
            current_tokens.append(token)

            # If we're collecting subtokens for a multitoken
            if current_multitoken_line:
                pending_subtoken_lines.append(line)

                # Check if we've collected all subtokens
                mt_parts = current_multitoken_line.split("\t")
                mt_range = mt_parts[0]
                start, end = map(int, mt_range.split("-"))

                if token.id == end:
                    # All subtokens collected
                    multitoken = MultiToken.from_conllu(
                        current_multitoken_line,
                        pending_subtoken_lines
                    )
                    current_multitokens.append(multitoken)
                    current_multitoken_line = None
                    pending_subtoken_lines = []

    # Don't forget last sentence if file doesn't end with empty line
    if current_tokens:
        tree = DependencyTree(
            tokens=current_tokens,
            multitokens=current_multitokens,
            metadata=current_metadata
        )
        trees.append(tree)

    return trees


def write_conllu_file(trees: List[DependencyTree], file_path: str):
    """
    Write list of DependencyTree objects to CoNLL-U file.

    Args:
        trees: List of DependencyTree objects
        file_path: Output file path
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        for tree in trees:
            f.write(tree.to_conllu())
            f.write("\n")  # Extra newline between sentences
