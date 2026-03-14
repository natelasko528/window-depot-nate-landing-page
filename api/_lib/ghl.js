const GHL_BASE = 'https://services.leadconnectorhq.com';
const GHL_VERSION = '2021-07-28';

async function ghlFetch(path, locationId, apiKey) {
  const url = `${GHL_BASE}${path}`;
  const resp = await fetch(url, {
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Version': GHL_VERSION,
      'Content-Type': 'application/json',
    },
  });
  if (!resp.ok) {
    const text = await resp.text();
    throw new Error(`GHL API ${resp.status}: ${text}`);
  }
  return resp.json();
}

async function fetchGHLPosts(locationId, apiKey) {
  const data = await ghlFetch(
    `/social-media-posting/${locationId}/posts?limit=100&sortOrder=DESC`,
    locationId,
    apiKey
  );
  return (data.posts || data.data || []).map(normalizePost);
}

function normalizePost(raw) {
  const metrics = raw.metrics || raw.insights || {};
  return {
    id: raw.id || raw._id,
    platform: detectPlatform(raw),
    theme: raw.tags?.[0] || raw.summary?.substring(0, 40) || 'Post',
    status: raw.status || 'published',
    caption: raw.summary || raw.text || '',
    scheduledAt: raw.scheduledAt || raw.scheduled_at || null,
    publishedAt: raw.publishedAt || raw.published_at || null,
    imageUrl: raw.media?.[0]?.url || raw.mediaUrls?.[0] || null,
    metrics: {
      impressions: metrics.impressions || metrics.views || 0,
      reach: metrics.reach || metrics.impressions || 0,
      engagements: (metrics.likes || 0) + (metrics.comments || 0) + (metrics.shares || 0) + (metrics.saves || 0),
      likes: metrics.likes || metrics.reactions || 0,
      comments: metrics.comments || metrics.replies || 0,
      shares: metrics.shares || metrics.reposts || 0,
      saves: metrics.saves || metrics.bookmarks || 0,
      clicks: metrics.clicks || metrics.link_clicks || 0,
    },
  };
}

function detectPlatform(raw) {
  const type = (raw.type || raw.platform || raw.accountType || '').toLowerCase();
  if (type.includes('facebook') || type.includes('fb')) return 'facebook';
  if (type.includes('instagram') || type.includes('ig')) return 'instagram';
  if (type.includes('linkedin') || type.includes('li')) return 'linkedin';
  if (raw.account?.platform) return raw.account.platform.toLowerCase();
  return 'facebook';
}

function isGHLConfigured() {
  return !!(process.env.GHL_API_KEY && process.env.GHL_LOCATION_ID);
}

module.exports = { fetchGHLPosts, isGHLConfigured };
