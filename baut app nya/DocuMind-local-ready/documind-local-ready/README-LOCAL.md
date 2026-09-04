# DocuMind — Local Setup

DocuMind is an interactive document intelligence workspace UI. This package includes the polished web experience for exploring documents, asking questions, reviewing citations, summarizing, extracting fields, and exporting results.

## Requirements

- Node.js 20 or newer
- pnpm 9 or newer

## Run the web app

From the project root:

```bash
pnpm install
PORT=5173 BASE_PATH=/ pnpm --filter @workspace/documind-web run dev
```

Then open `http://localhost:5173`.

### Windows PowerShell

```powershell
pnpm install
$env:PORT=5173
$env:BASE_PATH="/"
pnpm --filter @workspace/documind-web run dev
```

## Validate the project

```bash
pnpm run typecheck
PORT=5173 BASE_PATH=/ pnpm --filter @workspace/documind-web run build
```

## What is included

- `artifacts/documind-web` — the interactive React + Vite web app
- `artifacts/api-server` — the shared API service scaffold
- `lib` — shared workspace packages and generated API libraries
- `pnpm-lock.yaml` — locked dependency versions for reproducible installs

The current web experience uses local demo state so the full interface can be explored immediately after install. Upload, chat, citations, summarization, extraction, filtering, settings, and export interactions are all available in the browser. The Python RAG backend from the original GitHub repository is not bundled into this Node workspace or connected to the demo UI yet.
