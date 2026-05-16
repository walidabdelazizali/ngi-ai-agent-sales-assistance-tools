"""
comparison_formatter.py — Plan comparison summaries with deterministic formatting.

Handles comparison formatting for both English and Arabic outputs.
"""

from typing import Any, Optional
import re

from src.output.shared_helpers import (
    _MISSING,
    _SAFE_REFUSAL,
    COMPARISON_FIELDS,
    ENGLISH_LABELS,
    assert_approved,
    build_comparison_line,
    clean_aed,
    clean_utf8,
    extract_core_fields,
    join_lines,
)


def english_comparison_summary(comparison_message: str) -> str:
    """
    Clean and standardize English comparison output.
    
    Removes duplicate AED markers, normalizes spacing.
    """
    if not comparison_message:
        return _SAFE_REFUSAL
    
    lines = comparison_message.splitlines()
    if not lines:
        return _SAFE_REFUSAL
    
    out = []
    
    for i, line in enumerate(lines):
        if i == 0:
            # Header line: clean plan names
            m = re.match(r"Comparison between (.+) and (.+):", line)
            if m:
                p1 = clean_utf8(m.group(1))
                p2 = clean_utf8(m.group(2))
                out.append(f"Comparison between {p1} and {p2}:")
            else:
                out.append(clean_utf8(line))
        elif ":" in line and "|" in line:
            # Comparison row
            label, rest = line.split(":", 1)
            label = label.strip()
            vals = rest.split("|")
            
            if len(vals) == 2:
                v1 = vals[0].split(":", 1)[-1].strip()
                v2 = vals[1].split(":", 1)[-1].strip()
                
                # Clean UTF-8 artifacts
                v1 = clean_utf8(v1)
                v2 = clean_utf8(v2)
                
                # Clean AED duplications
                v1 = clean_aed(v1)
                v2 = clean_aed(v2)
                
                out.append(f"{label}: {v1} | {v2}")
            else:
                out.append(clean_utf8(line))
        else:
            # Other lines
            if line.strip():
                out.append(clean_utf8(line))
    
    result = join_lines(out, separator="\n")
    return result if result else _SAFE_REFUSAL


def comparison_summary(comparison_message: str, language: str = "en") -> str:
    """
    Format comparison summary in specified language.
    
    Handles both English and Arabic formatting.
    """
    if not comparison_message:
        return _SAFE_REFUSAL
    
    if language.lower() == "ar":
        # Arabic formatting is in arabic_formatter.py
        # This is a pass-through to maintain separation
        return english_comparison_summary(comparison_message)
    
    return english_comparison_summary(comparison_message)
