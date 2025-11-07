#!/usr/bin/env python3
"""
Coptic Dependency Parser with GUI, dependency graphs and tables

Author: André Linden (2025)
email: linden@bluewin.ch


This parser is licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/

Warning: this program is still at an experimental stage. Use it at your own risks!

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
import atexit
from coptic_text_normalizer import CopticTextNormalizer

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

        # Initialize text normalizer for handling combining diacritics
        self.text_normalizer = CopticTextNormalizer(mode='strip')

        # Initialize Prolog engine for grammatical validation
        try:
            from coptic_prolog_rules import create_prolog_engine
            self.prolog = create_prolog_engine()
            # Register cleanup handler to run at exit
            if self.prolog and hasattr(self.prolog, 'cleanup'):
                atexit.register(self.prolog.cleanup)
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

        # Set up proper cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Handle window close event with proper Prolog cleanup"""
        try:
            if self.prolog and hasattr(self.prolog, 'cleanup'):
                self.prolog.cleanup()
        except Exception as e:
            print(f"Warning during cleanup: {e}")
        finally:
            # Ensure the GUI closes even if cleanup fails
            self.root.quit()
            self.root.destroy()
            sys.exit(0)

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
        
        quit_btn = tk.Button(control_frame, text="Quit", command=self.on_closing,
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
        info_frame = ttk.LabelFrame(parent, text="Dependency Table Export", padding=20)
        info_frame.pack(fill=tk.BOTH, expand=True)

        # Brief, functional description
        info_text = """Dependency Table Export

Export parsed results in multiple formats:
• HTML - Interactive web viewing
• PDF - Publication-ready document
        """

        info_label = tk.Label(info_frame, text=info_text, font=("Arial", 11),
                             justify=tk.LEFT, fg="#333")
        info_label.pack(pady=(10, 20))

        # Button frame for multiple export options
        button_frame = ttk.Frame(info_frame)
        button_frame.pack(pady=10)

        # HTML export button
        self.html_button = tk.Button(button_frame, text="📄 Export to HTML & Open",
                                    command=self.open_html_viewer, font=("Arial", 11, "bold"),
                                    bg="#2196F3", fg="white", height=2, width=22, state=tk.DISABLED)
        self.html_button.pack(side=tk.LEFT, padx=5)

        # PDF export button
        self.pdf_button = tk.Button(button_frame, text="📕 Export to PDF",
                                   command=self.export_to_pdf, font=("Arial", 11, "bold"),
                                   bg="#E91E63", fg="white", height=2, width=22, state=tk.DISABLED)
        self.pdf_button.pack(side=tk.LEFT, padx=5)

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

        # Check if already loaded
        if self.nlp is not None and hasattr(self, 'diaparser'):
            return

        # Determine which parser to use first
        from config import get_diaparser_model_path
        model_path = get_diaparser_model_path()

        # Decide on processors based on whether we have DiaParser
        if model_path:
            # We have DiaParser, so Stanza only needs tokenize,pos
            processors = 'tokenize,pos,lemma'
            print(f"✓ Loading DiaParser model from: {model_path}")
        else:
            # No DiaParser, use Stanza for everything including dependency parsing
            processors = 'tokenize,pos,lemma,depparse'
            print("ℹ DiaParser model not found. Using Stanza's built-in dependency parser.")
            print("  See config.py or run 'python config.py' for setup instructions.")

        # Load Stanza pipeline with appropriate processors
        if self.nlp is None:
            print(f"✓ Loading Stanza pipeline with processors: {processors}")
            try:
                # Try to load with existing resources first
                self.nlp = stanza.Pipeline(
                    lang='cop',
                    processors=processors,
                    download_method=None,
                    verbose=False
                )
            except (KeyError, FileNotFoundError) as e:
                # Resources not found, try downloading
                print("ℹ Stanza resources not found. Downloading...")
                try:
                    stanza.download('cop', verbose=False)
                    self.nlp = stanza.Pipeline(
                        lang='cop',
                        processors=processors,
                        verbose=False
                    )
                except Exception as download_error:
                    raise Exception(
                        f"Failed to load Stanza models. Please run: python3 -c \"import stanza; stanza.download('cop')\"\n"
                        f"Error: {download_error}"
                    ) from download_error

        # Load DiaParser if available
        if not hasattr(self, 'diaparser'):
            if model_path:
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

                try:
                    self.diaparser = Parser.load(model_path)
                    print("✓ DiaParser loaded successfully")
                except Exception as e:
                    print(f"⚠️  Warning: Failed to load DiaParser model: {e}")
                    print("  Falling back to Stanza's dependency parser")
                    self.diaparser = None
            else:
                # No model path, use Stanza
                self.diaparser = None
    
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
        print(f"\n[DEBUG] do_parse called with text: {text[:50]}...")
        try:
            print("[DEBUG] Loading parser...")
            self.load_parser()
            print("[DEBUG] Parser loaded successfully")

            # Step 0: Normalize text (remove combining diacritics that cause <UNK> tokens)
            analysis = self.text_normalizer.analyze_text(text)
            normalized_text = analysis['normalized_text']

            # Track if normalization was applied
            normalization_applied = analysis['has_issues']

            # Step 1: Tokenization using Stanza (keeps sentences separate)
            doc_tok = self.nlp(normalized_text)

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

                # Parse this sentence with diaparser (if available) or use Stanza's results
                if self.diaparser is not None:
                    # Use DiaParser for dependency parsing
                    parsed_result = self.diaparser.predict([tokens], prob=False, verbose=False)
                    parsed_sentence = parsed_result.sentences[0]

                    # Extract dependency information
                    heads = parsed_sentence.values[6]
                    deprels = parsed_sentence.values[7]
                else:
                    # Use Stanza's dependency parsing results (already parsed)
                    heads = [word.head for word in stanza_sentence.words]
                    deprels = [word.deprel for word in stanza_sentence.words]

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

            # Show normalization info if applied
            if normalization_applied:
                results.append(f"\n⚙ Text Normalization Applied:")
                results.append(f"  Combining diacritical marks removed: {analysis['count']}")
                word_mapping = self.text_normalizer.create_mapping(text, normalized_text)
                if word_mapping and len(word_mapping) <= 10:
                    results.append(f"  Words normalized: {', '.join([f'{orig}→{norm}' for orig, norm in word_mapping])}")
                elif word_mapping:
                    results.append(f"  Words normalized: {len(word_mapping)} words affected")
                results.append(f"  Note: This prevents <UNK> tokens in the output")

            results.append(f"\nTotal sentences: {len(parsed_sentences)}")
            results.append(f"Total tokens: {sum(len(s.words) for s in parsed_sentences)}")
            results.append("\n" + "="*70)
            results.extend(all_results)
            results.append("\n" + "="*70)
            if self.diaparser is not None:
                results.append("\nNote: POS tags and lemmas provided by Stanza. Dependency parsing by DiaParser.")
            else:
                results.append("\nNote: All processing (tokenization, POS, lemmatization, dependency parsing) by Stanza.")
            results.append("Use the Dependency Graph tab to view individual sentence trees with navigation.")

            self.root.after(0, self.update_results, "\n".join(results), doc)

        except Exception as e:
            import traceback
            error_msg = str(e)
            print(f"\n[DEBUG] Exception in do_parse: {error_msg}")
            traceback.print_exc()
            print("[DEBUG] Calling show_error...")
            self.root.after(0, self.show_error, error_msg)
    
    def update_results(self, results, doc):
        print(f"\n[DEBUG] update_results called with {len(results)} characters")
        try:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, results)
            self.output_text.see(tk.END)  # Scroll to bottom
            print("[DEBUG] Output text updated successfully")
        except Exception as e:
            print(f"[DEBUG] Error updating output: {e}")
            import traceback
            traceback.print_exc()

        # Draw tree visualization for first sentence
        if doc.sentences:
            self.current_sentence_idx = 0
            self.update_graph_navigation()
            self.draw_dependency_tree(doc.sentences[0])

        # Enable HTML and PDF export
        self.html_button.config(state=tk.NORMAL)
        self.pdf_button.config(state=tk.NORMAL)
        self.viewer_status.config(text="✓ Ready to export (HTML or PDF)", fg="#4CAF50")

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

    def export_to_pdf(self):
        """Export dependency analysis to PDF"""
        if not self.current_doc:
            messagebox.showwarning("Warning", "No parsed data available. Parse text first.")
            return

        try:
            # Try to import weasyprint
            try:
                from weasyprint import HTML, CSS
                weasyprint_available = True
            except ImportError:
                weasyprint_available = False
                messagebox.showerror(
                    "WeasyPrint Not Installed",
                    "PDF export requires WeasyPrint.\n\n"
                    "Install it with:\n"
                    "pip install weasyprint\n\n"
                    "Or use 'Export to HTML' instead."
                )
                return

            # Generate HTML content
            html_content = self.generate_html_viewer(self.current_doc)

            # Save PDF file
            pdf_file = Path("coptic_dependency_analysis.pdf")

            # Show progress
            self.viewer_status.config(text="⏳ Generating PDF...", fg="#FF9800")
            self.root.update()

            # Convert HTML to PDF using WeasyPrint
            HTML(string=html_content).write_pdf(
                pdf_file,
                stylesheets=[CSS(string="""
                    @page {
                        size: A4;
                        margin: 2cm;
                    }
                """)]
            )

            # Open PDF file
            import os
            import platform
            system = platform.system()

            if system == "Darwin":  # macOS
                os.system(f'open "{pdf_file.absolute()}"')
            elif system == "Windows":
                os.startfile(pdf_file.absolute())
            else:  # Linux and others
                os.system(f'xdg-open "{pdf_file.absolute()}"')

            # Update status
            self.viewer_status.config(
                text=f"✓ PDF exported to: {pdf_file.name}",
                fg="#4CAF50"
            )

            messagebox.showinfo(
                "PDF Export Successful",
                f"Dependency analysis exported to:\n{pdf_file.absolute()}\n\n"
                "The PDF has been opened in your default PDF viewer."
            )

        except Exception as e:
            self.viewer_status.config(
                text="❌ PDF export failed",
                fg="#f44336"
            )
            messagebox.showerror("Error", f"Failed to export PDF: {e}\n\nTry using 'Export to HTML' instead.")

    def show_error(self, error_msg):
        print(f"[DEBUG] show_error called: {error_msg}")
        messagebox.showerror("Error", f"Parsing failed: {error_msg}")
        self.parse_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = CopticParserGUI(root)

    def signal_handler(sig, frame):
        """Handle Ctrl+C by calling proper cleanup"""
        print("\nInterrupted by user, cleaning up...")
        app.on_closing()

    signal.signal(signal.SIGINT, signal_handler)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, cleaning up...")
        app.on_closing()
