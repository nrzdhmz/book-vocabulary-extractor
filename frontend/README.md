# Frontend (React + Sass)

Traditional, serif-led UI for uploading a book PDF and downloading leveled vocabulary CSVs.

## Quick start
```
cd frontend
npm install
npm run dev
```

## API expectation
- `POST /api/extract` returns JSON with `summary` and `csv_base64` map (`all`, `easy`, `intermediate`, `hard`) as base64-encoded CSV strings.  
- Set `VITE_API_BASE` in `.env` if your backend is not on the same origin.

## Build
```
npm run build
npm run preview
```

## Design notes
- Fonts: Playfair Display (headings) + Public Sans (body).
- Palette: warm, print-inspired neutral tones; no gradients on content areas; subtle shadow on panels.
- Sass at `src/styles.scss`.
