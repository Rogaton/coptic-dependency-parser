#!/usr/bin/env python3
"""
Configuration Module for Coptic Dependency Parser
==================================================

Manages paths to external models and dependencies.
This allows users to configure where models are located without
modifying the main code.

Author: Coptic NLP Project
License: CC BY-NC-SA 4.0
"""

import os
from pathlib import Path

# ===================================================================
# MODEL PATH CONFIGURATION
# ===================================================================

def get_diaparser_model_path():
    """
    Get the path to the DiaParser model for Coptic.

    Priority order:
    1. Environment variable COPTIC_DIAPARSER_MODEL
    2. Local model file in project directory
    3. Default fallback to external location (if exists)
    4. None (will use Stanza's built-in model)

    Returns:
        str or None: Path to model file, or None if not found
    """
    # Check environment variable first
    env_path = os.environ.get('COPTIC_DIAPARSER_MODEL')
    if env_path and Path(env_path).exists():
        return env_path

    # Check for local model in project directory
    script_dir = Path(__file__).parent
    local_model = script_dir / 'models' / 'cop.diaparser'
    if local_model.exists():
        return str(local_model)

    # Check in standard models directory
    models_dir = script_dir / 'models'
    if (models_dir / 'cop.diaparser').exists():
        return str(models_dir / 'cop.diaparser')

    # Check legacy external path (if available on this system)
    # Note: This path is system-specific and won't exist for most users
    external_path = Path('/home/aldn/NLP/coptic-nlp/lib/cop.diaparser')
    if external_path.exists():
        print(f"ℹ Note: Using model from external location (system-specific)")
        print(f"   Location: {external_path}")
        print(f"   For portable setup, copy to: {models_dir}/cop.diaparser")
        print(f"   This message is specific to your system - other users will see different paths.")
        return str(external_path)

    # No model found - will fall back to Stanza
    return None


def get_coptic_nlp_path():
    """
    Get the path to coptic-nlp module (CopticScriptorium's tools).

    This is only needed for the simple wrapper tool.

    Priority order:
    1. Environment variable COPTIC_NLP_PATH
    2. Default external location (if exists)
    3. None (user needs to install)

    Returns:
        str or None: Path to coptic-nlp directory, or None if not found
    """
    # Check environment variable first
    env_path = os.environ.get('COPTIC_NLP_PATH')
    if env_path and Path(env_path).exists():
        return env_path

    # Check legacy external path
    external_path = Path('/home/aldn/NLP/coptic-nlp')
    if external_path.exists():
        return str(external_path)

    return None


# ===================================================================
# USAGE INSTRUCTIONS
# ===================================================================

def print_model_setup_instructions():
    """Print instructions for setting up models"""
    print("="*70)
    print("Coptic Dependency Parser - Model Configuration")
    print("="*70)
    print()
    print("This parser requires trained models for dependency parsing.")
    print()
    print("OPTION 1: Use Stanza's built-in models (Recommended)")
    print("-" * 70)
    print("  The parser will automatically use Stanza's Coptic models.")
    print("  No additional setup required!")
    print()
    print("OPTION 2: Use CopticScriptorium's DiaParser model")
    print("-" * 70)
    print("  1. Obtain the 'cop.diaparser' model from CopticScriptorium")
    print("  2. Place it in: ./models/cop.diaparser")
    print("  3. Or set environment variable:")
    print("     export COPTIC_DIAPARSER_MODEL=/path/to/cop.diaparser")
    print()
    print("Current Configuration (specific to this system):")
    print("-" * 70)
    diaparser_path = get_diaparser_model_path()
    if diaparser_path:
        # Check if it's a local or external path
        if 'models/' in str(diaparser_path):
            print(f"  ✓ DiaParser model found in local directory")
            print(f"    Path: {diaparser_path}")
        else:
            print(f"  ✓ DiaParser model found (external/legacy location)")
            print(f"    This is system-specific - other users will have different paths")
    else:
        print(f"  ℹ No external DiaParser model found")
        print(f"    Will use Stanza's built-in Coptic dependency parser")
    print()
    print("Note: Model paths are user-specific and not stored in Git.")
    print("="*70)


if __name__ == "__main__":
    # When run directly, show configuration status
    print_model_setup_instructions()
