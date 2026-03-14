const { guardMethods, sendError, sendJson } = require("../_lib/http");
const { requireOwnerSession } = require("../_lib/auth");
const { buildPerformanceDataset } = require("../_lib/performance");
const { evaluateAlerts } = require("../_lib/alerts");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["GET"])) return;
  if (!requireOwnerSession(req, res)) return;

  try {
    const dataset = await buildPerformanceDataset({ includeStats: true, limit: 250 });
    const alertResult = evaluateAlerts(
      {
        reach: dataset.kpis.totalReach,
        clicks: dataset.kpis.totalClicks,
        engagementRate: dataset.kpis.averageEngagementRate,
      },
      dataset.posts
    );

    sendJson(res, 200, {
      ok: true,
      summary: {
        impressions: dataset.kpis.totalImpressions,
        reach: dataset.kpis.totalReach,
        clicks: dataset.kpis.totalClicks,
        engagements: dataset.kpis.totalEngagement,
        engagementRate: dataset.kpis.averageEngagementRate,
        platformBreakdown: dataset.platformRollups.map((item) => ({
          platform: item.platform,
          posts: item.posts,
          impressions: item.impressions,
          reach: item.reach,
          clicks: item.clicks,
          engagements: item.engagement,
          engagementRate: item.engagementRate,
        })),
      },
      topPosts: dataset.rankings.topPosts.map((post) => ({
        id: post.id,
        title: post.title || post.content?.slice(0, 90) || "Untitled post",
        platform: post.platform,
        clicks: post.metrics?.clicks || 0,
        engagementRate: post.metrics?.engagementRate || 0,
      })),
      bottomPosts: dataset.rankings.bottomPosts.map((post) => ({
        id: post.id,
        title: post.title || post.content?.slice(0, 90) || "Untitled post",
        platform: post.platform,
        clicks: post.metrics?.clicks || 0,
        engagementRate: post.metrics?.engagementRate || 0,
      })),
      alerts: alertResult.alerts,
      health: dataset.source === "ghl-live" ? "ok" : "degraded",
      lastSync: dataset.generatedAt,
      meta: {
        source: dataset.source,
        warnings: dataset.warnings,
        totalPosts: dataset.posts.length,
      },
    });
  } catch (error) {
    const statusCode = Number(error.statusCode || 502);
    sendError(res, statusCode, "Failed to fetch live performance summary", {
      details: error.details || error.message,
    });
  }
};
