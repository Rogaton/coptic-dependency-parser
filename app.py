"""
Coptic Dependency Parser - Hugging Face Space Demo
Built on Coptic SCRIPTORIUM and Stanford NLP tools
"""

import gradio as gr
import stanza
import torch
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Fix PyTorch 2.6+ compatibility and __getitems__ error
import pickle

# Store original torch.load
_original_torch_load = torch.load

def patched_torch_load(*args, **kwargs):
    """Patched torch.load with multiple compatibility fixes"""
    # Set weights_only=False for older models
    kwargs['weights_only'] = False

    try:
        return _original_torch_load(*args, **kwargs)
    except (KeyError, AttributeError) as e:
        if '__getitems__' in str(e) or '__getitem__' in str(e):
            # Try with pickle protocol 4
            print(f"Retrying model load with pickle protocol 4...")
            kwargs['pickle_module'] = pickle
            return _original_torch_load(*args, **kwargs)
        raise

# Apply the patch
torch.load = patched_torch_load

# Import diaparser
sys.path.insert(0, str(Path(__file__).parent))
from diaparser.parsers.parser import Parser

# Fix DiaParser __getitems__ compatibility issue with PyTorch DataLoader
from diaparser.utils.data import Dataset
from diaparser.utils.transform import Sentence

# Patch Dataset to handle __getitems__ check
original_dataset_getattr = Dataset.__getattr__

def patched_dataset_getattr(self, name):
    """Patched __getattr__ to handle PyTorch DataLoader checks"""
    if name in ('__getitems__', '__getitem__', '_is_protocol'):
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    return original_dataset_getattr(self, name)

Dataset.__getattr__ = patched_dataset_getattr

# Patch Sentence to handle __getitems__ check
original_sentence_getattr = Sentence.__getattr__

def patched_sentence_getattr(self, name):
    """Patched __getattr__ to handle PyTorch DataLoader checks"""
    if name in ('__getitems__', '__getitem__', '_is_protocol'):
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    return original_sentence_getattr(self, name)

Sentence.__getattr__ = patched_sentence_getattr

# Global variables for models
nlp = None
diaparser = None
prolog = None


def load_models():
    """Load Stanza, DiaParser, and Prolog models"""
    global nlp, diaparser, prolog

    if nlp is None:
        print("Loading Stanza Coptic model...")
        # Download models if not present
        try:
            stanza.download('cop', verbose=False)
        except:
            pass  # Models might already be downloaded

        nlp = stanza.Pipeline(
            lang='cop',
            processors='tokenize,pos',
            verbose=False
        )
        print("✓ Stanza loaded")

    if diaparser is None:
        print("Loading DiaParser model...")
        diaparser = Parser.load('cop.diaparser')
        print("✓ DiaParser loaded")

    if prolog is None:
        try:
            print("Loading Prolog rule engine...")
            from coptic_prolog_rules import create_prolog_engine
            prolog = create_prolog_engine()
            print("✓ Prolog loaded")
        except Exception as e:
            print(f"⚠️  Prolog not available: {e}")
            prolog = None


def parse_coptic_text(text):
    """
    Parse Coptic text and return formatted results

    Args:
        text: Input Coptic text

    Returns:
        tuple: (text_output, html_table, status_message)
    """
    if not text or not text.strip():
        return "Please enter some Coptic text to parse.", "", "⚠️ No input provided"

    try:
        # Load models if needed
        load_models()

        # Tokenize with Stanza
        doc_tok = nlp(text)

        # Parse each sentence
        all_results = []
        text_output_lines = []

        for sent_idx, stanza_sentence in enumerate(doc_tok.sentences, 1):
            # Extract tokens, POS tags, lemmas
            tokens = [word.text for word in stanza_sentence.words]
            pos_tags = [word.upos for word in stanza_sentence.words]
            lemmas = [word.lemma if word.lemma else word.text for word in stanza_sentence.words]

            # Parse with DiaParser
            parsed_result = diaparser.predict([tokens], prob=False, verbose=False)

            # Build text output for this sentence
            text_output_lines.append(f"\n{'='*60}")
            text_output_lines.append(f"SENTENCE {sent_idx}: {' '.join(tokens)}")
            text_output_lines.append(f"{'='*60}\n")

            # Create word data
            sentence_words = []
            for i, token in enumerate(tokens):
                head_idx = parsed_result.arcs[0][i]
                rel = parsed_result.rels[0][i]
                pos = pos_tags[i] if i < len(pos_tags) else "UNKNOWN"
                lemma = lemmas[i] if i < len(lemmas) else token

                word_data = {
                    'id': i + 1,
                    'form': token,
                    'lemma': lemma,
                    'upos': pos,
                    'head': head_idx,
                    'deprel': rel
                }
                sentence_words.append(word_data)

                # Add to text output
                # Bounds checking for head_idx
                if head_idx == 0:
                    head_word = "ROOT"
                elif 0 < head_idx <= len(tokens):
                    head_word = tokens[head_idx - 1]
                else:
                    head_word = f"INVALID({head_idx})"

                text_output_lines.append(
                    f"  {i+1}. {token:15} → {head_word:15} [{rel}]"
                )
                text_output_lines.append(
                    f"     POS: {pos:10} Lemma: {lemma}"
                )

            # Prolog validation (if available)
            if prolog and prolog.prolog_initialized:
                heads = [word_data['head'] for word_data in sentence_words]
                deprels = [word_data['deprel'] for word_data in sentence_words]

                validation = prolog.validate_parse_tree(tokens, pos_tags, heads, deprels)

                # Check for tripartite pattern
                if validation.get("patterns_found"):
                    for pattern in validation["patterns_found"]:
                        if pattern.get("is_tripartite"):
                            text_output_lines.append(f"\n✓ Prolog: {pattern['description']} detected")
                            text_output_lines.append(f"  Pattern: {pattern['pattern']}")

                # Show warnings if any
                if validation.get("warnings"):
                    text_output_lines.append(f"\n⚠ Prolog Warnings:")
                    for warning in validation["warnings"]:
                        text_output_lines.append(f"  - {warning}")

            all_results.append({
                'sentence_id': sent_idx,
                'text': ' '.join(tokens),
                'words': sentence_words
            })

        # Generate text output
        text_output = '\n'.join(text_output_lines)

        # Generate HTML table
        html_table = generate_html_table(all_results)

        # Status message
        num_sentences = len(doc_tok.sentences)
        num_words = sum(len(sent.words) for sent in doc_tok.sentences)
        status = f"✓ Parsed {num_sentences} sentence(s) with {num_words} words"

        return text_output, html_table, status

    except Exception as e:
        # Detailed error message with traceback for debugging
        import traceback
        error_details = traceback.format_exc()
        print("="*60)
        print("PARSING ERROR:")
        print(error_details)
        print("="*60)

        # User-friendly error message
        error_msg = f"""❌ Parsing Error

Error type: {type(e).__name__}
Details: {str(e)}

This could be due to:
- Very long text (try shorter passages)
- Unusual characters or formatting
- Model limitations

Try:
1. Use the Clear button to reset
2. Parse shorter text segments
3. Check that text is valid Coptic

Technical details printed to console."""

        return error_msg, f"<p style='color:red;'><b>Error:</b> {str(e)}</p>", f"❌ {type(e).__name__}: {str(e)[:100]}"


def generate_html_table(results):
    """Generate HTML table visualization of parse results"""

    html = """
    <style>
        .parse-container { font-family: 'Segoe UI', Arial, sans-serif; }
        .sentence-block {
            margin: 20px 0;
            border: 2px solid #2196F3;
            border-radius: 8px;
            padding: 15px;
            background: #f8f9fa;
        }
        .sentence-header {
            font-size: 1.1em;
            font-weight: bold;
            color: #1976D2;
            margin-bottom: 10px;
        }
        .sentence-text {
            font-size: 1.05em;
            color: #333;
            margin-bottom: 15px;
            padding: 10px;
            background: white;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th {
            background: #2196F3;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }
        td {
            padding: 10px;
            border-bottom: 1px solid #e0e0e0;
        }
        tr:hover { background: #f5f5f5; }
        .word-id { font-weight: bold; color: #1976D2; }
        .word-form { font-weight: 600; color: #333; }
        .pos-tag {
            background: #4CAF50;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.9em;
        }
        .deprel {
            background: #FF9800;
            color: white;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.9em;
        }
    </style>
    <div class="parse-container">
    """

    for result in results:
        sent_id = result['sentence_id']
        sent_text = result['text']
        words = result['words']

        html += f"""
        <div class="sentence-block">
            <div class="sentence-header">Sentence {sent_id}</div>
            <div class="sentence-text">{sent_text}</div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Word</th>
                        <th>Lemma</th>
                        <th>POS</th>
                        <th>Head</th>
                        <th>Relation</th>
                    </tr>
                </thead>
                <tbody>
        """

        for word in words:
            # Bounds checking for head index
            head_idx = word['head']
            if head_idx == 0:
                head_word = "ROOT"
            elif 0 < head_idx <= len(words):
                head_word = words[head_idx - 1]['form']
            else:
                head_word = f"INVALID({head_idx})"

            html += f"""
                    <tr>
                        <td class="word-id">{word['id']}</td>
                        <td class="word-form">{word['form']}</td>
                        <td>{word['lemma']}</td>
                        <td><span class="pos-tag">{word['upos']}</span></td>
                        <td>{head_word} ({word['head']})</td>
                        <td><span class="deprel">{word['deprel']}</span></td>
                    </tr>
            """

        html += """
                </tbody>
            </table>
        </div>
        """

    html += "</div>"
    return html


# Create Gradio interface
with gr.Blocks(title="Coptic Dependency Parser", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # Coptic Dependency Parser

    Neural-symbolic dependency parser for Coptic text with POS tagging, lemmatization, and grammatical validation.

    **Built on:**
    - [Coptic SCRIPTORIUM](https://copticscriptorium.org/) training data
    - [Stanford Stanza](https://stanfordnlp.github.io/stanza/) NLP framework
    - [DiaParser](https://github.com/Unipisa/diaparser) biaffine parser
    - **Prolog rule engine** for Coptic grammatical validation

    **Features:**
    - ✓ Neural dependency parsing
    - ✓ Tripartite sentence pattern detection
    - ✓ Morphological analysis (article stripping)
    - ✓ Grammatical validation with Prolog rules

    **Usage:** Enter Coptic text below and click "Parse" to see dependency analysis.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            input_text = gr.Textbox(
                label="Coptic Text Input",
                placeholder="Enter Coptic text here... (single or multiple sentences)",
                lines=6,
                value="ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ"  # Example: "I am God"
            )

            with gr.Row():
                parse_btn = gr.Button("🔍 Parse Text", variant="primary", size="lg")
                clear_btn = gr.Button("🗑️ Clear", variant="secondary", size="lg")

            status_output = gr.Textbox(label="Status", interactive=False, lines=1)

    with gr.Tabs():
        with gr.Tab("📊 Dependency Table"):
            html_output = gr.HTML(label="Parse Results")

        with gr.Tab("📝 Text Output"):
            text_output = gr.Textbox(
                label="Detailed Parse Output",
                lines=20,
                interactive=False
            )

    gr.Markdown("""
    ---

    ### About

    This parser performs:
    - **Tokenization**: Splits text into sentences and words
    - **POS Tagging**: Identifies parts of speech (NOUN, VERB, etc.)
    - **Lemmatization**: Finds dictionary forms of words
    - **Dependency Parsing**: Analyzes grammatical relationships
    - **Grammatical Validation**: Detects Coptic linguistic patterns (tripartite sentences, etc.)

    ### Citation

    If you use this tool in research, please cite:
    - **Coptic SCRIPTORIUM**: Zeldes, A. & Schroeder, C. T. (2016)
    - **Stanford Stanza**: Qi et al. (2020)
    - **DiaParser**: Attardi et al. (2021)

    ### License

    Apache 2.0

    ---
    **Source Code:** [GitHub](https://github.com/Rogaton/coptic-dependency-parser)
    """)

    # Connect Parse button to parsing function
    parse_btn.click(
        fn=parse_coptic_text,
        inputs=[input_text],
        outputs=[text_output, html_output, status_output]
    )

    # Also parse on Enter key
    input_text.submit(
        fn=parse_coptic_text,
        inputs=[input_text],
        outputs=[text_output, html_output, status_output]
    )

    # Connect Clear button to reset all outputs
    def clear_all():
        return "", "", "", "Ready to parse"

    clear_btn.click(
        fn=clear_all,
        inputs=[],
        outputs=[input_text, text_output, html_output, status_output]
    )


# Launch demo
if __name__ == "__main__":
    print("Starting Coptic Dependency Parser...")
    demo.launch()
