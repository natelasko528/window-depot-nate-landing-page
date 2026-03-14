function safeNumber(value) {
  if (typeof value === "number" && Number.isFinite(value)) return value;
  const numeric = Number(value);
  return Number.isFinite(numeric) ? numeric : 0;
}

function createAlert(type, severity, message, context = {}) {
  return {
    type,
    severity,
    message,
    context,
  };
}

function calculatePostAgeHours(post) {
  const publishedAt = post?.publishedAt;
  if (!publishedAt) return null;
  const date = new Date(publishedAt);
  if (Number.isNaN(date.getTime())) return null;
  return (Date.now() - date.getTime()) / (1000 * 60 * 60);
}

function evaluatePostAlerts(posts) {
  const alerts = [];

  posts.forEach((post) => {
    const impressions = safeNumber(post?.metrics?.impressions);
    const clicks = safeNumber(post?.metrics?.clicks);
    const engagementRate = safeNumber(post?.metrics?.engagementRate);
    const postAgeHours = calculatePostAgeHours(post);

    if (impressions >= 100 && engagementRate >= 2) {
      alerts.push(
        createAlert("high_performer", "info", "High-performing post identified", {
          postId: post.id,
          platform: post.platform,
          engagementRate,
          impressions,
        })
      );
    }

    if ((postAgeHours || 0) >= 24 && impressions >= 100 && engagementRate < 0.5) {
      alerts.push(
        createAlert("low_performer", "warning", "Low-performing post needs optimization", {
          postId: post.id,
          platform: post.platform,
          engagementRate,
          impressions,
        })
      );
    }

    if ((postAgeHours || 0) >= 72 && impressions < 25 && clicks === 0) {
      alerts.push(
        createAlert("stale_post", "warning", "Post appears stale with no meaningful activity", {
          postId: post.id,
          platform: post.platform,
          ageHours: Number((postAgeHours || 0).toFixed(1)),
          impressions,
          clicks,
        })
      );
    }
  });

  return alerts;
}

function evaluateSummaryAlerts(summary) {
  const alerts = [];
  const reach = safeNumber(summary?.reach);
  const clicks = safeNumber(summary?.clicks);
  const engagementRate = safeNumber(summary?.engagementRate);

  if (reach > 0 && clicks > 0) {
    const ctr = Number(((clicks / reach) * 100).toFixed(2));
    if (ctr < 0.25) {
      alerts.push(
        createAlert("low_ctr", "warning", "Overall click-through rate is below target", {
          ctr,
          clicks,
          reach,
        })
      );
    }
  }

  if (reach > 0 && engagementRate < 1) {
    alerts.push(
      createAlert("low_engagement", "warning", "Overall engagement rate is below 1%", {
        engagementRate,
        reach,
      })
    );
  }

  return alerts;
}

function evaluateAlerts(summary, posts) {
  const postAlerts = evaluatePostAlerts(Array.isArray(posts) ? posts : []);
  const summaryAlerts = evaluateSummaryAlerts(summary || {});
  const alerts = [...postAlerts, ...summaryAlerts];

  return {
    alerts,
    counts: {
      total: alerts.length,
      high: alerts.filter((item) => item.type === "high_performer").length,
      low: alerts.filter((item) => item.type === "low_performer").length,
      stale: alerts.filter((item) => item.type === "stale_post").length,
      warning: alerts.filter((item) => item.severity === "warning").length,
    },
  };
}

module.exports = {
  evaluateAlerts,
};
