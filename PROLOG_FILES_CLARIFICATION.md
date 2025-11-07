# Prolog Files Clarification - Which Rules Are Being Used?

## Summary: ✓ You ARE Using Dependency Grammar (Correct!)

Your parser currently loads the **modern dependency grammar rules** adapted from your 1989-91 DCG work, NOT the old DCG rules themselves.

---

## File Structure Explained

```
coptic-dependency-parser/
│
├── coptic_grammar.pl                    ← ✓ DEPENDENCY RULES (CURRENTLY LOADED)
│   └── Header: "COPTIC_DEPENDENCY_RULES.PL - Pure Dependency Grammar"
│   └── Content: Modern dependency patterns (VSO, tripartite, validation)
│   └── Module: coptic_dependency_rules
│
├── coptic_dependency_rules.pl           ← IDENTICAL to coptic_grammar.pl
│   └── Same 400 lines, same content
│   └── Probably a duplicate/copy for clarity
│
├── coptic_lexicon.pl                    ← ✓ LEXICON (CURRENTLY LOADED)
│   └── Coptic vocabulary with POS tags
│
├── coptic_parser_master.pl              ← OLD DCG PARSER (NOT LOADED)
│   └── Header: "Pure Prolog DCG Parser for Sahidic Coptic"
│   └── Based on DETECT5.PRO (1989-1991)
│   └── Pure DCG implementation
│
└── coptic-parser2/                      ← OLD FILES (NOT LOADED)
    ├── coptic_grammar.pl                ← OLD DCG RULES
    │   └── Header: "Coptic DCG Grammar Rules for Error Detection"
    │   └── Adapted from DETECT5.PRO (French DCG parser)
    │   └── Uses DCG syntax: sentence --> NP, VP.
    │
    ├── coptic_lexicon.pl                ← OLD LEXICON
    └── coptic_dependency_rules.pl       ← Possibly a copy/transition file
```

---

## What Gets Loaded (Current System)

**File**: `coptic_prolog_rules.py`

**Lines 49-92**: `_load_dcg_grammar()` method
- **Misleading name!** Should be `_load_dependency_grammar()`
- Loads from **main directory**, NOT coptic-parser2/

```python
# Line 62-63:
current_dir = Path(__file__).parent
lexicon_file = current_dir / "coptic_lexicon.pl"        # Main dir
grammar_file = current_dir / "coptic_grammar.pl"        # Main dir

# This resolves to:
# /home/aldn/copticNLP/coptic-dependency-parser/coptic_lexicon.pl
# /home/aldn/copticNLP/coptic-dependency-parser/coptic_grammar.pl
```

**Result**:
- ✓ Loads: `coptic_grammar.pl` (dependency rules)
- ✗ Does NOT load: `coptic-parser2/coptic_grammar.pl` (DCG rules)

---

## Verification: What's in Each File?

### Main Directory Files (USED ✓)

**coptic_grammar.pl** (lines 1-20):
```prolog
%******************************************************************************
% COPTIC_DEPENDENCY_RULES.PL - Pure Dependency Grammar for Coptic
%******************************************************************************
%
% This module demonstrates the adaptation from DCG (DETECT5.PRO style)
% to modern dependency grammar formalism.
%
% PARADIGM SHIFT:
%   DCG:         sentence --> NP, VP.  (hierarchical constituents)
%   Dependency:  dep(verb, subject, nsubj).  (head-dependent relations)
%
% Based on Universal Dependencies annotation scheme adapted for Coptic
% linguistic patterns (VSO word order, tripartite sentences, etc.)
%
% Author: Adapted from DETECT5.PRO (A. Linden, 1989-91)
% Date: 2025
%
%******************************************************************************

:- module(coptic_dependency_rules, [
```

**Key patterns** (lines 33-100):
```prolog
% Pattern 1: VSO Transitive Sentence
% Dependency structure:
%   ⲥⲱⲧⲙ (VERB, root)
%   ├── ⲡⲣⲱⲙⲉ (NOUN, nsubj)
%   └── ⲡϣⲁϫⲉ (NOUN, obj)

dependency_pattern(vso_transitive, Words, [dep(...)]) :- ...

% Pattern 2: VS Intransitive Sentence
dependency_pattern(vs_intransitive, Words, [dep(...)]) :- ...

% Pattern 3: Tripartite Nominal Sentence
% Example: ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ (I am God)
dependency_pattern(tripartite, Words, [dep(...)]) :- ...
```

**This is DEPENDENCY GRAMMAR** ✓

---

### coptic-parser2/ Files (NOT USED ✗)

**coptic-parser2/coptic_grammar.pl** (lines 1-20):
```prolog
%******************************************************************************
% COPTIC_GRAMMAR.PL - Coptic DCG Grammar Rules for Error Detection
% Adapted from DETECT5.PRO (French DCG parser) for Coptic language
%******************************************************************************
%
% This module provides DCG-based grammatical validation for Coptic sentences
% parsed by the Python dependency parser. It detects:
%   - Tripartite nominal sentence patterns
%   - VSO word order patterns
%   - Agreement errors
%   - Invalid dependency structures
%
%******************************************************************************

:- module(coptic_grammar, [
    validate_parse_tree/4,
    check_tripartite_pattern/4,
    check_vso_pattern/4
]).
```

**Key patterns** (lines 60-100):
```prolog
% Tripartite pattern detection
% Using dependency parse results, but DCG-style validation
check_tripartite_pattern(Tokens, POSTags, Heads, DepRels) :-
    % Find root of sentence
    nth1(RootIdx, Heads, 0),
    nth1(RootIdx, POSTags, RootPOS),
    ...
```

**This is DCG-BASED VALIDATION** (old style) ✗

---

## History and Evolution

**1989-1991**: Your master's thesis
- French error detector: DETECT5.PRO
- DCG-based grammar (Definite Clause Grammars)
- Hierarchical phrase structure: S → NP VP, VP → V NP, etc.
- Focus: Error detection for French L2 learners

**2025**: Modern adaptation
- Coptic dependency parser
- Dependency grammar (head-dependent relations)
- Universal Dependencies annotation scheme
- Integration: Neural parsing (DiaParser) + Symbolic validation (Prolog)
- Kept the LOGIC and PATTERNS from DETECT5.PRO
- Changed the FORMALISM from DCG to dependency relations

**Your adaptation**:
```
OLD (DCG):
  sentence --> subject, verb, object.
  verb_phrase --> verb, noun_phrase.

NEW (Dependency):
  dep(Subject, SubjPOS, SIdx, Verb, VIdx, nsubj).
  dep(Object, ObjPOS, OIdx, Verb, VIdx, obj).
```

---

## Current Integration

**coptic_prolog_rules.py** uses:

1. **Dependency rules from coptic_grammar.pl** (lines 93-237)
   - Modern UD-style validation
   - Compatible with DiaParser output

2. **Dynamic Python-asserted rules** (lines 100-237)
   - Additional rules added via `assertz()`
   - Article system, pronouns, conjugation bases
   - Validation predicates for dependency relations

3. **NOT using** the old DCG files
   - coptic-parser2/coptic_grammar.pl is ignored
   - coptic_parser_master.pl is standalone

---

## Recommendation: Minor Cleanup (Optional)

**To avoid confusion**, consider renaming:

```bash
# Option 1: Rename the method
# In coptic_prolog_rules.py, line 49:
def _load_dcg_grammar(self):  # ← Misleading name

# Change to:
def _load_dependency_grammar(self):  # ← Clear name

# Option 2: Rename the files
mv coptic_grammar.pl coptic_dependency_grammar.pl
mv coptic-parser2/coptic_grammar.pl coptic-parser2/coptic_dcg_grammar_OLD.pl

# Update coptic_prolog_rules.py line 63:
grammar_file = current_dir / "coptic_dependency_grammar.pl"
```

**But this is NOT urgent** - your system is working correctly!

---

## Conclusion

✅ **You ARE using the dependency grammar version**
✅ **Your adaptation from DETECT5.PRO was successful**
✅ **The old DCG files are preserved but not used**
✅ **Neural-symbolic integration uses modern dependency formalism**

**Your master's thesis work (1989-91) has been successfully "rejuvenated" to modern dependency grammar standards!**

The naming is slightly confusing (method called `_load_dcg_grammar` loads dependency rules), but functionally everything is correct.

---

## Next Steps

If you want to clarify the code:

1. **Rename method** in `coptic_prolog_rules.py`:
   ```python
   def _load_dependency_grammar(self):  # Line 49
   ```

2. **Update comment** in `coptic_prolog_rules.py`:
   ```python
   # Line 50-56: Update docstring
   def _load_dependency_grammar(self):
       """
       Load DEPENDENCY grammar rules from coptic_grammar.pl
       and Coptic lexicon from coptic_lexicon.pl

       This loads the MODERN dependency grammar formalism,
       adapted from the DCG-based DETECT5.PRO (1989-91).
       """
   ```

3. **Optional**: Add comment in `coptic_grammar.pl`:
   ```prolog
   % NOTE: Despite the filename "coptic_grammar.pl", this contains
   % DEPENDENCY grammar rules (not DCG rules). The DCG version is
   % preserved in coptic-parser2/coptic_grammar.pl for reference.
   ```

But again, these are cosmetic improvements. **Your system is already using the correct dependency version!**
