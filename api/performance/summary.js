const { getSession } = require('../_lib/auth');
const { fetchGHLPosts, isGHLConfigured } = require('../_lib/ghl');
const { generateDemoData, generateDemoTimeSeries } = require('../_lib/demo-data');

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

    const published = posts.filter(p => p.status === 'published');
    const totalReach = published.reduce((s, p) => s + p.metrics.reach, 0);
    const totalEngagement = published.reduce((s, p) => s + p.metrics.engagements, 0);
    const totalClicks = published.reduce((s, p) => s + p.metrics.clicks, 0);
    const totalImpressions = published.reduce((s, p) => s + p.metrics.impressions, 0);
    const avgCTR = totalImpressions > 0 ? (totalClicks / totalImpressions * 100) : 0;

    const platformStats = {};
    for (const platform of ['facebook', 'instagram', 'linkedin']) {
      const pPosts = published.filter(p => p.platform === platform);
      const pReach = pPosts.reduce((s, p) => s + p.metrics.reach, 0);
      const pEng = pPosts.reduce((s, p) => s + p.metrics.engagements, 0);
      const pClicks = pPosts.reduce((s, p) => s + p.metrics.clicks, 0);
      const pImpressions = pPosts.reduce((s, p) => s + p.metrics.impressions, 0);
      platformStats[platform] = {
        postCount: pPosts.length,
        totalPosts: posts.filter(p => p.platform === platform).length,
        reach: pReach,
        engagements: pEng,
        clicks: pClicks,
        ctr: pImpressions > 0 ? (pClicks / pImpressions * 100) : 0,
      };
    }

    const avgEng = published.length > 0 ? totalEngagement / published.length : 0;
    const alerts = [];
    published.forEach(p => {
      if (p.metrics.engagements > avgEng * 2.5) {
        alerts.push({ type: 'winner', postId: p.id, platform: p.platform, theme: p.theme, message: `Trending — ${(p.metrics.engagements / avgEng).toFixed(1)}× avg engagement` });
      }
      if (p.metrics.engagements < avgEng * 0.3 && p.metrics.engagements > 0) {
        alerts.push({ type: 'underperformer', postId: p.id, platform: p.platform, theme: p.theme, message: `Underperforming — ${Math.round(p.metrics.engagements / avgEng * 100)}% of avg` });
      }
    });
    for (const platform of ['facebook', 'instagram', 'linkedin']) {
      const scheduled = posts.filter(p => p.platform === platform && p.status === 'published').length;
      const total = posts.filter(p => p.platform === platform).length;
      if (scheduled === total && total > 0) {
        alerts.push({ type: 'status', platform, message: `All ${total} ${platform} posts published on schedule` });
      }
    }

    const timeSeries = generateDemoTimeSeries(posts);

    res.status(200).json({
      isDemo,
      lastSync: new Date().toISOString(),
      kpi: {
        totalReach,
        totalEngagement,
        avgCTR: Math.round(avgCTR * 100) / 100,
        activePosts: published.length,
        totalPosts: posts.length,
      },
      platformStats,
      timeSeries,
      alerts: alerts.slice(0, 10),
    });
  } catch (err) {
    console.error('Summary error:', err);
    res.status(500).json({ error: 'Failed to load summary' });
  }
};
