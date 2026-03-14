const { getPerformanceSourceData } = require("./ghl");

function normalizeStatus(status) {
  const value = String(status || "").toLowerCase();
  if (!value) return "unknown";
  if (value.includes("publish")) return "published";
  if (value.includes("schedule")) return "scheduled";
  if (value.includes("draft")) return "draft";
  return value;
}

function aggregateMetrics(posts) {
  const totals = posts.reduce(
    (acc, post) => {
      acc.impressions += Number(post.metrics?.impressions || 0);
      acc.reach += Number(post.metrics?.reach || 0);
      acc.clicks += Number(post.metrics?.clicks || 0);
      acc.engagement += Number(post.metrics?.engagement || 0);
      return acc;
    },
    { impressions: 0, reach: 0, clicks: 0, engagement: 0 }
  );

  const engagementRate =
    totals.impressions > 0 ? (totals.engagement / totals.impressions) * 100 : 0;

  return {
    totalPosts: posts.length,
    totalImpressions: totals.impressions,
    totalReach: totals.reach,
    totalClicks: totals.clicks,
    totalEngagement: totals.engagement,
    averageEngagementRate: Number(engagementRate.toFixed(2)),
  };
}

function buildPlatformRollups(posts) {
  const rollups = posts.reduce((acc, post) => {
    const key = post.platform || "unknown";
    if (!acc[key]) {
      acc[key] = {
        platform: key,
        posts: 0,
        impressions: 0,
        reach: 0,
        clicks: 0,
        engagement: 0,
      };
    }

    acc[key].posts += 1;
    acc[key].impressions += Number(post.metrics?.impressions || 0);
    acc[key].reach += Number(post.metrics?.reach || 0);
    acc[key].clicks += Number(post.metrics?.clicks || 0);
    acc[key].engagement += Number(post.metrics?.engagement || 0);
    return acc;
  }, {});

  return Object.values(rollups).map((platform) => ({
    ...platform,
    engagementRate:
      platform.impressions > 0
        ? Number(((platform.engagement / platform.impressions) * 100).toFixed(2))
        : 0,
  }));
}

function rankPosts(posts) {
  const scored = posts.map((post) => ({
    ...post,
    score:
      Number(post.metrics?.engagementRate || 0) * 0.6 +
      Number(post.metrics?.clicks || 0) * 0.25 +
      Number(post.metrics?.impressions || 0) * 0.15,
  }));

  const byScoreDesc = [...scored].sort((a, b) => b.score - a.score);
  const byScoreAsc = [...scored].sort((a, b) => a.score - b.score);
  return {
    topPosts: byScoreDesc.slice(0, 5),
    bottomPosts: byScoreAsc.slice(0, 5),
  };
}

function evaluateAlerts(posts) {
  const now = Date.now();
  const staleThresholdMs = 7 * 24 * 60 * 60 * 1000;

  const highPerformers = [];
  const lowPerformers = [];
  const stalePosts = [];

  posts.forEach((post) => {
    const impressions = Number(post.metrics?.impressions || 0);
    const clicks = Number(post.metrics?.clicks || 0);
    const engagementRate = Number(post.metrics?.engagementRate || 0);
    const publishedAt = post.publishedAt ? new Date(post.publishedAt).getTime() : null;

    if (engagementRate >= 5 || clicks >= 20) {
      highPerformers.push(post);
    }

    if (impressions >= 100 && engagementRate < 1) {
      lowPerformers.push(post);
    }

    if (
      publishedAt &&
      now - publishedAt > staleThresholdMs &&
      impressions === 0 &&
      clicks === 0
    ) {
      stalePosts.push(post);
    }
  });

  return {
    highPerformers,
    lowPerformers,
    stalePosts,
  };
}

function applyPostFilters(posts, query = {}) {
  const platformFilter = query.platform ? String(query.platform).toLowerCase() : null;
  const statusFilter = query.status ? normalizeStatus(query.status) : null;
  const searchFilter = query.search ? String(query.search).toLowerCase() : null;

  let filtered = [...posts];
  if (platformFilter) {
    filtered = filtered.filter((post) => String(post.platform).toLowerCase() === platformFilter);
  }
  if (statusFilter) {
    filtered = filtered.filter((post) => normalizeStatus(post.status) === statusFilter);
  }
  if (searchFilter) {
    filtered = filtered.filter((post) =>
      `${post.title || ""} ${post.content || ""}`.toLowerCase().includes(searchFilter)
    );
  }
  return filtered;
}

function sortPosts(posts, sortBy = "scheduledAt", sortDirection = "desc") {
  const direction = String(sortDirection).toLowerCase() === "asc" ? 1 : -1;
  const key = sortBy;
  return [...posts].sort((a, b) => {
    const aValue = a[key];
    const bValue = b[key];
    if (aValue === bValue) return 0;
    if (aValue === null || aValue === undefined) return 1;
    if (bValue === null || bValue === undefined) return -1;
    if (typeof aValue === "number" && typeof bValue === "number") {
      return (aValue - bValue) * direction;
    }
    return String(aValue).localeCompare(String(bValue)) * direction;
  });
}

async function buildPerformanceDataset(options = {}) {
  const sourceData = await getPerformanceSourceData({
    includeStats: options.includeStats ?? true,
    limit: options.limit || 200,
    status: options.status,
  });

  const posts = sourceData.posts.map((post) => ({
    ...post,
    status: normalizeStatus(post.status),
  }));
  const kpis = aggregateMetrics(posts);
  const platformRollups = buildPlatformRollups(posts);
  const rankings = rankPosts(posts);
  const alerts = evaluateAlerts(posts);

  return {
    generatedAt: new Date().toISOString(),
    source: sourceData.source,
    warnings: sourceData.warnings,
    accounts: sourceData.accounts,
    posts,
    kpis,
    platformRollups,
    rankings,
    alerts,
  };
}

module.exports = {
  aggregateMetrics,
  buildPlatformRollups,
  rankPosts,
  evaluateAlerts,
  applyPostFilters,
  sortPosts,
  buildPerformanceDataset,
};
