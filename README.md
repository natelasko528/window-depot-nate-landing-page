# Window Depot USA Milwaukee — Nate's Landing Page

## About
Official landing page for Nate at Window Depot USA of Milwaukee. Built with pure HTML/CSS/JS — no frameworks, no build step needed.

## File Structure
```
index.html                — Main landing page (all-in-one: HTML + CSS + JS)
kb.js                     — AI chatbot knowledge base (reference)
vercel.json               — Vercel deployment config (serves root as output)
SKILLBOSS_GUIDE.md        — SkillBoss setup, usage & marketing playbook
mcp.json.example          — MCP server config template for SkillBoss
package.json              — Node dependencies (includes skillboss-mcp-server)
```

## SkillBoss Integration

This project includes [SkillBoss](https://skillboss.co) — a unified AI platform (100+ models) for generating social media posts, ad copy, images, voiceovers, and more through Cursor's MCP protocol.

**Quick setup:**
1. Get your API key at [skillboss.co/console](https://skillboss.co/console)
2. Copy `mcp.json.example` to `.cursor/mcp.json` (create `.cursor/` dir if needed)
3. Replace `YOUR_KEY_HERE` with your key
4. Restart Cursor

See **[SKILLBOSS_GUIDE.md](SKILLBOSS_GUIDE.md)** for the full marketing playbook with prompt templates, batch workflows, and platform-specific guides.

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
