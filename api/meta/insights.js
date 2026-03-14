const { getSession } = require('../_lib/auth');
const { isMetaConfigured, fetchAllMetaPosts } = require('../_lib/meta');

module.exports = async (req, res) => {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }
  if (!getSession(req)) {
    return res.status(401).json({ error: 'Not authenticated' });
  }
  if (!isMetaConfigured()) {
    return res.status(200).json({
      configured: false,
      message: 'Meta API not configured. Visit /owner/meta-setup to connect.',
      posts: [],
    });
  }

  try {
    const posts = await fetchAllMetaPosts();

    posts.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));

    posts.forEach(p => {
      p.metrics.engagementRate = p.metrics.reach > 0
        ? Math.round(p.metrics.engagements / p.metrics.reach * 10000) / 100
        : 0;
      p.metrics.ctr = p.metrics.impressions > 0
        ? Math.round(p.metrics.clicks / p.metrics.impressions * 10000) / 100
        : 0;
    });

    const fbPosts = posts.filter(p => p.platform === 'facebook');
    const igPosts = posts.filter(p => p.platform === 'instagram');

    const summarize = (arr) => ({
      count: arr.length,
      totalReach: arr.reduce((s, p) => s + p.metrics.reach, 0),
      totalEngagements: arr.reduce((s, p) => s + p.metrics.engagements, 0),
      totalImpressions: arr.reduce((s, p) => s + p.metrics.impressions, 0),
      totalLikes: arr.reduce((s, p) => s + p.metrics.likes, 0),
      totalComments: arr.reduce((s, p) => s + p.metrics.comments, 0),
      totalShares: arr.reduce((s, p) => s + p.metrics.shares, 0),
    });

    res.status(200).json({
      configured: true,
      source: 'meta_graph_api',
      fetchedAt: new Date().toISOString(),
      summary: {
        total: summarize(posts),
        facebook: summarize(fbPosts),
        instagram: summarize(igPosts),
      },
      posts,
    });
  } catch (err) {
    console.error('Meta insights error:', err);
    res.status(500).json({ error: 'Failed to fetch Meta insights', message: err.message });
  }
};
