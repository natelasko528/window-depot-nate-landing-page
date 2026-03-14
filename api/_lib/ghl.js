const fs = require("fs/promises");
const path = require("path");

const GHL_BASE_URL = process.env.GHL_BASE_URL || "https://services.leadconnectorhq.com";
const GHL_API_VERSION = "2021-07-28";
const REQUEST_TIMEOUT_MS = Number(process.env.GHL_REQUEST_TIMEOUT_MS || 15000);

const FALLBACK_POSTS_FILE = path.join(
  process.cwd(),
  "ad-drafts",
  "30-posts",
  "v3_ghl_schedule_results.json"
);

function safeString(value) {
  if (typeof value === "string") return value;
  if (value == null) return "";
  return String(value);
}

function safeNumber(value) {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  if (typeof value === "string" && value.trim()) {
    const parsed = Number(value.replace(/,/g, ""));
    if (Number.isFinite(parsed)) return parsed;
  }
  return 0;
}

function getGhlConfig() {
  const token = safeString(process.env.GHL_API_TOKEN);
  const locationId = safeString(process.env.GHL_LOCATION_ID);
  return { token, locationId, configured: Boolean(token && locationId) };
}

function normalizePlatform(input) {
  const value = safeString(input).toLowerCase();
  if (!value) return "unknown";
  if (value.includes("facebook") || value === "fb") return "facebook";
  if (value.includes("instagram") || value === "ig") return "instagram";
  if (value.includes("linkedin") || value === "li") return "linkedin";
  if (value.includes("google")) return "google";
  if (value.includes("youtube")) return "youtube";
  return value;
}

function parseResponseBody(raw) {
  if (!raw) return {};
  try {
    return JSON.parse(raw);
  } catch (_error) {
    return { rawText: raw };
  }
}

async function ghlRequest(pathname, options = {}) {
  const { token, configured } = getGhlConfig();
  if (!configured) {
    const error = new Error("Missing GHL_API_TOKEN or GHL_LOCATION_ID");
    error.statusCode = 500;
    throw error;
  }

  const url = new URL(pathname, GHL_BASE_URL);
  if (options.query && typeof options.query === "object") {
    Object.entries(options.query).forEach(([key, value]) => {
      if (value !== undefined && value !== null && safeString(value) !== "") {
        url.searchParams.set(key, safeString(value));
      }
    });
  }

  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(url.toString(), {
      method: safeString(options.method || "GET").toUpperCase(),
      headers: {
        Authorization: `Bearer ${token}`,
        Version: GHL_API_VERSION,
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: options.body ? JSON.stringify(options.body) : undefined,
      signal: abortController.signal,
    });
    const payload = parseResponseBody(await response.text());
    if (!response.ok) {
      const error = new Error(
        payload?.message || payload?.error || `GHL request failed with ${response.status}`
      );
      error.statusCode = response.status;
      error.payload = payload;
      throw error;
    }
    return payload;
  } finally {
    clearTimeout(timeout);
  }
}

function extractArrayPayload(payload) {
  if (Array.isArray(payload)) return payload;
  if (!payload || typeof payload !== "object") return [];
  const list = [
    payload.data,
    payload.items,
    payload.posts,
    payload.accounts,
    payload.results,
    payload.results && payload.results.posts,
    payload.results && payload.results.items,
    payload.results && payload.results.accounts,
  ];
  for (const candidate of list) {
    if (Array.isArray(candidate)) return candidate;
  }
  return [];
}

function collectNumericValues(value, bag = {}) {
  if (!value || typeof value !== "object") return bag;
  if (Array.isArray(value)) {
    value.forEach((item) => collectNumericValues(item, bag));
    return bag;
  }
  Object.entries(value).forEach(([key, child]) => {
    if (typeof child === "number" || typeof child === "string") {
      bag[key.toLowerCase()] = safeNumber(child);
    } else if (child && typeof child === "object") {
      collectNumericValues(child, bag);
    }
  });
  return bag;
}

function pickMetric(bag, aliases) {
  for (const alias of aliases) {
    if (Object.prototype.hasOwnProperty.call(bag, alias)) return bag[alias];
  }
  for (const [key, value] of Object.entries(bag)) {
    if (aliases.some((alias) => key.includes(alias))) return value;
  }
  return 0;
}

function normalizeMetrics(rawMetrics = {}) {
  const bag = collectNumericValues(rawMetrics, {});
  const impressions = pickMetric(bag, ["impressions", "views", "viewcount"]);
  const reach = pickMetric(bag, ["reach", "uniqueviews", "uniquereach"]);
  const clicks = pickMetric(bag, ["clicks", "linkclicks", "clickcount"]);
  const likes = pickMetric(bag, ["likes", "reactions"]);
  const comments = pickMetric(bag, ["comments", "commentcount"]);
  const shares = pickMetric(bag, ["shares", "sharecount"]);
  const saves = pickMetric(bag, ["saves", "savecount"]);
  const engagement = likes + comments + shares + saves + clicks;
  const engagementRate = impressions > 0 ? (engagement / impressions) * 100 : 0;
  return {
    impressions,
    reach,
    clicks,
    likes,
    comments,
    shares,
    saves,
    engagement,
    engagementRate: Number(engagementRate.toFixed(2)),
  };
}

function normalizeAccount(raw) {
  return {
    id: safeString(raw.id || raw.accountId || raw._id),
    name: safeString(raw.name || raw.accountName || "Untitled account"),
    platform: normalizePlatform(raw.platform || raw.type || raw.channel),
    connected: true,
    raw,
  };
}

function normalizePost(raw) {
  const metrics = normalizeMetrics({
    ...(raw.metrics || {}),
    ...(raw.stats || {}),
    ...(raw.analytics || {}),
    ...(raw.insights || {}),
  });
  const mediaUrl = Array.isArray(raw.media) && raw.media.length
    ? safeString(raw.media[0]?.url || raw.media[0]?.imageUrl)
    : safeString(raw.mediaUrl || raw.imageUrl || raw.image);

  return {
    id: safeString(raw.id || raw._id || raw.postId || raw.socialPostId),
    platform: normalizePlatform(raw.platform || raw.channel || raw.network),
    status: safeString(raw.status || raw.state || "unknown"),
    title: safeString(raw.title || raw.headline || raw.name || raw.summary).slice(0, 140),
    content: safeString(raw.summary || raw.message || raw.caption || raw.content),
    accountId: safeString(raw.accountId || (Array.isArray(raw.accountIds) ? raw.accountIds[0] : "")),
    scheduledAt: safeString(raw.scheduleDate || raw.scheduledAt || raw.displayDate),
    publishedAt: safeString(raw.publishedAt || raw.postedAt || raw.createdAt),
    mediaUrl,
    metrics,
    raw,
  };
}

async function fetchConnectedAccounts() {
  const { locationId } = getGhlConfig();
  const payload = await ghlRequest(`/social-media-posting/${locationId}/accounts`);
  const accounts = extractArrayPayload(payload);
  return accounts.map(normalizeAccount);
}

async function fetchPostsList(options = {}) {
  const { locationId } = getGhlConfig();
  const payload = await ghlRequest(`/social-media-posting/${locationId}/posts/list`, {
    method: "POST",
    body: { skip: safeString(options.skip ?? "0"), limit: safeString(options.limit ?? "250") },
  });
  return extractArrayPayload(payload);
}

async function fetchStatistics(profileIds = []) {
  const { locationId } = getGhlConfig();
  if (!Array.isArray(profileIds) || profileIds.length === 0) {
    return null;
  }
  return ghlRequest("/social-media-posting/statistics", {
    method: "POST",
    query: { locationId },
    body: { profileIds },
  });
}

async function readFallbackPosts() {
  try {
    const raw = await fs.readFile(FALLBACK_POSTS_FILE, "utf8");
    const payload = JSON.parse(raw);
    const created = Array.isArray(payload?.created) ? payload.created : [];
    return created.map((post) =>
      normalizePost({
        ...post,
        id: post.post_id,
        status: "scheduled",
        media: [{ url: post.media_url }],
      })
    );
  } catch (_error) {
    return [];
  }
}

function summarizePosts(posts) {
  const totals = posts.reduce(
    (acc, post) => {
      acc.impressions += safeNumber(post.metrics?.impressions);
      acc.reach += safeNumber(post.metrics?.reach);
      acc.clicks += safeNumber(post.metrics?.clicks);
      acc.engagements += safeNumber(post.metrics?.engagement);
      return acc;
    },
    { impressions: 0, reach: 0, clicks: 0, engagements: 0 }
  );
  const platformMap = {};
  posts.forEach((post) => {
    const key = normalizePlatform(post.platform);
    if (!platformMap[key]) {
      platformMap[key] = {
        platform: key,
        posts: 0,
        impressions: 0,
        reach: 0,
        clicks: 0,
        engagements: 0,
      };
    }
    platformMap[key].posts += 1;
    platformMap[key].impressions += safeNumber(post.metrics?.impressions);
    platformMap[key].reach += safeNumber(post.metrics?.reach);
    platformMap[key].clicks += safeNumber(post.metrics?.clicks);
    platformMap[key].engagements += safeNumber(post.metrics?.engagement);
  });
  const platformBreakdown = Object.values(platformMap).map((entry) => ({
    ...entry,
    engagementRate:
      entry.impressions > 0 ? Number(((entry.engagements / entry.impressions) * 100).toFixed(2)) : 0,
  }));
  const engagementRate =
    totals.impressions > 0 ? Number(((totals.engagements / totals.impressions) * 100).toFixed(2)) : 0;
  return { ...totals, engagementRate, platformBreakdown };
}

async function getPerformanceSourceData(options = {}) {
  const warnings = [];
  const { configured } = getGhlConfig();
  if (!configured) {
    const fallbackPosts = await readFallbackPosts();
    return {
      source: "fallback-local",
      accounts: [],
      posts: fallbackPosts,
      summary: summarizePosts(fallbackPosts),
      warnings: ["Missing GHL credentials; using local scheduled fallback data."],
    };
  }

  try {
    const [accounts, postsRaw] = await Promise.all([
      fetchConnectedAccounts().catch((error) => {
        warnings.push(`Account fetch failed: ${error.message}`);
        return [];
      }),
      fetchPostsList({ limit: options.limit || 250 }),
    ]);
    const statsRaw = await fetchStatistics(accounts.map((item) => item.id).filter(Boolean)).catch(
      (error) => {
        warnings.push(`Statistics endpoint unavailable: ${error.message}`);
        return null;
      }
    );

    const posts = postsRaw.map(normalizePost);
    const derived = summarizePosts(posts);
    const statsMetrics = normalizeMetrics(statsRaw || {});
    const summary =
      statsMetrics.impressions || statsMetrics.reach || statsMetrics.clicks
        ? {
            ...derived,
            impressions: statsMetrics.impressions || derived.impressions,
            reach: statsMetrics.reach || derived.reach,
            clicks: statsMetrics.clicks || derived.clicks,
            engagements: statsMetrics.engagement || derived.engagements,
            engagementRate:
              (statsMetrics.impressions || derived.impressions) > 0
                ? Number(
                    (
                      ((statsMetrics.engagement || derived.engagements) /
                        (statsMetrics.impressions || derived.impressions)) *
                      100
                    ).toFixed(2)
                  )
                : derived.engagementRate,
          }
        : derived;

    return { source: "ghl-live", accounts, posts, summary, warnings };
  } catch (error) {
    const fallbackPosts = await readFallbackPosts();
    return {
      source: "fallback-local",
      accounts: [],
      posts: fallbackPosts,
      summary: summarizePosts(fallbackPosts),
      warnings: [...warnings, `GHL fetch failed: ${error.message}`],
    };
  }
}

async function fetchPostPerformanceRows() {
  const sourceData = await getPerformanceSourceData({ limit: 250 });
  return {
    rows: sourceData.posts,
    meta: {
      source: sourceData.source,
      rowCount: sourceData.posts.length,
      warnings: sourceData.warnings,
      fetchedAt: new Date().toISOString(),
    },
  };
}

async function fetchLivePerformanceSummary() {
  const sourceData = await getPerformanceSourceData({ limit: 250 });
  return {
    summary: sourceData.summary,
    meta: {
      source: sourceData.source,
      warnings: sourceData.warnings,
      fetchedAt: new Date().toISOString(),
    },
  };
}

module.exports = {
  getGhlConfig,
  normalizePlatform,
  normalizeMetrics,
  fetchConnectedAccounts,
  fetchPostsList,
  fetchPostPerformanceRows,
  fetchLivePerformanceSummary,
  getPerformanceSourceData,
};
