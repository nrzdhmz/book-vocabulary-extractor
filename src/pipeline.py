import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Any

import pandas as pd

from src.pdf_reader import extract_text_from_pdf
from src.text_processor import process_text
from src.vocab_builder import build_vocabulary
from src.example_extractor import add_example_sentences
from src.vocab_ranker import rank_vocabulary
from src.definition_extractor import add_definitions
from src.vocab_saver import save_vocab_by_difficulty


@dataclass
class PipelineSummary:
    text_length: int
    token_count: int
    vocab_size: int
    duration_seconds: float
    counts_by_difficulty: Dict[str, int]
    counts_by_pos: Dict[str, int]


def run_pipeline(
    pdf_path: Path | str,
    min_frequency: int = 2,
    output_dir: Path | str = "outputs",
    base_name: str = "ranked_vocabulary",
) -> dict[str, Any]:
    start = time.perf_counter()
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    text = extract_text_from_pdf(str(pdf_path))
    tokens = process_text(text)
    vocab_df = build_vocabulary(tokens, min_frequency=min_frequency)
    vocab_examples = add_example_sentences(vocab_df, text)
    ranked = rank_vocabulary(vocab_examples)
    ranked = add_definitions(ranked)

    # CSVs
    saved_paths = save_vocab_by_difficulty(
        ranked, out_dir=output_dir, base_name=base_name
    )
    combined_path = Path(output_dir) / f"{base_name}.csv"
    ranked.to_csv(combined_path, index=False)
    saved_paths["combined"] = combined_path

    duration = time.perf_counter() - start
    summary = PipelineSummary(
        text_length=len(text),
        token_count=len(tokens),
        vocab_size=len(ranked),
        duration_seconds=duration,
        counts_by_difficulty=ranked["difficulty"].value_counts().to_dict(),
        counts_by_pos=ranked["pos"].value_counts().to_dict(),
    )

    metadata = {
        "pdf_path": str(pdf_path),
        "min_frequency": min_frequency,
        "output_dir": str(Path(output_dir).resolve()),
        "base_name": base_name,
        "summary": asdict(summary),
    }

    metadata_path = Path(output_dir) / f"{base_name}_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    saved_paths["metadata"] = metadata_path

    return {
        "ranked": ranked,
        "saved_paths": saved_paths,
        "summary": summary,
    }
