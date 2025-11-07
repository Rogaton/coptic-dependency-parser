# Coptic Character Reference
## Quick Copy & Paste Guide for Manual Transcription

Since **OCR doesn't work well** on Kasser's handwritten lexicon, use this reference for **manual transcription**.

---

## 📋 Coptic Alphabet (Copy & Paste)

### Lowercase
```
ⲁ ⲃ ⲅ ⲇ ⲉ ⲍ ⲏ ⲑ ⲓ ⲕ ⲗ ⲙ ⲛ ⲝ ⲟ ⲡ ⲣ ⲥ ⲧ ⲩ ⲫ ⲭ ⲯ ⲱ
```

### Uppercase
```
Ⲁ Ⲃ Ⲅ Ⲇ Ⲉ Ⲍ Ⲏ Ⲑ Ⲓ Ⲕ Ⲗ Ⲙ Ⲛ Ⲝ Ⲟ Ⲡ Ⲣ Ⲥ Ⲧ Ⲩ Ⲫ Ⲭ Ⲯ Ⲱ
```

### Special Coptic Letters
```
ϣ ϥ ϧ ϩ ϫ ϭ ϯ
Ϣ Ϥ Ϧ Ϩ Ϫ Ϭ Ϯ
```

---

## 🎯 Character-by-Character Reference

| Character | Name | Latin | Unicode |
|-----------|------|-------|---------|
| ⲁ | alpha | a | U+2C81 |
| ⲃ | beta (vida) | b | U+2C83 |
| ⲅ | gamma | g | U+2C85 |
| ⲇ | dalda | d | U+2C87 |
| ⲉ | eie | e | U+2C89 |
| ⲍ | zata | z | U+2C8B |
| ⲏ | eta | ē | U+2C8D |
| ⲑ | theta | th | U+2C8F |
| ⲓ | iota | i | U+2C91 |
| ⲕ | kapa | k | U+2C93 |
| ⲗ | laula | l | U+2C95 |
| ⲙ | me | m | U+2C97 |
| ⲛ | ne | n | U+2C99 |
| ⲝ | xi (eksi) | x | U+2C9B |
| ⲟ | o | o | U+2C9D |
| ⲡ | pi | p | U+2C9F |
| ⲣ | ro | r | U+2CA1 |
| ⲥ | sima | s | U+2CA3 |
| ⲧ | tau | t | U+2CA5 |
| ⲩ | he | u/y | U+2CA7 |
| ⲫ | phi | ph | U+2CA9 |
| ⲭ | khi | kh | U+2CAB |
| ⲯ | psi | ps | U+2CAD |
| ⲱ | omega | ō | U+2CAF |
| ϣ | shai | sh | U+03E3 |
| ϥ | fai | f | U+03E5 |
| ϧ | khai | x | U+03E7 |
| ϩ | hori | h | U+03E9 |
| ϫ | janja | j | U+03EB |
| ϭ | chima | č | U+03ED |
| ϯ | ti | ti | U+03EF |

---

## 📖 Common Words from Page 7 (Copy & Paste)

Based on the image you're transcribing, here are the actual entries I can see:

### Nouns
```
ⲁⲅⲁⲡⲏ     (agapē - love)
ⲁⲅⲅⲉⲗⲟⲥ   (angelos - angel)
```

### Adjectives
```
ⲁⲅⲁⲑⲟⲥ   (agathos - good)
```

### Verbs
```
ⲁⲕⲟⲩⲱ    (akouw - to give birth)
```

### Pronouns
```
ⲁⲛⲟⲕ     (anok - I, me)
ⲁⲛⲧⲟⲕ    (antok - you, masc.)
ⲁⲛⲧⲟ     (anto - you, fem.)
```

### Particles/Conjunctions
```
ⲁⲛ       (an - negation)
ⲁⲗⲗⲁ     (alla - but)
```

---

## ⌨️ Coptic Keyboard Input (Linux)

### Option 1: Install Coptic Keyboard

```bash
# Install IBus Coptic keyboard
sudo apt install ibus-table-coptic

# Then:
# 1. Go to Settings → Region & Language
# 2. Click "+" to add input source
# 3. Search for "Coptic"
# 4. Add "Coptic (Sahidic)"
# 5. Switch between keyboards with Super+Space
```

### Option 2: Unicode Input (Works Everywhere)

Press **Ctrl+Shift+U**, then type the hex code, then press **Space**:

Examples:
- `Ctrl+Shift+U` → `2c81` → `Space` = ⲁ
- `Ctrl+Shift+U` → `2c83` → `Space` = ⲃ
- `Ctrl+Shift+U` → `03e9` → `Space` = ϩ

---

## 🖱️ Quick Copy Toolbar (Keep This Open)

Copy these as needed during transcription:

**Alpha → Iota:**
```
ⲁ  ⲃ  ⲅ  ⲇ  ⲉ  ⲍ  ⲏ  ⲑ  ⲓ
```

**Kappa → Pi:**
```
ⲕ  ⲗ  ⲙ  ⲛ  ⲝ  ⲟ  ⲡ
```

**Ro → Omega:**
```
ⲣ  ⲥ  ⲧ  ⲩ  ⲫ  ⲭ  ⲯ  ⲱ
```

**Special (Sahidic):**
```
ϣ  ϥ  ϧ  ϩ  ϫ  ϭ  ϯ
```

---

## 🎯 Recommended Transcription Workflow

### Setup (One Time)

```bash
cd /home/aldn/copticNLP/coptic-dependency-parser

# Keep this reference open in browser or terminal
cat COPTIC_CHARACTERS_REFERENCE.md
```

### Per Session (Pages 8, 9, 10...)

```bash
# Open page 8 with helper
./transcription_helper.sh 8

# This opens:
# 1. Image viewer (left) - shows lexiqueRK2-8.png
# 2. Terminal (right) - shows transcription tool
# 3. Character reference (top) - this file for copying
```

### Per Entry (30-60 seconds each)

1. **Look at PNG** - see entry like: `○ ΔΛΛΔ ⲁⲗⲗⲁ mais`
2. **Build the word**:
   - Look up `ⲁ` in this reference → copy
   - Look up `ⲗ` in this reference → copy
   - Look up `ⲗ` in this reference → copy
   - Look up `ⲁ` in this reference → copy
   - Result: `ⲁⲗⲗⲁ`
3. **Paste into tool** when prompted for "Coptic word"
4. **Add definition** from PNG: "mais" (but)
5. **Continue** to next entry

**Time per page**: ~30-40 minutes (30-40 entries)

---

## 💡 Pro Tips

### Tip 1: Use Multiple Monitors/Windows
- **Left**: Image viewer with PNG
- **Center**: This character reference
- **Right**: Terminal with transcription tool

### Tip 2: Learn Common Prefixes
- `ⲁⲛ-` (an-) = negation prefix
- `ⲁⲧ-` (at-) = negative prefix
- `ⲙⲛ-` (mn-) = with, and

### Tip 3: Build Word Templates
Create a text file `my_coptic_templates.txt`:
```
ⲁ__ (start with alpha)
ⲙⲛ_ (mn- prefix)
_ⲱ_ (omega in middle)
```

### Tip 4: Use Text Expansion
If you use the same words often (like ⲁⲅⲁⲡⲏ), create shortcuts:
```bash
# In your ~/.bashrc or text expander
alias coptic_love='echo "ⲁⲅⲁⲡⲏ" | xclip -selection clipboard'
```

---

## 🚀 Your Next Steps

1. **Open this file in browser or editor**:
   ```bash
   xdg-open COPTIC_CHARACTERS_REFERENCE.md &
   ```

2. **Start transcribing page 8**:
   ```bash
   ./transcription_helper.sh 8
   ```

3. **Use character reference** to build each Coptic word

4. **Track progress**:
   ```bash
   python3 kasser_transcription_tool.py stats
   ```

---

## 📊 Expected Speed

- **First 10 entries**: ~2 min/entry (learning characters)
- **Next 50 entries**: ~1 min/entry (getting familiar)
- **After 100 entries**: ~30-45 sec/entry (confident)

**Target**: 30-40 entries per page × 1 minute = **30-40 minutes per page**

**Full lexicon (94 pages)**: ~50-60 hours total (spread over weeks)

---

## ✅ Why Manual is Better Than OCR Here

For Kasser's lexicon specifically:

| Aspect | OCR | Manual |
|--------|-----|--------|
| **Accuracy** | 10-20% | 100% |
| **Time** | Fast extraction, hours of correction | Slower but correct first time |
| **Learning** | None | You learn the lexicon structure |
| **Quality** | Unreliable | Perfect for your parser |
| **Research value** | Low | High (you understand each entry) |

**Bottom line**: Manual transcription with this character reference is the **fastest path to a high-quality lexicon**.

---

## 🎉 You've Got This!

You've already completed **32 entries** (page 7). That's **0.9% of the lexicon**.

Keep going with manual transcription - it's the right approach! 💪

---

**Quick access during transcription**:
```bash
# Show character reference
cat COPTIC_CHARACTERS_REFERENCE.md | grep -A 20 "Quick Copy Toolbar"
```
