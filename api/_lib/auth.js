const crypto = require('crypto');

function signToken(payload, secret) {
  const header = Buffer.from(JSON.stringify({ alg: 'HS256', typ: 'JWT' })).toString('base64url');
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const sig = crypto.createHmac('sha256', secret).update(`${header}.${body}`).digest('base64url');
  return `${header}.${body}.${sig}`;
}

function verifyToken(token, secret) {
  if (!token || !secret) return null;
  const parts = token.split('.');
  if (parts.length !== 3) return null;
  const [header, body, sig] = parts;
  const expected = crypto.createHmac('sha256', secret).update(`${header}.${body}`).digest('base64url');
  if (sig !== expected) return null;
  try {
    const payload = JSON.parse(Buffer.from(body, 'base64url').toString());
    if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch {
    return null;
  }
}

function parseCookies(str) {
  const obj = {};
  if (!str) return obj;
  str.split(';').forEach(pair => {
    const [key, ...val] = pair.split('=');
    if (key) obj[key.trim()] = val.join('=').trim();
  });
  return obj;
}

function getSession(req) {
  const secret = process.env.SESSION_SECRET;
  if (!secret) return null;
  const cookies = parseCookies(req.headers.cookie);
  return verifyToken(cookies.wd_session, secret);
}

function setSessionCookie(res, token) {
  const maxAge = 86400;
  const secure = process.env.NODE_ENV === 'production' ? '; Secure' : '';
  res.setHeader('Set-Cookie', `wd_session=${token}; HttpOnly; SameSite=Strict; Path=/${secure}; Max-Age=${maxAge}`);
}

function clearSessionCookie(res) {
  res.setHeader('Set-Cookie', 'wd_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0');
}

module.exports = { signToken, verifyToken, parseCookies, getSession, setSessionCookie, clearSessionCookie };
