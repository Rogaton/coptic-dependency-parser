# Third-Party Licenses

This directory contains the license texts for all third-party dependencies used in the Coptic Dependency Parser project.

## Purpose

While the original code of the Coptic Dependency Parser is licensed under **CC BY-NC-SA 4.0** (non-commercial), this project depends on several open-source libraries that have their own licenses. This directory documents all third-party licenses to ensure proper attribution and compliance.

## Dependency Licenses

### Core NLP Libraries

| Library | License | File |
|---------|---------|------|
| Stanford Stanza | Apache 2.0 | `Apache-2.0-Stanza.txt` |
| DiaParser | Apache 2.0 | `Apache-2.0-DiaParser.txt` |
| PyTorch | BSD 3-Clause | `BSD-3-PyTorch.txt` |

### Web Interface

| Library | License | File |
|---------|---------|------|
| Gradio | Apache 2.0 | `Apache-2.0-Gradio.txt` |

### Scientific Computing

| Library | License | File |
|---------|---------|------|
| NumPy | BSD 3-Clause | `BSD-3-NumPy.txt` |
| Pandas | BSD 3-Clause | `BSD-3-Pandas.txt` |
| Matplotlib | PSF-based | `Matplotlib-License.txt` |
| SciPy | BSD 3-Clause | `BSD-3-SciPy.txt` |
| Scikit-learn | BSD 3-Clause | `BSD-3-Scikit-learn.txt` |

### Other Dependencies

Additional dependencies listed in `requirements.txt` are covered by permissive open-source licenses (MIT, BSD, Apache 2.0).

## Training Data

### Coptic SCRIPTORIUM

The training data comes from the Coptic SCRIPTORIUM project. For specific licensing information about the corpus, see:
- https://copticscriptorium.org/
- Individual data files in the `data/` directory may contain licensing headers

### Universal Dependencies

The dependency parsing annotations follow the Universal Dependencies standard. See:
- https://universaldependencies.org/

## Important Notes

1. **Dual License Structure**: The Coptic Dependency Parser uses a dual license:
   - Original code by Rogaton: **CC BY-NC-SA 4.0** (non-commercial)
   - Third-party dependencies: **Their original licenses** (documented here)

2. **Commercial Use**: While the dependencies are under permissive licenses (Apache 2.0, BSD), the original parser code is non-commercial. This means:
   - ✓ You can use the dependencies commercially
   - ✗ You cannot use the parser's original code commercially

3. **License Compatibility**: All included licenses are compatible with the CC BY-NC-SA 4.0 license for non-commercial use.

## How to Add New Dependencies

If you add a new dependency to this project:

1. Check the dependency's license
2. Add the license text to this directory as `[LICENSE-TYPE]-[LIBRARY].txt`
3. Update the table above
4. Ensure the license is compatible with CC BY-NC-SA 4.0

## Questions?

For licensing questions, please open an issue at:
https://github.com/Rogaton/coptic-dependency-parser/issues
