const { getSession } = require('../_lib/auth');
const { isGHLConfigured } = require('../_lib/ghl');
const { isMetaConfigured, fetchAllMetaPosts } = require('../_lib/meta');
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

    const published = posts.filter(p => p.status === 'published');
    const totalReach = published.reduce((s, p) => s + p.metrics.reach, 0);
    const totalEngagement = published.reduce((s, p) => s + p.metrics.engagements, 0);
    const totalClicks = published.reduce((s, p) => s + p.metrics.clicks, 0);
    const totalImpressions = published.reduce((s, p) => s + p.metrics.impressions, 0);
    const avgCTR = totalImpressions > 0 ? (totalClicks / totalImpressions * 100) : 0;

    const platforms = [...new Set(published.map(p => p.platform))];
    const platformStats = {};
    for (const platform of platforms) {
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
        alerts.push({ type: 'winner', postId: p.id, platform: p.platform, theme: (p.caption || '').substring(0, 40), message: `Trending — ${(p.metrics.engagements / avgEng).toFixed(1)}× avg engagement` });
      }
      if (avgEng > 0 && p.metrics.engagements < avgEng * 0.3 && p.metrics.engagements > 0) {
        alerts.push({ type: 'underperformer', postId: p.id, platform: p.platform, theme: (p.caption || '').substring(0, 40), message: `Underperforming — ${Math.round(p.metrics.engagements / avgEng * 100)}% of avg` });
      }
    });

    const timeSeries = isDemo
      ? generateDemoTimeSeries(posts)
      : buildTimeSeries(published);

    res.status(200).json({
      isDemo,
      source,
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
      metaConnected: isMetaConfigured(),
    });
  } catch (err) {
    console.error('Summary error:', err);
    res.status(500).json({ error: 'Failed to load summary' });
  }
};

function buildTimeSeries(posts) {
  const dayMs = 86400000;
  const now = Date.now();
  const days = 30;
  const series = [];
  const platforms = [...new Set(posts.map(p => p.platform))];

  for (let d = days; d >= 0; d--) {
    const date = new Date(now - d * dayMs);
    const dateStr = date.toISOString().split('T')[0];
    const entry = { date: dateStr, total: 0 };
    for (const p of platforms) entry[p] = 0;

    posts.forEach(post => {
      if (!post.publishedAt) return;
      const pubDate = new Date(post.publishedAt);
      const daysSincePub = Math.floor((date.getTime() - pubDate.getTime()) / dayMs);
      if (daysSincePub >= 0 && daysSincePub < 7) {
        const dailyEng = Math.floor(post.metrics.engagements * (0.4 * Math.exp(-0.5 * daysSincePub)));
        entry[post.platform] = (entry[post.platform] || 0) + dailyEng;
        entry.total += dailyEng;
      }
    });

    series.push(entry);
  }

  return series;
}
