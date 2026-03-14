const { getSession } = require('../_lib/auth');

const GRAPH_BASE = 'https://graph.facebook.com/v21.0';

module.exports = async (req, res) => {
  if (!getSession(req)) {
    res.writeHead(302, { Location: '/owner' });
    return res.end();
  }

  const url = new URL(req.url, `https://${req.headers.host}`);
  const code = url.searchParams.get('code');
  const error = url.searchParams.get('error');

  if (error || !code) {
    return sendHTML(res, 'Authorization Failed', `
      <p class="error">Facebook returned an error: ${error || 'no authorization code received'}.</p>
      <p>${url.searchParams.get('error_description') || ''}</p>
      <a href="/owner/meta-setup" class="btn">Try Again</a>
    `);
  }

  const appId = process.env.META_APP_ID;
  const appSecret = process.env.META_APP_SECRET;
  const baseUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : process.env.BASE_URL || 'https://wdusa-nate-landing.vercel.app';
  const redirectUri = `${baseUrl}/api/meta/callback`;

  if (!appId || !appSecret) {
    return sendHTML(res, 'Configuration Error', `
      <p class="error">META_APP_ID or META_APP_SECRET not set in Vercel environment variables.</p>
      <a href="/owner/meta-setup" class="btn">Setup Guide</a>
    `);
  }

  try {
    const tokenResp = await fetch(
      `${GRAPH_BASE}/oauth/access_token?client_id=${appId}&redirect_uri=${encodeURIComponent(redirectUri)}&client_secret=${appSecret}&code=${code}`
    );
    const tokenData = await tokenResp.json();
    if (tokenData.error) throw new Error(tokenData.error.message);

    const shortToken = tokenData.access_token;

    const longResp = await fetch(
      `${GRAPH_BASE}/oauth/access_token?grant_type=fb_exchange_token&client_id=${appId}&client_secret=${appSecret}&fb_exchange_token=${shortToken}`
    );
    const longData = await longResp.json();
    if (longData.error) throw new Error(longData.error.message);

    const longToken = longData.access_token;
    const expiresIn = longData.expires_in;
    const expiresDate = new Date(Date.now() + (expiresIn || 5184000) * 1000).toLocaleDateString();

    const pagesResp = await fetch(`${GRAPH_BASE}/me/accounts?fields=id,name,access_token,instagram_business_account&access_token=${longToken}`);
    const pagesData = await pagesResp.json();
    if (pagesData.error) throw new Error(pagesData.error.message);

    const pages = (pagesData.data || []).map(p => ({
      id: p.id,
      name: p.name,
      token: p.access_token,
      igId: p.instagram_business_account?.id || null,
    }));

    let html = `
      <div class="success-banner">Authorization successful.</div>
      <p>Long-lived user token expires: <strong>${expiresDate}</strong></p>

      <h2>Connected Pages</h2>
      <div class="pages">
    `;

    for (const page of pages) {
      html += `
        <div class="page-card">
          <div class="page-name">${page.name}</div>
          <div class="page-id">Page ID: ${page.id}${page.igId ? ` · IG ID: ${page.igId}` : ''}</div>
          <label>Page Access Token (never expires):</label>
          <div class="token-box">
            <code id="token_${page.id}">${page.token}</code>
            <button class="copy-btn" onclick="copyToken('token_${page.id}')">Copy</button>
          </div>
        </div>
      `;
    }

    html += `
      </div>

      <h2>What To Do Next</h2>
      <ol>
        <li>Copy the <strong>Page Access Token</strong> for the Facebook page you want to track.</li>
        <li>Go to <a href="https://vercel.com" target="_blank">Vercel Dashboard</a> → your project → Settings → Environment Variables.</li>
        <li>Add <code>META_PAGE_TOKEN</code> with the copied token.</li>
        <li>Add <code>META_PAGE_ID</code> with the Page ID above.</li>
        ${pages.some(p => p.igId) ? '<li>Add <code>META_IG_USER_ID</code> with the IG ID above (for Instagram insights).</li>' : ''}
        <li>Redeploy the project (or wait for the next push).</li>
        <li>Your dashboard will now show <strong>real per-post engagement data</strong> from Meta.</li>
      </ol>

      <div class="note">
        Page tokens obtained this way <strong>do not expire</strong> as long as the app and page remain connected.
        Your user token expires on ${expiresDate} — but the page tokens persist independently.
      </div>

      <a href="/owner/dashboard" class="btn">Back to Dashboard</a>

      <script>
      function copyToken(id) {
        const el = document.getElementById(id);
        navigator.clipboard.writeText(el.textContent).then(() => {
          const btn = el.parentElement.querySelector('.copy-btn');
          btn.textContent = 'Copied!';
          setTimeout(() => btn.textContent = 'Copy', 2000);
        });
      }
      </script>
    `;

    sendHTML(res, 'Meta Authorization Complete', html);
  } catch (err) {
    sendHTML(res, 'Authorization Error', `
      <p class="error">${err.message}</p>
      <a href="/owner/meta-setup" class="btn">Try Again</a>
    `);
  }
};

function sendHTML(res, title, body) {
  res.writeHead(200, { 'Content-Type': 'text/html' });
  res.end(`<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>${title} — Window Depot USA</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'DM Sans',sans-serif;background:#0A1628;color:#fff;padding:40px 20px;min-height:100vh;
background-image:radial-gradient(ellipse at 20% 80%,rgba(21,101,192,0.06) 0%,transparent 50%)}
.container{max-width:720px;margin:0 auto}
h1{font-size:22px;margin-bottom:24px;color:#D4AF37}
h2{font-size:16px;margin:28px 0 12px;color:#fff}
p{color:rgba(255,255,255,0.7);margin-bottom:12px;line-height:1.6;font-size:14px}
.success-banner{background:rgba(34,197,94,0.12);border:1px solid rgba(34,197,94,0.3);border-radius:10px;padding:14px 20px;color:#22C55E;font-weight:600;margin-bottom:20px;font-size:14px}
.error{color:#EF4444;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.2);border-radius:10px;padding:14px 20px;font-size:14px}
.page-card{background:#1A2F50;border-radius:12px;padding:20px;margin-bottom:12px;border:1px solid rgba(255,255,255,0.06)}
.page-name{font-weight:600;font-size:15px;margin-bottom:4px}
.page-id{font-size:12px;color:rgba(255,255,255,0.4);margin-bottom:12px;font-family:'JetBrains Mono',monospace}
label{display:block;font-size:11px;text-transform:uppercase;letter-spacing:0.5px;color:rgba(255,255,255,0.5);margin-bottom:6px}
.token-box{display:flex;gap:8px;align-items:flex-start}
.token-box code{flex:1;background:rgba(0,0,0,0.3);border-radius:8px;padding:10px 12px;font-size:11px;font-family:'JetBrains Mono',monospace;word-break:break-all;color:rgba(255,255,255,0.7);line-height:1.5;border:1px solid rgba(255,255,255,0.06)}
.copy-btn{padding:10px 16px;border-radius:8px;border:none;background:#D4AF37;color:#0A1628;font-weight:600;font-size:12px;cursor:pointer;white-space:nowrap;font-family:'DM Sans',sans-serif}
.copy-btn:hover{opacity:0.9}
ol{color:rgba(255,255,255,0.7);margin-left:20px;font-size:14px;line-height:2}
ol code{background:rgba(212,175,55,0.15);padding:2px 6px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#D4AF37}
.note{background:rgba(21,101,192,0.08);border:1px solid rgba(21,101,192,0.15);border-radius:10px;padding:14px 20px;color:rgba(255,255,255,0.6);font-size:13px;margin:20px 0}
a{color:#D4AF37}
.btn{display:inline-block;margin-top:20px;padding:12px 24px;background:#D4AF37;color:#0A1628;border-radius:10px;text-decoration:none;font-weight:600;font-size:14px}
.btn:hover{opacity:0.9}
</style>
</head><body><div class="container"><h1>${title}</h1>${body}</div></body></html>`);
}
