# Lexicon Data

## ⚠️ The Main Lexicon is Already Included!

**You don't need files in this directory.** The parser's lexicon is at the project root:

📄 **`coptic_lexicon.pl`** (485 KB) - 6,842 lexical entries including:
- Nouns with gender and number
- Verbs with transitivity information  
- Adjectives, pronouns, determiners, etc.
- Morphological features

This Prolog lexicon is used by `coptic_prolog_rules.py` for grammatical validation.

## What's This Directory For?

Optional supplementary resources only:
- Custom lexicon extensions
- Research data
- Experimental features

**Most users won't need anything here.**

## Lexicon Coverage

The included `coptic_lexicon.pl` contains:
- **6,842+ entries** from Coptic Scriptorium resources
- **Complete coverage** of common Coptic vocabulary
- **Format**: Prolog facts for fast lookup

## Lexicon Format

The lexicon uses Prolog facts:

```prolog
% Nouns with gender and number
coptic_noun('ⲛⲟⲩⲧⲉ', masc, sing).    % god
coptic_noun('ⲃⲁϣⲟⲣ', fem, sing).     % basket

% Verbs with transitivity
coptic_verb('ⲥⲱⲧⲙ', [transitive]).  % hear
coptic_verb('ⲃⲱⲕ', [intransitive]). % go

% Adjectives with agreement
coptic_adjective('ⲛⲟⲩϥⲣⲉ', masc, sing). % good
```

## Adding Custom Entries

To extend the lexicon, edit `coptic_lexicon.pl` at the project root:

```prolog
% Add your custom entries at the end of the file
coptic_noun('ⲙⲓⲛⲉ', fem, sing).
coptic_verb('ⲙⲟⲩⲧⲉ', [intransitive]).
```

Then restart the parser to load new entries.

## Data Source

**Extracted from**: Comprehensive Coptic Lexicon / Coptic Scriptorium  
**License**: CC BY-SA 4.0  
**Citation**:
```
Coptic Scriptorium. (2024). Coptic SCRIPTORIUM Treebank.
Universal Dependencies. https://github.com/UniversalDependencies/UD_Coptic-Scriptorium
```

---

**Summary**: Empty placeholder directory. Main lexicon is in `coptic_lexicon.pl` at project root.
