const { guardMethods, parseJsonBody, sendError, sendJson } = require("../_lib/http");
const { requireOwnerSession } = require("../_lib/auth");
const { buildPerformanceDataset } = require("../_lib/performance");
const { buildSuggestions, createChangeRequest } = require("../_lib/owner-tools");
const { evaluateAlerts } = require("../_lib/alerts");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["POST"])) return;
  if (!requireOwnerSession(req, res)) return;

  try {
    const body = await parseJsonBody(req);
    const message = typeof body?.message === "string" ? body.message.trim() : "";

    if (!message) {
      sendError(res, 400, "message is required");
      return;
    }

    let summary = {
      impressions: 0,
      reach: 0,
      clicks: 0,
      engagements: 0,
      engagementRate: 0,
      platformBreakdown: [],
    };
    let rows = [];
    let dataWarning = null;

    try {
      const dataset = await buildPerformanceDataset({ includeStats: true, limit: 250 });
      summary = {
        impressions: dataset.kpis.totalImpressions,
        reach: dataset.kpis.totalReach,
        clicks: dataset.kpis.totalClicks,
        engagements: dataset.kpis.totalEngagement,
        engagementRate: dataset.kpis.averageEngagementRate,
        platformBreakdown: dataset.platformRollups,
      };
      rows = dataset.posts;
    } catch (error) {
      dataWarning = "Live GHL data unavailable; suggestions generated from owner request only";
    }

    const alertResult = evaluateAlerts(summary, rows);
    const suggestions = buildSuggestions(message, summary, rows, alertResult);
    const changeRequest = createChangeRequest({ message, summary, rows });

    sendJson(res, 200, {
      ok: true,
      reply:
        suggestions.length > 0
          ? `I reviewed current performance and prepared ${suggestions.length} recommended actions.`
          : "I reviewed the request and prepared a focused action plan.",
      suggestions,
      changeRequest,
      dataWarning,
    });
  } catch (error) {
    const statusCode = Number(error.statusCode || 500);
    sendError(res, statusCode, error.message || "Unable to process owner chat request");
  }
};
