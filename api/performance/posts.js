const { guardMethods, parseQuery, sendError, sendJson } = require("../_lib/http");
const { requireOwnerSession } = require("../_lib/auth");
const { applyPostFilters, buildPerformanceDataset, sortPosts } = require("../_lib/performance");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["GET"])) return;
  if (!requireOwnerSession(req, res)) return;

  try {
    const query = parseQuery(req);
    const dataset = await buildPerformanceDataset({ includeStats: false, limit: 250 });
    const filtered = applyPostFilters(dataset.posts, query);
    const sorted = sortPosts(
      filtered,
      query.sortBy || "scheduledAt",
      query.sortDirection || "desc"
    );

    sendJson(res, 200, {
      ok: true,
      rows: sorted,
      meta: {
        source: dataset.source,
        warnings: dataset.warnings,
        totalRows: sorted.length,
        fetchedAt: dataset.generatedAt,
      },
    });
  } catch (error) {
    const statusCode = Number(error.statusCode || 502);
    sendError(res, statusCode, "Failed to fetch post performance rows", {
      details: error.details || error.message,
    });
  }
};
