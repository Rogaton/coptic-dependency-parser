#!/usr/bin/env python3
"""
Coptic Dependency Parser - Complete GUI with Table + Graph Views

For Coptic researchers and students - easy access to CopticScriptorium NLP tools

===============================================================================
CREDITS AND ATTRIBUTION
===============================================================================

This parser integrates multiple open-source NLP tools and models:

1. COPTIC SCRIPTORIUM (https://copticscriptorium.org/)
   - Coptic NLP models and linguistic resources
   - Citation: Zeldes & Schroeder (2016). "An NLP Pipeline for Coptic"

2. STANZA - Stanford NLP Library (https://stanfordnlp.github.io/stanza/)
   - Tokenization and POS tagging for Coptic
   - Citation: Qi et al. (2020). "Stanza: A Python NLP Toolkit for Many Languages"
   - License: Apache 2.0

3. DIAPARSER - Biaffine Dependency Parser (https://github.com/Unipisa/diaparser)
   - Neural dependency parsing implementation
   - Citation: Attardi et al. (2009)
   - License: Apache 2.0

4. STANFORD CORENLP (https://stanfordnlp.github.io/CoreNLP/)
   - Neural dependency parsing architecture
   - Citation: Manning et al. (2014), Dozat & Manning (2017)
   - License: GPL v3+

For detailed attribution, see CREDITS_AND_ATTRIBUTION.md

===============================================================================
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import stanza
import threading
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import webbrowser
from pathlib import Path
import signal
import sys

# Fix PyTorch 2.6+ compatibility and __getitems__ error
import torch
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

# Set matplotlib to use fonts that support Coptic Unicode
plt.rcParams['font.family'] = ['Noto Sans Coptic', 'DejaVu Sans', 'sans-serif']

class CopticParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coptic NLP Tools - Parser & Dependency Analyzer")
        self.root.geometry("1200x800")

        self.nlp = None
        self.current_doc = None
        self.current_sentence_idx = 0  # For navigating between sentences in graph view

        # Initialize Prolog engine for grammatical validation
        try:
            from coptic_prolog_rules import create_prolog_engine
            self.prolog = create_prolog_engine()
        except Exception as e:
            print(f"Warning: Prolog integration not available: {e}")
            self.prolog = None

        # Coptic alphabet
        self.coptic_chars = [
            'ⲁ', 'ⲃ', 'ⲅ', 'ⲇ', 'ⲉ', 'ⲍ', 'ⲏ', 'ⲑ', 'ⲓ', 'ⲕ',
            'ⲗ', 'ⲙ', 'ⲛ', 'ⲝ', 'ⲟ', 'ⲡ', 'ⲣ', 'ⲥ', 'ⲧ', 'ⲩ',
            'ⲫ', 'ⲭ', 'ⲯ', 'ⲱ', 'ϣ', 'ϥ', 'ϧ', 'ϩ', 'ϫ', 'ϭ', 'ϯ'
        ]
        
        # Simple Coptic to Latin transliteration map
        self.coptic_to_latin = {
            'ⲁ': 'a', 'ⲃ': 'b', 'ⲅ': 'g', 'ⲇ': 'd', 'ⲉ': 'e', 'ⲍ': 'z', 
            'ⲏ': 'h', 'ⲑ': 'th', 'ⲓ': 'i', 'ⲕ': 'k', 'ⲗ': 'l', 'ⲙ': 'm', 
            'ⲛ': 'n', 'ⲝ': 'x', 'ⲟ': 'o', 'ⲡ': 'p', 'ⲣ': 'r', 'ⲥ': 's', 
            'ⲧ': 't', 'ⲩ': 'u', 'ⲫ': 'f', 'ⲭ': 'ch', 'ⲯ': 'ps', 'ⲱ': 'w',
            'ϣ': 'sh', 'ϥ': 'f', 'ϧ': 'q', 'ϩ': 'h', 'ϫ': 'j', 'ϭ': 'c', 'ϯ': 'ti'
        }
        
        self.setup_gui()
    
    def transliterate_coptic(self, coptic_text):
        """Convert Coptic text to Latin transliteration"""
        result = ""
        for char in coptic_text:
            result += self.coptic_to_latin.get(char, char)
        return result
    
    def setup_gui(self):
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Text analysis tab
        text_frame = ttk.Frame(notebook)
        notebook.add(text_frame, text="📝 Parse Text")
        
        # Dependency graph tab
        graph_frame = ttk.Frame(notebook)
        notebook.add(graph_frame, text="🌳 Dependency Graph")
        
        # HTML table viewer tab
        table_frame = ttk.Frame(notebook)
        notebook.add(table_frame, text="📊 Dependency Table")
        
        self.setup_text_tab(text_frame)
        self.setup_graph_tab(graph_frame)
        self.setup_table_tab(table_frame)
    
    def setup_text_tab(self, parent):
        # Input section
        input_frame = ttk.LabelFrame(parent, text="Input Coptic Text", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.input_text = scrolledtext.ScrolledText(
            input_frame, height=4, font=("Noto Sans Coptic", 14), wrap=tk.WORD
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)
        self.setup_context_menu(self.input_text)
        
        # Virtual keyboard
        keyboard_frame = ttk.LabelFrame(parent, text="Virtual Coptic Keyboard", padding=5)
        keyboard_frame.pack(fill=tk.X, pady=(0, 10))
        
        button_frame = ttk.Frame(keyboard_frame)
        button_frame.pack()
        
        row, col = 0, 0
        for char in self.coptic_chars:
            btn = tk.Button(button_frame, text=char, font=("Noto Sans Coptic", 10),
                           command=lambda c=char: self.insert_char(c), width=2, height=1)
            btn.grid(row=row, column=col, padx=1, pady=1)
            col += 1
            if col > 15:
                col, row = 0, row + 1
        
        # Control buttons
        control_frame = ttk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.parse_button = tk.Button(control_frame, text="🔍 Parse & Analyze Dependencies",
                                     command=self.parse_text, font=("Arial", 12, "bold"),
                                     bg="#4CAF50", fg="white", height=2)
        self.parse_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_btn = tk.Button(control_frame, text="Clear", command=self.clear_input, 
                             font=("Arial", 10), bg="#f44336", fg="white")
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        quit_btn = tk.Button(control_frame, text="Quit", command=self.root.quit, 
                            font=("Arial", 10), bg="#9E9E9E", fg="white")
        quit_btn.pack(side=tk.RIGHT)
        
        # Output section
        output_frame = ttk.LabelFrame(parent, text="Parse Results", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=8, font=("Courier New", 10), wrap=tk.WORD
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.setup_context_menu(self.output_text)
        
        # Sample text - leave empty to avoid parsing errors on startup
        # sample_text = "ⲉⲣϣⲁⲛ ⲧ ⲃⲁϣⲟⲣ"
        # self.input_text.insert(tk.END, sample_text)
    
    def setup_graph_tab(self, parent):
        # Navigation frame for multiple sentences
        nav_frame = ttk.Frame(parent)
        nav_frame.pack(fill=tk.X, padx=10, pady=5)

        self.prev_btn = tk.Button(nav_frame, text="◀ Previous Sentence",
                                  command=self.prev_sentence, state=tk.DISABLED,
                                  font=("Arial", 10))
        self.prev_btn.pack(side=tk.LEFT, padx=5)

        self.sentence_label = tk.Label(nav_frame, text="No sentences parsed yet",
                                       font=("Arial", 10, "bold"))
        self.sentence_label.pack(side=tk.LEFT, expand=True)

        self.next_btn = tk.Button(nav_frame, text="Next Sentence ▶",
                                  command=self.next_sentence, state=tk.DISABLED,
                                  font=("Arial", 10))
        self.next_btn.pack(side=tk.RIGHT, padx=5)

        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, parent)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initial empty plot
        self.ax.text(0.5, 0.5, 'Parse text to see dependency graph',
                    ha='center', va='center', transform=self.ax.transAxes, fontsize=14)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
    
    def setup_table_tab(self, parent):
        # Simple, direct interface for researchers
        info_frame = ttk.LabelFrame(parent, text="Dependency Table (HTML Export)", padding=20)
        info_frame.pack(fill=tk.BOTH, expand=True)

        # Brief, functional description
        info_text = """HTML Dependency Table

Exports parsed results as a formatted HTML table for:
• Detailed linguistic analysis
• Citation in publications
• Integration with other tools
• Archival and sharing
        """

        info_label = tk.Label(info_frame, text=info_text, font=("Arial", 11),
                             justify=tk.LEFT, fg="#333")
        info_label.pack(pady=(10, 20))

        # Simple, functional button
        self.html_button = tk.Button(info_frame, text="Export to HTML & Open",
                                    command=self.open_html_viewer, font=("Arial", 12, "bold"),
                                    bg="#2196F3", fg="white", height=2, state=tk.DISABLED)
        self.html_button.pack(pady=10)

        self.viewer_status = tk.Label(info_frame, text="Parse text first to enable export",
                                     font=("Arial", 10), fg="#666")
        self.viewer_status.pack(pady=(10, 0))
    
    def draw_dependency_tree(self, sentence):
        """Draw dependency tree for a sentence"""
        self.ax.clear()
        
        words = [word.text for word in sentence.words]
        n_words = len(words)
        
        if n_words == 0:
            return
        
        # Position words horizontally
        x_positions = np.linspace(0.1, 0.9, n_words)
        y_word = 0.3
        
        # Draw words and POS tags using transliteration
        for i, (word, x) in enumerate(zip(words, x_positions)):
            # Use transliteration for display
            display_text = self.transliterate_coptic(word)
            
            # Draw word box
            self.ax.text(x, y_word, display_text, ha='center', va='center', 
                        fontsize=12, bbox=dict(boxstyle="round,pad=0.4", 
                                              facecolor="lightblue", edgecolor="blue"))
            
            # Draw POS tags
            pos_tag = sentence.words[i].upos
            self.ax.text(x, y_word - 0.12, pos_tag, ha='center', va='center', 
                        fontsize=10, style='italic', color='darkgreen', weight='bold')
            
            # Draw original Coptic text below (smaller)
            self.ax.text(x, y_word - 0.18, f"({word})", ha='center', va='center',
                        fontsize=8, color='gray')
        
        # Draw dependency arcs
        for i, word in enumerate(sentence.words):
            if word.head > 0:  # Not root
                head_idx = word.head - 1
                
                if head_idx < len(x_positions):  # Safety check
                    x_child = x_positions[i]
                    x_head = x_positions[head_idx]
                    
                    # Calculate arc parameters
                    distance = abs(i - head_idx)
                    arc_height = 0.25 + 0.05 * distance
                    
                    # Draw the arc using a simple curved line
                    if x_child != x_head:
                        # Create arc points
                        n_points = 30
                        t = np.linspace(0, 1, n_points)
                        
                        # Bezier curve points
                        x_arc = x_child * (1-t) + x_head * t
                        y_arc = y_word + 0.08 + 4 * arc_height * t * (1-t)
                        
                        # Draw the arc
                        self.ax.plot(x_arc, y_arc, 'red', linewidth=2.5)
                        
                        # Add arrowhead
                        arrow_offset = 0.03 if x_child < x_head else -0.03
                        self.ax.annotate('', xy=(x_head, y_word + 0.08), 
                                       xytext=(x_head + arrow_offset, y_word + 0.12),
                                       arrowprops=dict(arrowstyle='->', color='red', lw=2.5))
                        
                        # Add relation label
                        label_x = (x_child + x_head) / 2
                        label_y = y_word + 0.08 + arc_height
                        self.ax.text(label_x, label_y, word.deprel, ha='center', va='center',
                                   fontsize=10, bbox=dict(boxstyle="round,pad=0.3", 
                                                         facecolor="yellow", edgecolor="orange"),
                                   weight='bold')
        
        # Mark root
        for i, word in enumerate(sentence.words):
            if word.head == 0:  # Root word
                self.ax.text(x_positions[i], y_word + 0.18, 'ROOT', ha='center', va='center',
                           fontsize=14, color='red', weight='bold',
                           bbox=dict(boxstyle="round,pad=0.3", facecolor="pink", edgecolor="red"))
        
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.set_title(f'Dependency Tree: {sentence.text}', fontsize=16, pad=20, weight='bold')
        self.ax.axis('off')
        
        self.canvas.draw()
    
    def generate_html_viewer(self, doc):
        """Generate HTML viewer from Stanza document"""
        
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Coptic Dependency Analysis</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; border-bottom: 3px solid #4CAF50; padding-bottom: 15px; }
        .sentence { margin: 25px 0; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #fafafa; }
        .sentence-text { font-size: 20px; font-weight: bold; margin-bottom: 15px; color: #2c3e50; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #4CAF50; color: white; font-weight: bold; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .root { background-color: #e8f5e8 !important; font-weight: bold; }
        .coptic { font-family: 'Noto Sans Coptic', 'Antinoou', serif; font-size: 16px; }
        .stats { background: linear-gradient(135deg, #e8f5e8, #c8e6c9); padding: 15px; border-radius: 8px; margin-bottom: 25px; text-align: center; font-size: 16px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Coptic Dependency Analysis</h1>
"""
        
        # Add statistics
        total_sentences = len(doc.sentences)
        total_tokens = sum(len(sent.words) for sent in doc.sentences)
        
        html += f"""
        <div class="stats">
            <strong>Analysis Results:</strong> {total_sentences} sentences | {total_tokens} tokens
        </div>
"""
        
        # Add each sentence
        for i, sentence in enumerate(doc.sentences, 1):
            html += f"""
        <div class="sentence">
            <div class="sentence-text coptic">Sentence {i}: {sentence.text}</div>
            <table>
                <tr>
                    <th>ID</th><th>Form</th><th>Lemma</th><th>UPOS</th>
                    <th>Head</th><th>Dependency</th><th>Features</th>
                </tr>
"""
            
            for word in sentence.words:
                is_root = word.head == 0
                head_text = 'ROOT' if is_root else sentence.words[word.head-1].text
                row_class = 'root' if is_root else ''
                feats = word.feats if word.feats else ''
                
                html += f"""
                <tr class="{row_class}">
                    <td><strong>{word.id}</strong></td>
                    <td class="coptic"><strong>{word.text}</strong></td>
                    <td class="coptic">{word.lemma or '_'}</td>
                    <td><span style="background:#e3f2fd;padding:3px 6px;border-radius:3px">{word.upos}</span></td>
                    <td class="coptic"><strong>{head_text}</strong></td>
                    <td><span style="background:#fff3e0;padding:3px 6px;border-radius:3px">{word.deprel}</span></td>
                    <td style="font-size:12px">{feats}</td>
                </tr>"""
            
            html += "</table></div>"
        
        html += """
        <div style="text-align: center; margin-top: 30px; padding: 15px; background: #f0f0f0; border-radius: 8px;">
            <p style="color: #666; margin: 0;">Generated by Coptic NLP Tools - CopticScriptorium Project</p>
        </div>
        </div>
    </body>
    </html>"""
        
        return html
    
    def setup_context_menu(self, widget):
        context_menu = tk.Menu(widget, tearoff=0)
        context_menu.add_command(label="Copy", command=lambda: widget.event_generate("<<Copy>>"))
        context_menu.add_command(label="Paste", command=lambda: widget.event_generate("<<Paste>>"))
        context_menu.add_command(label="Select All", command=lambda: widget.tag_add(tk.SEL, "1.0", tk.end))
        
        def show_context_menu(event):
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
        
        widget.bind("<Button-3>", show_context_menu)
    
    def insert_char(self, char):
        self.input_text.insert(tk.INSERT, char)
        self.input_text.focus_set()

    def clear_input(self):
        self.input_text.delete(1.0, tk.END)

    def prev_sentence(self):
        """Navigate to previous sentence in graph view"""
        if self.current_doc and self.current_sentence_idx > 0:
            self.current_sentence_idx -= 1
            self.update_graph_navigation()
            self.draw_dependency_tree(self.current_doc.sentences[self.current_sentence_idx])

    def next_sentence(self):
        """Navigate to next sentence in graph view"""
        if self.current_doc and self.current_sentence_idx < len(self.current_doc.sentences) - 1:
            self.current_sentence_idx += 1
            self.update_graph_navigation()
            self.draw_dependency_tree(self.current_doc.sentences[self.current_sentence_idx])

    def update_graph_navigation(self):
        """Update navigation buttons and label"""
        if not self.current_doc or len(self.current_doc.sentences) == 0:
            self.sentence_label.config(text="No sentences parsed yet")
            self.prev_btn.config(state=tk.DISABLED)
            self.next_btn.config(state=tk.DISABLED)
            return

        total = len(self.current_doc.sentences)
        current = self.current_sentence_idx + 1
        self.sentence_label.config(text=f"Sentence {current} of {total}")

        # Enable/disable navigation buttons
        self.prev_btn.config(state=tk.NORMAL if self.current_sentence_idx > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.current_sentence_idx < total - 1 else tk.DISABLED)
    
    def load_parser(self):
        # Using Stanza for tokenization instead of coptic-nlp to avoid compatibility issues
        import warnings
        warnings.filterwarnings('ignore')

        if self.nlp is None:
            # Load Stanza pipeline for Coptic tokenization and POS tagging
            self.nlp = stanza.Pipeline(
                lang='cop',
                processors='tokenize,pos',  # Added POS tagging
                download_method=None,
                verbose=False
            )

        # Load diaparser for dependency parsing
        if not hasattr(self, 'diaparser'):
            import sys
            sys.path.insert(0, '/home/aldn/NLP/coptic-nlp')

            # The torch patch was already applied at module level (lines 50-73)

            from diaparser.parsers.parser import Parser

            # Fix DiaParser __getitems__ compatibility issue with PyTorch DataLoader
            if not hasattr(self, '_diaparser_patched'):
                from diaparser.utils.data import Dataset
                from diaparser.utils.transform import Sentence

                # Patch Dataset to handle __getitems__ check
                original_dataset_getattr = Dataset.__getattr__

                def patched_dataset_getattr(self_inner, name):
                    """Patched __getattr__ to handle PyTorch DataLoader checks"""
                    if name in ('__getitems__', '__getitem__', '_is_protocol'):
                        raise AttributeError(f"'{type(self_inner).__name__}' object has no attribute '{name}'")
                    return original_dataset_getattr(self_inner, name)

                Dataset.__getattr__ = patched_dataset_getattr

                # Patch Sentence to handle __getitems__ check
                original_sentence_getattr = Sentence.__getattr__

                def patched_sentence_getattr(self_inner, name):
                    """Patched __getattr__ to handle PyTorch DataLoader checks"""
                    if name in ('__getitems__', '__getitem__', '_is_protocol'):
                        raise AttributeError(f"'{type(self_inner).__name__}' object has no attribute '{name}'")
                    return original_sentence_getattr(self_inner, name)

                Sentence.__getattr__ = patched_sentence_getattr
                self._diaparser_patched = True

            self.diaparser = Parser.load('/home/aldn/NLP/coptic-nlp/lib/cop.diaparser')
    
    def parse_text(self):
        input_text = self.input_text.get(1.0, tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("Warning", "Please enter some Coptic text to parse.")
            return
        
        self.parse_button.config(state=tk.DISABLED)
        
        thread = threading.Thread(target=self.do_parse, args=(input_text,))
        thread.daemon = True
        thread.start()
    
    def do_parse(self, text):
        try:
            self.load_parser()

            # Step 1: Tokenization using Stanza (keeps sentences separate)
            doc_tok = self.nlp(text)

            if len(doc_tok.sentences) == 0:
                raise ValueError("No sentences were parsed from the input.")

            # Step 2: Parse each sentence separately
            import warnings
            warnings.filterwarnings('ignore')

            parsed_sentences = []
            all_results = []

            for sent_idx, stanza_sentence in enumerate(doc_tok.sentences, 1):
                # Extract words, POS tags, and lemmas from Stanza
                # Note: Using words (not tokens) for consistent linguistic units
                tokens = [word.text for word in stanza_sentence.words]
                pos_tags = [word.upos for word in stanza_sentence.words]
                lemmas = [word.lemma if word.lemma else word.text for word in stanza_sentence.words]

                if not tokens:
                    continue

                # Parse this sentence with diaparser
                parsed_result = self.diaparser.predict([tokens], prob=False, verbose=False)
                parsed_sentence = parsed_result.sentences[0]

                # Extract dependency information
                heads = parsed_sentence.values[6]
                deprels = parsed_sentence.values[7]

                # Create word objects for this sentence
                words = []
                for word_id, (token, head, deprel, pos, lemma) in enumerate(zip(tokens, heads, deprels, pos_tags, lemmas), start=1):
                    word_obj = type('Word', (), {
                        'id': word_id,
                        'text': token,
                        'lemma': lemma,  # lemma from Stanza
                        'upos': pos,     # POS tag from Stanza
                        'head': head,
                        'deprel': deprel,
                        'feats': ''
                    })()
                    words.append(word_obj)

                # Create sentence object
                sentence_text = stanza_sentence.text
                sentence_obj = type('Sentence', (), {
                    'text': sentence_text,
                    'words': words
                })()
                parsed_sentences.append(sentence_obj)

                # Format results for this sentence
                all_results.append(f"\n{'='*70}")
                all_results.append(f"SENTENCE {sent_idx}: {sentence_text}")
                all_results.append('='*70)
                all_results.append("\nDependency Structure:")
                all_results.append('-'*70)

                for word in words:
                    if word.head == 0:
                        head_text = "ROOT"
                    else:
                        head_text = words[word.head-1].text if word.head <= len(words) else "?"
                    all_results.append(f"  {word.text:15} ({word.upos:6}) --{word.deprel:10}--> {head_text:15}")

                all_results.append(f"\nTokens in sentence: {len(words)}")

                # Prolog validation (if available)
                if self.prolog and self.prolog.prolog_initialized:
                    validation = self.prolog.validate_parse_tree(tokens, pos_tags, heads, deprels)

                    # Check for tripartite pattern
                    if validation.get("patterns_found"):
                        for pattern in validation["patterns_found"]:
                            if pattern.get("is_tripartite"):
                                all_results.append(f"\n✓ Prolog: {pattern['description']} detected")
                                all_results.append(f"  Pattern: {pattern['pattern']}")

                    # Show warnings if any
                    if validation.get("warnings"):
                        all_results.append(f"\n⚠ Prolog Warnings:")
                        for warning in validation["warnings"]:
                            all_results.append(f"  - {warning}")

            # Create doc object with all sentences
            doc = type('Doc', (), {
                'sentences': parsed_sentences
            })()

            self.current_doc = doc
            self.current_sentence_idx = 0  # Reset to first sentence

            # Format overall summary
            results = []
            results.append(f"Input text parsed successfully!")
            results.append(f"Total sentences: {len(parsed_sentences)}")
            results.append(f"Total tokens: {sum(len(s.words) for s in parsed_sentences)}")
            results.append("\n" + "="*70)
            results.extend(all_results)
            results.append("\n" + "="*70)
            results.append("\nNote: POS tags and lemmas provided by Stanza. Dependency parsing by DiaParser.")
            results.append("Use the Dependency Graph tab to view individual sentence trees with navigation.")

            self.root.after(0, self.update_results, "\n".join(results), doc)

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.root.after(0, self.show_error, str(e))
    
    def update_results(self, results, doc):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, results)

        # Draw tree visualization for first sentence
        if doc.sentences:
            self.current_sentence_idx = 0
            self.update_graph_navigation()
            self.draw_dependency_tree(doc.sentences[0])

        # Enable HTML viewer
        self.html_button.config(state=tk.NORMAL)
        self.viewer_status.config(text="✓ Ready to export", fg="#4CAF50")

        self.parse_button.config(state=tk.NORMAL)
    
    def open_html_viewer(self):
        if not self.current_doc:
            messagebox.showwarning("Warning", "No parsed data available. Parse text first.")
            return

        try:
            # Generate HTML
            html_content = self.generate_html_viewer(self.current_doc)

            # Save to file in current directory
            html_file = Path("coptic_dependency_analysis.html")
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Open in browser directly - no popup
            file_url = f'file://{html_file.absolute()}'
            webbrowser.open(file_url)

            # Update status to show file location (no popup interruption)
            self.viewer_status.config(
                text=f"✓ Exported to: {html_file.name}",
                fg="#4CAF50"
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export HTML table: {e}")
    
    def show_error(self, error_msg):
        messagebox.showerror("Error", f"Parsing failed: {error_msg}")
        self.parse_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    def signal_handler(sig, frame):
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    root = tk.Tk()
    app = CopticParserGUI(root)
    root.mainloop()
