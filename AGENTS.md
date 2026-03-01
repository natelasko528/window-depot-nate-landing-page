# AGENTS.md

## Cursor Cloud specific instructions

This is a zero-dependency static website (pure HTML/CSS/JS). There is no build step, no package manager, and no framework.

### Running the dev server

Serve the site with any HTTP server from the repo root:

```
python3 -m http.server 8080
```

Then open `http://localhost:8080/` in a browser. The main page is `index.html`; a light-mode variant lives at `index_lightmode.html`.

### Key files

- `index.html` — all-in-one landing page (HTML + inline CSS + inline JS, ~1900 lines)
- `kb.js` — AI chatbot knowledge base (exported JS const, reference only)
- `vercel.json` — Vercel static deployment config (no build command)

### External widgets

The page embeds two GoHighLevel (GHL) SaaS widgets (chat bubble + booking calendar). These load from external CDN URLs and require active GHL accounts. They work in the cloud VM when internet is available but are non-critical — the page renders fully without them.

### No lint/test/build tooling

There is no linter, test runner, or build system configured in this repo. Validation is visual — open `index.html` in a browser and verify rendering. If linting is needed, ad-hoc use of an HTML validator or `npx htmlhint index.html` can be run without installing project-level dependencies.
