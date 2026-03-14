const { guardMethods, sendError, sendJson } = require("../_lib/http");
const { verifyCronRequest } = require("../_lib/auth");
const { buildPerformanceDataset } = require("../_lib/performance");
const { evaluateAlerts } = require("../_lib/alerts");
const { writeAlertsSnapshot } = require("../_lib/storage");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["GET"])) return;

  const cronAuth = verifyCronRequest(req);
  if (!cronAuth.ok) {
    sendError(res, 401, cronAuth.reason);
    return;
  }

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
    const persisted = await writeAlertsSnapshot({
      generatedAt: dataset.generatedAt,
      source: dataset.source,
      warnings: dataset.warnings,
      counts: alertResult.counts,
      alerts: alertResult.alerts,
    });

    sendJson(res, 200, {
      ok: true,
      cronAuth,
      evaluatedAt: dataset.generatedAt,
      counts: alertResult.counts,
      alerts: alertResult.alerts,
      persisted,
    });
  } catch (error) {
    const statusCode = Number(error.statusCode || 502);
    sendError(res, statusCode, "Alert evaluation failed", {
      details: error.details || error.message,
      cronAuth,
    });
  }
};
