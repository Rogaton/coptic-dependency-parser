# Dependency Parsing Training Data

## ⚠️ This Directory is Empty (You Don't Need Files Here!)

**The parser works without any files in this directory.** It uses:
- Stanza's built-in dependency parser (automatic fallback), OR
- A pre-trained DiaParser model (optional - place in `models/` directory)

## When Do You Need This?

Only if you want to **train your own DiaParser model** from scratch.

## Training Data Files

If training, place these CoNLL-U files here:

```
cop_scriptorium.train.in.conllu   (~114 MB) - Training set
cop_scriptorium.dev.in.conllu     (~14 MB)  - Development set
cop_scriptorium.test.in.conllu    (~14 MB)  - Test set
```

## Where to Get Training Data

**Source**: Coptic Scriptorium UD Treebank (CC BY-SA 4.0)

1. Visit: https://github.com/UniversalDependencies/UD_Coptic-Scriptorium
2. Download latest release
3. Copy .conllu files to this directory
4. See `models/README.md` for training instructions

## Citation

```
Zeldes, Amir and Schroeder, Caroline T. (2016).
"An NLP Pipeline for Coptic."
Proceedings of the 10th SIGHUM Workshop on Language Technology for Cultural Heritage,
Social Sciences, and Humanities (LaTeCH). Berlin: 146-155.
```

---

**Summary**: Empty placeholder. Only needed for model training.
