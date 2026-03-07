from pathlib import Path
import pandas as pd


def default_output_dir() -> Path:
    project_root = Path(__file__).resolve().parents[1]
    return project_root / "outputs"

def save_vocab_by_difficulty(
    vocab_df: pd.DataFrame,
    out_dir: Path | str | None = None,
    base_name: str = "vocabulary"
) -> dict[str, Path]:
    out_dir = Path(out_dir) if out_dir else default_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = {}

    def _save(df: pd.DataFrame, suffix: str):
        path = out_dir / f"{base_name}_{suffix}.csv"
        # Reorder columns: lemma, pos, definition, example_sentence, then the rest.
        priority = ["lemma", "pos", "definition", "example_sentence"]
        cols = priority + [c for c in df.columns if c not in priority]
        df[cols].to_csv(path, index=False)
        saved[suffix] = path

    # Save the full vocabulary
    _save(vocab_df, "all")
    # Save based on difficulty levels
    for level in ("easy", "intermediate", "hard"):
        subset = vocab_df[vocab_df["difficulty"] == level]
        _save(subset, level)

    return saved
