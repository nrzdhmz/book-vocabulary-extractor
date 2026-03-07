from __future__ import annotations

import base64
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from src.pipeline import run_pipeline

app = FastAPI(title="Book Vocabulary Extractor API")

# Allow local dev origins (Vite default) and same-origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def encode_csv(path: Path) -> str:
    data = path.read_bytes()
    return base64.b64encode(data).decode("ascii")


@app.post("/api/extract")
async def extract(
    file: UploadFile = File(...),
    min_frequency: int = Form(2),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Empty filename")

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Save upload to a temp path inside backend/tmp_uploads
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    temp_path = upload_dir / file.filename
    temp_path.write_bytes(await file.read())

    try:
        result = run_pipeline(
            pdf_path=temp_path,
            min_frequency=min_frequency,
            output_dir=Path("outputs"),
            base_name="ranked_vocabulary",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        temp_path.unlink(missing_ok=True)

    saved = result["saved_paths"]

    csv_map: Dict[str, str] = {}
    for key in ("all", "easy", "intermediate", "hard"):
        path = saved.get(key)
        if path:
            csv_map[key] = encode_csv(Path(path))

    summary = result["summary"].__dict__

    return {
        "summary": summary,
        "csv_base64": csv_map,
    }


@app.get("/healthz")
async def health():
    return {"status": "ok"}
