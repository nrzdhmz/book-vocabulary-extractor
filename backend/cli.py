"""
Command-line entry to run the vocabulary pipeline without the notebook.

Usage:
    python cli.py --pdf data/raw/book.pdf --min-frequency 2 --out outputs
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from src.pipeline import run_pipeline


def parse_args():
    p = argparse.ArgumentParser(description="Run book vocabulary pipeline.")
    p.add_argument("--pdf", required=True, help="Path to the PDF file.")
    p.add_argument(
        "--min-frequency",
        type=int,
        default=2,
        help="Minimum frequency to keep a token.",
    )
    p.add_argument(
        "--out",
        default="outputs",
        help="Output directory (default: outputs).",
    )
    p.add_argument(
        "--base-name",
        default="ranked_vocabulary",
        help="Base filename for outputs (default: ranked_vocabulary).",
    )
    return p.parse_args()


def main():
    args = parse_args()
    try:
        result = run_pipeline(
            pdf_path=args.pdf,
            min_frequency=args.min_frequency,
            output_dir=args.out,
            base_name=args.base_name,
        )
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print("Saved files:")
    for k, path in result["saved_paths"].items():
        print(f"  {k}: {path}")
    s = result["summary"]
    print(
        f"Summary — text_len: {s.text_length}, tokens: {s.token_count}, "
        f"vocab: {s.vocab_size}, duration: {s.duration_seconds:.2f}s"
    )
    print("Difficulty counts:", s.counts_by_difficulty)
    print("POS counts:", s.counts_by_pos)


if __name__ == "__main__":
    main()
