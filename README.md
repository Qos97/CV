# fgfernandes.pt

Personal CV / portfolio site for Filipe Fernandes — a React + Vite single-page app, bilingual (EN/PT), served via nginx in Docker.

## Stack

- **React 18 + Vite** — SPA with route-based code splitting (`react-router-dom`)
- **lucide-react** — icon set
- **content.json** — single source of truth for all site text (EN + PT); also drives the generated CV PDFs
- **nginx** — multi-stage Docker build, CSP headers, gzip, immutable asset caching, `/healthz` healthcheck

## Running locally

```bash
cd website
npm install
npm run dev       # → http://localhost:5173
```

Other useful commands (from `website/`):

```bash
npm run build      # production build → website/dist/
npm run preview    # preview the production build → http://localhost:4173
```

## Editing content

All visible text lives in `content.json` at the repo root (`{ en: {...}, pt: {...} }`). After editing it, run from the repo root:

```bash
python3 generate.py
```

This validates `content.json`, copies it to `website/src/content.json`, and regenerates the downloadable CV PDFs (`cv-documents/`).

## Deploying

```bash
python3 deploy.py
```

Full pipeline: converts CV `.docx` sources to PDF, validates `content.json`, rsyncs to the target VM, and rebuilds the Docker container.
