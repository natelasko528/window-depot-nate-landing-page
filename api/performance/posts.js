const { getSession } = require('../_lib/auth');
const { fetchGHLPosts, isGHLConfigured } = require('../_lib/ghl');
const { generateDemoData } = require('../_lib/demo-data');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!getSession(req)) {
    return res.status(401).json({ error: 'Not authenticated' });
  }

  try {
    let posts;
    let isDemo = false;

    if (isGHLConfigured()) {
      try {
        posts = await fetchGHLPosts(process.env.GHL_LOCATION_ID, process.env.GHL_API_KEY);
      } catch (err) {
        console.error('GHL fetch failed, falling back to demo:', err.message);
        posts = generateDemoData();
        isDemo = true;
      }
    } else {
      posts = generateDemoData();
      isDemo = true;
    }

    posts.sort((a, b) => b.metrics.engagements - a.metrics.engagements);

    posts.forEach(p => {
      p.metrics.engagementRate = p.metrics.reach > 0
        ? Math.round(p.metrics.engagements / p.metrics.reach * 10000) / 100
        : 0;
      p.metrics.ctr = p.metrics.impressions > 0
        ? Math.round(p.metrics.clicks / p.metrics.impressions * 10000) / 100
        : 0;
    });

    res.status(200).json({ isDemo, posts });
  } catch (err) {
    console.error('Posts error:', err);
    res.status(500).json({ error: 'Failed to load posts' });
  }
};
