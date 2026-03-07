from pathlib import Path
import pandas as pd


def default_output_dir() -> Path:
    """Project-rooted outputs/ directory (avoids writing under notebooks/)."""
    project_root = Path(__file__).resolve().parents[1]
    return project_root / "outputs"


def save_vocab_by_difficulty(
    vocab_df: pd.DataFrame,
    out_dir: Path | str | None = None,
    base_name: str = "vocabulary"
) -> dict[str, Path]:
    """
    Save the full vocabulary and per-difficulty slices to CSV files.

    Expects `vocab_df` to already include a `difficulty` column
    (e.g., produced by rank_vocabulary).

    By default it writes to <project_root>/outputs to avoid creating
    notebooks/outputs when run from inside the notebooks folder.

    Returns a dict of difficulty -> saved Path.
    """
    out_dir = Path(out_dir) if out_dir else default_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = {}

    def _save(df: pd.DataFrame, suffix: str):
        path = out_dir / f"{base_name}_{suffix}.csv"
        df.to_csv(path, index=False)
        saved[suffix] = path

    # full
    _save(vocab_df, "all")

    for level in ("easy", "intermediate", "hard"):
        subset = vocab_df[vocab_df["difficulty"] == level]
        _save(subset, level)

    return saved
