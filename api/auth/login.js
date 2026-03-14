const { signToken, setSessionCookie } = require('../_lib/auth');

module.exports = (req, res) => {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const ownerPassword = process.env.OWNER_PASSWORD;
  const sessionSecret = process.env.SESSION_SECRET;

  if (!ownerPassword || !sessionSecret) {
    return res.status(500).json({ error: 'Server not configured. Set OWNER_PASSWORD and SESSION_SECRET env vars.' });
  }

  let body = '';
  req.on('data', chunk => { body += chunk; });
  req.on('end', () => {
    try {
      const { password } = JSON.parse(body);
      if (!password || password !== ownerPassword) {
        return res.status(401).json({ error: 'Invalid password' });
      }

      const now = Math.floor(Date.now() / 1000);
      const token = signToken({ sub: 'owner', iat: now, exp: now + 86400 }, sessionSecret);
      setSessionCookie(res, token);
      res.status(200).json({ ok: true });
    } catch {
      res.status(400).json({ error: 'Invalid request body' });
    }
  });
};
