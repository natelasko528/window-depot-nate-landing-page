# Window Depot USA Milwaukee — Nate's Landing Page

## About
Official landing page for Nate at Window Depot USA of Milwaukee. Built with pure HTML/CSS/JS — no frameworks, no build step needed.

## File Structure
```
index.html      — Main landing page (all-in-one: HTML + CSS + JS)
kb.js           — AI chatbot knowledge base (reference)
vercel.json     — Vercel deployment config (serves root as output)
```

## Deploying to Vercel
1. Connect this GitHub repo to Vercel at vercel.com/new
2. Vercel auto-detects the config — zero setup needed
3. Every push to `main` auto-deploys

**Live URL**: https://wdusa-nate-landing.vercel.app

## Making Changes
- Edit `index.html` to change content, colors, copy, sections
- Update phone numbers by searching for `(414) 312-5213`
- Update the GHL booking calendar by changing the iframe `src` URL
- Update the GHL chat widget by changing the `data-widget-id` attribute

## Contact Info in the Page
- Phone: (414) 312-5213
- Email: nate@windowdepotmilwaukee.com
- Website: windowdepotmilwaukee.com

## Key CSS Variables (top of index.html)
```css
--navy: #0A1628      /* dark navy */
--gold: #B8900A      /* dark gold */
--gold2: #D4AF37     /* bright gold */
--ivory: #FAFAF6     /* page background */
```
