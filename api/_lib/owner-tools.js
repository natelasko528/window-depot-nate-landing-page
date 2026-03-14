const { evaluateAlerts } = require("./alerts");

function safeString(value) {
  if (typeof value === "string") return value.trim();
  if (value == null) return "";
  return String(value).trim();
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function detectFocusAreas(message) {
  const text = safeString(message).toLowerCase();
  const tags = [];

  const dictionary = [
    ["windows", ["window", "windows", "triple pane", "provia"]],
    ["doors", ["door", "doors", "entry"]],
    ["siding", ["siding", "cladding", "craneboard", "ascend"]],
    ["roofing", ["roof", "roofing", "shingle", "metal roof"]],
    ["flooring", ["floor", "flooring", "lvp", "hardwood", "laminate", "carpet"]],
    ["bathrooms", ["bath", "bathroom", "shower", "tub"]],
    ["facebook", ["facebook", "fb"]],
    ["instagram", ["instagram", "ig"]],
    ["linkedin", ["linkedin"]],
    ["creative", ["creative", "image", "graphic", "visual"]],
    ["copy", ["copy", "headline", "caption", "text"]],
    ["offer", ["offer", "gift card", "estimate", "price lock"]],
  ];

  dictionary.forEach(([tag, keywords]) => {
    if (keywords.some((keyword) => text.includes(keyword))) {
      tags.push(tag);
    }
  });

  return unique(tags);
}

function rankPosts(rows) {
  const normalized = Array.isArray(rows) ? rows : [];
  const sorted = [...normalized].sort(
    (a, b) => (b?.metrics?.engagementRate || 0) - (a?.metrics?.engagementRate || 0)
  );
  return {
    topPosts: sorted.slice(0, 3),
    lowPosts: sorted.slice(-3).reverse(),
  };
}

function buildSuggestions(message, summary, rows, alertResult) {
  const suggestions = [];
  const focusAreas = detectFocusAreas(message);
  const { topPosts, lowPosts } = rankPosts(rows);

  if (topPosts.length > 0) {
    const top = topPosts[0];
    suggestions.push(
      `Replicate the strongest post style from ${top.platform} (engagement rate ${top.metrics.engagementRate}%).`
    );
  }

  if (lowPosts.length > 0) {
    const lowest = lowPosts[0];
    suggestions.push(
      `Refresh underperforming ${lowest.platform} copy with a tighter local CTA and clearer offer framing.`
    );
  }

  if ((summary?.engagementRate || 0) < 1) {
    suggestions.push(
      "Test shorter captions plus one direct homeowner benefit in the first sentence to improve overall engagement."
    );
  }

  if ((summary?.clicks || 0) > 0 && (summary?.reach || 0) > 0) {
    const ctr = Number((((summary?.clicks || 0) / (summary?.reach || 1)) * 100).toFixed(2));
    if (ctr < 0.25) {
      suggestions.push(
        "A/B test CTA buttons and first-line hooks to improve click-through rate from social posts."
      );
    }
  }

  if (focusAreas.length > 0) {
    suggestions.push(`Prioritize the requested focus areas: ${focusAreas.join(", ")}.`);
  }

  if ((alertResult?.counts?.stale || 0) > 0) {
    suggestions.push(
      "Archive stale posts and recycle their core idea with updated visuals and a softer call-to-action."
    );
  }

  return unique(suggestions).slice(0, 6);
}

function createChangeRequest({ message, summary, rows }) {
  const focusAreas = detectFocusAreas(message);
  const { topPosts, lowPosts } = rankPosts(rows);
  const alerts = evaluateAlerts(summary, rows);

  const suggestedActions = buildSuggestions(message, summary, rows, alerts).map((text, index) => ({
    id: `action_${index + 1}`,
    text,
  }));

  return {
    id: `change_${Date.now()}`,
    createdAt: new Date().toISOString(),
    ownerMessage: safeString(message),
    focusAreas,
    metricsSnapshot: {
      summary,
      topPosts,
      lowPosts,
      alertCounts: alerts.counts,
    },
    suggestedActions,
  };
}

function buildCursorPrompt(changeRequest) {
  const payload = changeRequest || {};
  const focusAreas = Array.isArray(payload.focusAreas) ? payload.focusAreas : [];
  const actions = Array.isArray(payload.suggestedActions) ? payload.suggestedActions : [];

  const actionLines = actions.length
    ? actions.map((action) => `- ${action.text}`).join("\n")
    : "- Review current social performance data and propose clear next actions.";

  return [
    "Implement owner-approved campaign optimizations for Window Depot USA of Milwaukee.",
    "",
    `Owner request: ${safeString(payload.ownerMessage) || "N/A"}`,
    `Focus areas: ${focusAreas.join(", ") || "general optimization"}`,
    "",
    "Requested actions:",
    actionLines,
    "",
    "Constraints:",
    "- Keep brand voice warm, local, and no-pressure.",
    "- Do not change public landing page behavior unless explicitly requested.",
    "- Preserve factual claims (4.9 stars, 1,000+ reviews, $500 gift card, 12-month price lock).",
    "",
    "Structured request payload:",
    JSON.stringify(payload, null, 2),
  ].join("\n");
}

module.exports = {
  buildSuggestions,
  createChangeRequest,
  buildCursorPrompt,
};
