const crypto = require('crypto');
const { getSession } = require('../_lib/auth');

module.exports = (req, res) => {
  if (!getSession(req)) {
    return res.status(401).json({ error: 'Not authenticated. Log in at /owner first.' });
  }

  const appId = process.env.META_APP_ID;
  const baseUrl = process.env.VERCEL_URL
    ? `https://${process.env.VERCEL_URL}`
    : process.env.BASE_URL || 'https://wdusa-nate-landing.vercel.app';

  if (!appId) {
    return res.status(500).json({
      error: 'META_APP_ID not configured. Add it to Vercel environment variables.',
      setup: 'See /owner/meta-setup for instructions.',
    });
  }

  const redirectUri = `${baseUrl}/api/meta/callback`;
  const state = crypto.randomBytes(16).toString('hex');

  const scopes = [
    'pages_read_engagement',
    'pages_show_list',
    'read_insights',
    'instagram_basic',
    'instagram_manage_insights',
  ].join(',');

  const authUrl = new URL('https://www.facebook.com/v21.0/dialog/oauth');
  authUrl.searchParams.set('client_id', appId);
  authUrl.searchParams.set('redirect_uri', redirectUri);
  authUrl.searchParams.set('scope', scopes);
  authUrl.searchParams.set('response_type', 'code');
  authUrl.searchParams.set('state', state);

  res.writeHead(302, { Location: authUrl.toString() });
  res.end();
};
