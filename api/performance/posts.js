const { getSession } = require('../_lib/auth');
const { isMetaConfigured, fetchAllMetaPosts } = require('../_lib/meta');
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
    let source = 'demo';

    if (isMetaConfigured()) {
      try {
        posts = await fetchAllMetaPosts();
        source = 'meta';
      } catch (err) {
        console.error('Meta fetch failed, falling back to demo:', err.message);
        posts = generateDemoData();
        isDemo = true;
      }
    } else {
      posts = generateDemoData();
      isDemo = true;
    }

    posts.sort((a, b) => (b.metrics.engagements || 0) - (a.metrics.engagements || 0));

    posts.forEach(p => {
      p.metrics.engagementRate = p.metrics.reach > 0
        ? Math.round(p.metrics.engagements / p.metrics.reach * 10000) / 100
        : 0;
      p.metrics.ctr = p.metrics.impressions > 0
        ? Math.round(p.metrics.clicks / p.metrics.impressions * 10000) / 100
        : 0;
    });

    res.status(200).json({ isDemo, source, posts });
  } catch (err) {
    console.error('Posts error:', err);
    res.status(500).json({ error: 'Failed to load posts' });
  }
};
