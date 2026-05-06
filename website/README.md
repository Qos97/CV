# Filipe Fernandes – CV Website

React + Vite single-page application with client-side routing.

## Requirements
- Node.js 18+
- npm 9+

## Setup

```bash
npm install
```

## Development server

```bash
npm run dev
# → http://localhost:5173
```

## Production build

```bash
npm run build
# Output in /dist
```

## Preview production build locally

```bash
npm run preview
# → http://localhost:4173
```

## Deploy

Static hosting — just upload the `/dist` folder to:
- **GitHub Pages**: use `gh-pages` branch or GitHub Actions
- **Netlify**: drag and drop `/dist` or connect repo
- **Vercel**: connect repo, set framework to Vite

For GitHub Pages with a custom base path, update `vite.config.js`:
```js
base: '/your-repo-name/'
```

## Update CV PDFs

Replace the files in `/public/`:
- `CV_Filipe_Fernandes_EN.pdf`
- `CV_Filipe_Fernandes_PT.pdf`

## Structure

```
src/
  pages/
    Home.jsx          # Hero + highlights + tech stack
    About.jsx         # Summary + stats + contact card
    Experience.jsx    # Timeline of work history
    Skills.jsx        # Tech skills by category
    Projects.jsx      # Homelab / personal projects
    Certifications.jsx # Target certifications
    Contact.jsx       # Email + LinkedIn
  App.jsx             # Router + Navbar + Footer
  index.css           # Global styles + design tokens
```
