import { useMemo, useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "";

const difficultyOrder = ["all", "easy", "intermediate", "hard"];

const pretty = (s) => s.charAt(0).toUpperCase() + s.slice(1);

export default function App() {
  const [file, setFile] = useState(null);
  const [minFreq, setMinFreq] = useState(2);
  const [status, setStatus] = useState("Idle");
  const [summary, setSummary] = useState(null);
  const [csvMap, setCsvMap] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  const hasCsv = useMemo(() => Object.keys(csvMap).length > 0, [csvMap]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setStatus("Please select a PDF first.");
      return;
    }
    setIsLoading(true);
    setStatus("Uploading and processing…");
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("min_frequency", String(minFreq || 2));
      const res = await fetch(`${API_BASE}/api/extract`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Request failed");
      setSummary(data.summary || null);
      setCsvMap(data.csv_base64 || {});
      setStatus("Ready — choose a CSV to download.");
    } catch (err) {
      setStatus(`Error: ${err.message}`);
      setCsvMap({});
    } finally {
      setIsLoading(false);
    }
  };

  const downloadCsv = (which) => {
    const b64 = csvMap[which];
    if (!b64) return;
    const text = atob(b64);
    const blob = new Blob([text], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `vocabulary_${which}.csv`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  };

  return (
    <div className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Book Vocabulary Extractor</p>
          <h1>Upload a book PDF. Get leveled vocabulary with examples & definitions.</h1>
          <p className="sub">Best with text-based PDFs (not scanned images).</p>
        </div>
        <div className="badge">{summary ? `${summary.vocab_size} words` : "0 words"}</div>
      </header>

      <section className="panel">
        <form className="form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="label">Book PDF</label>
            <div className="file-row">
              <label className="file-cta">
                <input
                  type="file"
                  accept="application/pdf"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  disabled={isLoading}
                />
                <span>{file ? "Replace PDF" : "Choose PDF"}</span>
              </label>
              <span className="file-name">
                {file ? file.name : "No file chosen"}
              </span>
            </div>
            <p className="hint">Choose a text-based (non-scanned) PDF.</p>
          </div>

          <div className="form-group inline">
            <div className="freq-wrap">
              <label className="label" htmlFor="minfreq">Min frequency</label>
              <input
                id="minfreq"
                type="number"
                min={1}
                value={minFreq}
                onChange={(e) => setMinFreq(Number(e.target.value) || 2)}
                disabled={isLoading}
              />
            </div>
            <button type="submit" className="btn" disabled={isLoading}>
              {isLoading ? "Processing…" : "Run extractor"}
            </button>
          </div>
        </form>

        <p className="status">{status}</p>

        {summary && (
          <div className="stats">
            <Stat label="Text length" value={summary.text_length?.toLocaleString()} />
            <Stat label="Tokens" value={summary.token_count?.toLocaleString()} />
            <Stat label="Vocabulary" value={summary.vocab_size?.toLocaleString()} />
          </div>
        )}
      </section>

      <section className="panel">
        <h3>Download CSVs</h3>
        <p className="hint">Each file contains lemma, POS, frequency, difficulty, definition, and example sentence.</p>
        <div className="download-grid">
          {difficultyOrder.map((d) => (
            <button
              key={d}
              className="btn ghost"
              disabled={!hasCsv}
              onClick={() => downloadCsv(d)}
            >
              {pretty(d)} CSV
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="stat">
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value ?? "—"}</div>
    </div>
  );
}
