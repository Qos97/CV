# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal CV website for Filipe Fernandes. React + Vite SPA served via nginx in Docker, deployed to a local VM. Supports EN/PT bilingual content driven entirely by `content.json`.

## Key Commands

All frontend commands run from `website/`:

```bash
cd website
npm install       # first-time setup
npm run dev       # dev server → http://localhost:5173
npm run build     # production build → website/dist/
npm run preview   # preview production build → http://localhost:4173
```

**Before deploying**, always run from the repo root:
```bash
python3 generate.py   # validates content.json and copies it to website/src/content.json
```

**Full deploy** (WSL → VM via rsync + Docker):
```bash
python3 deploy.py
# Converts .docx CVs to PDF via Word COM, validates content.json, rsyncs to VM, rebuilds container
```

## Architecture

```
content.json              ← single source of truth for all website text (EN + PT)
generate.py               ← validates content.json and copies it to website/src/content.json
deploy.py                 ← full pipeline: PDF conversion → generate → rsync → docker compose up
cv-documents/             ← CV source files (.docx) and generated PDFs
website/
  src/
    content.json          ← copy of root content.json (do not edit directly — use generate.py)
    LanguageContext.jsx   ← React context: { lang, setLang }, default 'en'
    App.jsx               ← Router, Navbar, Footer; wraps everything in <LanguageProvider>
    pages/                ← one component per route (Home, About, Experience, Skills, Projects, Certifications, Contact)
    index.css             ← global styles and CSS design tokens
  public/                 ← static assets; PDFs served from here at runtime
  Dockerfile              ← multi-stage: Node build → nginx static serve
  docker-compose.yml      ← exposes port 8080, healthcheck at /healthz
```

## Content Editing Workflow

All visible text lives in `content.json` (root), structured as `{ en: {...}, pt: {...} }` with sections: `nav`, `home`, `about`, `experience`, `skills`, `projects`, `certifications`, `contact`.

After editing `content.json`, run `python3 generate.py` to validate and sync it to `website/src/content.json`. The website reads from the copy in `src/`.

## Bilingual Pattern

Every page component calls `useLang()` to get `lang`, then reads `content[lang].<section>` for its data. No i18n library — all translations are in `content.json`.
