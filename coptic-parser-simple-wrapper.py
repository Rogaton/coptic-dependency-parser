#!/usr/bin/env python3
"""
Simple Coptic Parser with Working GUI
Uses tokenizer-only mode to avoid lemmatization issues
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import sys
import os
sys.path.insert(0, '/home/aldn/NLP/coptic-nlp')

class SimpleCopticParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coptic NLP Tools - Simple Tokenizer & POS Tagger")
        self.root.geometry("900x700")

        self.coptic_chars = [
            'ⲁ', 'ⲃ', 'ⲅ', 'ⲇ', 'ⲉ', 'ⲍ', 'ⲏ', 'ⲑ', 'ⲓ', 'ⲕ',
            'ⲗ', 'ⲙ', 'ⲛ', 'ⲝ', 'ⲟ', 'ⲡ', 'ⲣ', 'ⲥ', 'ⲧ', 'ⲩ',
            'ⲫ', 'ⲭ', 'ⲯ', 'ⲱ', 'ϣ', 'ϥ', 'ϧ', 'ϩ', 'ϫ', 'ϭ', 'ϯ'
        ]

        self.setup_gui()

    def setup_gui(self):
        # Input section
        input_frame = ttk.LabelFrame(self.root, text="Input Coptic Text", padding=10)
        input_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10), padx=10)

        self.input_text = scrolledtext.ScrolledText(
            input_frame, height=4, font=("Noto Sans Coptic", 14), wrap=tk.WORD
        )
        self.input_text.pack(fill=tk.BOTH, expand=True)

        # Virtual keyboard
        keyboard_frame = ttk.LabelFrame(self.root, text="Virtual Coptic Keyboard", padding=5)
        keyboard_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

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
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=10)

        self.parse_button = tk.Button(control_frame, text="🔍 Tokenize & Tag",
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
        output_frame = ttk.LabelFrame(self.root, text="Results", padding=10)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=10)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, height=12, font=("Courier New", 10), wrap=tk.WORD
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)

        # Add sample text
        sample_text = "ⲁⲛⲟⲕ ⲡⲉ ⲡⲛⲟⲩⲧⲉ"
        self.input_text.insert(tk.END, sample_text)

    def insert_char(self, char):
        self.input_text.insert(tk.INSERT, char)
        self.input_text.focus_set()

    def clear_input(self):
        self.input_text.delete(1.0, tk.END)

    def parse_text(self):
        input_text = self.input_text.get(1.0, tk.END).strip()

        if not input_text:
            messagebox.showwarning("Warning", "Please enter some Coptic text to parse.")
            return

        self.parse_button.config(state=tk.DISABLED)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Processing...\n")

        try:
            from coptic_nlp import nlp_coptic

            # Use tokenization and normalization only - more reliable
            result = nlp_coptic(input_text,
                              do_tok=True,           # Tokenization
                              do_norm=True,          # Normalization
                              do_tag=True,           # POS tagging
                              do_lemma=False,        # Skip lemmatization (causes issues)
                              do_parse=False,        # Skip parsing for now
                              do_lang=False,
                              do_mwe=False,
                              sgml_mode="pipes",     # Use pipes mode
                              tok_mode="auto")

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "=== Tokenization & POS Tagging Results ===\n\n")
            self.output_text.insert(tk.END, result)
            self.output_text.insert(tk.END, "\n\n=== Format ===\n")
            self.output_text.insert(tk.END, "Each line shows: WORD | NORMALIZED | POS_TAG\n")

        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}\n\n{traceback.format_exc()}"
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, error_msg)
            messagebox.showerror("Error", f"Parsing failed: {str(e)}")

        finally:
            self.parse_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCopticParserGUI(root)
    root.mainloop()
