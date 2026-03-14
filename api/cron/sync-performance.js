const { guardMethods, sendError, sendJson } = require("../_lib/http");
const { verifyCronRequest } = require("../_lib/auth");
const { buildPerformanceDataset } = require("../_lib/performance");
const { writePerformanceSnapshot } = require("../_lib/storage");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["GET"])) return;

  const cronAuth = verifyCronRequest(req);
  if (!cronAuth.ok) {
    sendError(res, 401, cronAuth.reason);
    return;
  }

  try {
    const dataset = await buildPerformanceDataset({ includeStats: true, limit: 250 });
    const persisted = await writePerformanceSnapshot({
      generatedAt: dataset.generatedAt,
      source: dataset.source,
      warnings: dataset.warnings,
      kpis: dataset.kpis,
      platformRollups: dataset.platformRollups,
      rankings: dataset.rankings,
      posts: dataset.posts,
    });

    sendJson(res, 200, {
      ok: true,
      cronAuth,
      sync: {
        syncedAt: dataset.generatedAt,
        totalPosts: dataset.posts.length,
        source: dataset.source,
        warnings: dataset.warnings,
        persisted,
      },
    });
  } catch (error) {
    const statusCode = Number(error.statusCode || 502);
    sendError(res, statusCode, "Performance sync failed", {
      details: error.details || error.message,
      cronAuth,
    });
  }
};
