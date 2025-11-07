# Tokenization Data

## ✅ Tokenization Files Included!

This directory contains small configuration files for Stanza tokenization:

**Files included**:
- `cop_scriptorium-ud-dev-mwt.json` - Multi-word token rules (dev set)
- `cop_scriptorium-ud-train-mwt.json` - Multi-word token rules (training set)

These tiny JSON files configure how Stanza splits multi-word tokens in Coptic text.

## What Are Multi-Word Tokens (MWT)?

In Coptic, some written forms represent multiple syntactic words:

- **ⲉⲧⲃⲉ** → **ⲉ** (preposition) + **ⲧⲃⲉ** (noun)
- **ⲉϩⲟⲩⲛ** → **ⲉ** (preposition) + **ϩⲟⲩⲛ** (adverb)

These JSON files tell Stanza how to split these correctly.

## Parser Behavior

The parser automatically uses these files if present. No configuration needed!

## Additional Training Data (Optional)

If you want to retrain Stanza's tokenizer, you would need:

```
cop_scriptorium-ud-train.txt
cop_scriptorium-ud-dev.txt
cop_scriptorium-ud-test.txt
cop_scriptorium-ud-train.conllu
cop_scriptorium-ud-dev.conllu
cop_scriptorium-ud-test.conllu
*.toklabels files
```

**Source**: https://github.com/UniversalDependencies/UD_Coptic-Scriptorium
**License**: CC BY-SA 4.0

But for normal use, you don't need these. Stanza has built-in Coptic tokenization.

---

**Summary**: Contains small tokenization config files (already included).
