(function ownerDashboardScript() {
  "use strict";

  if (!window.OwnerUI) {
    return;
  }

  const ui = window.OwnerUI;
  const state = {
    live: null,
    posts: [],
    filteredPosts: [],
    chatHistory: [],
    lastChangeRequest: null,
    lastExportPrompt: "",
    refreshTimerId: null
  };

  function escapeHtml(value) {
    return String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  function normalizePlatform(value) {
    const platform = String(value || "unknown").trim().toLowerCase();
    if (platform === "fb" || platform === "facebook") {
      return "facebook";
    }
    if (platform === "ig" || platform === "instagram") {
      return "instagram";
    }
    if (platform === "linkedin" || platform === "li") {
      return "linkedin";
    }
    return platform || "unknown";
  }

  function platformLabel(platform) {
    if (platform === "facebook") {
      return "Facebook";
    }
    if (platform === "instagram") {
      return "Instagram";
    }
    if (platform === "linkedin") {
      return "LinkedIn";
    }
    return platform.charAt(0).toUpperCase() + platform.slice(1);
  }

  function normalizePosts(raw) {
    const payload = ui.toPayload(raw);
    const source = Array.isArray(payload)
      ? payload
      : Array.isArray(payload && payload.posts)
        ? payload.posts
        : Array.isArray(payload && payload.rows)
          ? payload.rows
        : [];

    return source.map(function mapPost(item, index) {
      const metrics = item && typeof item === "object" && item.metrics && typeof item.metrics === "object"
        ? item.metrics
        : {};
      const impressions = ui.safeNumber(item.impressions || metrics.impressions);
      const reach = ui.safeNumber(item.reach || metrics.reach);
      const clicks = ui.safeNumber(item.clicks || metrics.clicks);
      const engagements = ui.safeNumber(item.engagements || metrics.engagements || metrics.engagement);
      const computedRate = impressions > 0
        ? (engagements > 0 ? (engagements / impressions) * 100 : 0)
        : 0;
      const engagementRate = Number.isFinite(Number(item.engagementRate))
        ? ui.safeNumber(item.engagementRate)
        : (Number.isFinite(Number(metrics.engagementRate))
          ? ui.safeNumber(metrics.engagementRate)
          : computedRate);

      return {
        id: item.id || item.postId || "post-" + (index + 1),
        title: item.title || item.caption || item.name || item.contentSnippet || "Untitled post",
        platform: normalizePlatform(item.platform),
        publishedAt: item.publishedAt || item.scheduledAt || item.createdAt || item.scheduleDate || null,
        impressions: impressions,
        reach: reach,
        clicks: clicks,
        engagementRate: engagementRate,
        url: item.url || item.postUrl || item.mediaUrl || ""
      };
    });
  }

  function aggregateFromPosts(posts) {
    const totals = {
      impressions: 0,
      reach: 0,
      clicks: 0
    };
    let weightedRateSum = 0;
    let weightedRateCount = 0;

    posts.forEach(function eachPost(post) {
      totals.impressions += ui.safeNumber(post.impressions);
      totals.reach += ui.safeNumber(post.reach);
      totals.clicks += ui.safeNumber(post.clicks);
      const weight = post.impressions > 0 ? post.impressions : 1;
      weightedRateSum += ui.safeNumber(post.engagementRate) * weight;
      weightedRateCount += weight;
    });

    return {
      impressions: totals.impressions,
      reach: totals.reach,
      clicks: totals.clicks,
      engagementRate: weightedRateCount > 0 ? (weightedRateSum / weightedRateCount) : 0
    };
  }

  function aggregatePlatforms(posts) {
    const map = {
      facebook: { platform: "facebook", impressions: 0, reach: 0, clicks: 0, weightedRateSum: 0, weightedRateCount: 0 },
      instagram: { platform: "instagram", impressions: 0, reach: 0, clicks: 0, weightedRateSum: 0, weightedRateCount: 0 },
      linkedin: { platform: "linkedin", impressions: 0, reach: 0, clicks: 0, weightedRateSum: 0, weightedRateCount: 0 }
    };

    posts.forEach(function eachPost(post) {
      const key = map[post.platform] ? post.platform : "linkedin";
      const target = map[key];
      target.impressions += ui.safeNumber(post.impressions);
      target.reach += ui.safeNumber(post.reach);
      target.clicks += ui.safeNumber(post.clicks);
      const weight = post.impressions > 0 ? post.impressions : 1;
      target.weightedRateSum += ui.safeNumber(post.engagementRate) * weight;
      target.weightedRateCount += weight;
    });

    return Object.keys(map).map(function toEntry(key) {
      const item = map[key];
      return {
        platform: key,
        impressions: item.impressions,
        reach: item.reach,
        clicks: item.clicks,
        engagementRate: item.weightedRateCount > 0 ? item.weightedRateSum / item.weightedRateCount : 0
      };
    });
  }

  function rankPosts(posts, direction) {
    const sorted = posts.slice().sort(function compare(a, b) {
      const rateDiff = ui.safeNumber(b.engagementRate) - ui.safeNumber(a.engagementRate);
      if (rateDiff !== 0) {
        return rateDiff;
      }
      return ui.safeNumber(b.clicks) - ui.safeNumber(a.clicks);
    });
    return direction === "bottom" ? sorted.reverse().slice(0, 5) : sorted.slice(0, 5);
  }

  function normalizeLive(raw, posts, sourceHealthy) {
    const payload = ui.toPayload(raw) || {};
    const summary = payload.summary && typeof payload.summary === "object" ? payload.summary : {};
    const fallbackKpis = aggregateFromPosts(posts);
    const kpis = payload.kpis || payload.metrics || summary || {};
    const normalizedKpis = {
      impressions: ui.safeNumber(kpis.impressions || fallbackKpis.impressions),
      reach: ui.safeNumber(kpis.reach || fallbackKpis.reach),
      clicks: ui.safeNumber(kpis.clicks || fallbackKpis.clicks),
      engagementRate: ui.safeNumber(kpis.engagementRate || fallbackKpis.engagementRate)
    };
    const platformBreakdown = Array.isArray(payload.platformBreakdown)
      ? payload.platformBreakdown.map(function mapPlatform(item) {
          return {
            platform: normalizePlatform(item.platform),
            impressions: ui.safeNumber(item.impressions),
            reach: ui.safeNumber(item.reach),
            clicks: ui.safeNumber(item.clicks),
            engagementRate: ui.safeNumber(item.engagementRate)
          };
        })
      : aggregatePlatforms(posts);

    return {
      kpis: normalizedKpis,
      platformBreakdown: platformBreakdown,
      topPosts: Array.isArray(payload.topPosts) ? payload.topPosts : rankPosts(posts, "top"),
      bottomPosts: Array.isArray(payload.bottomPosts) ? payload.bottomPosts : rankPosts(posts, "bottom"),
      alerts: Array.isArray(payload.alerts) ? payload.alerts : [],
      health: payload.health || (sourceHealthy ? "ok" : "degraded"),
      lastSync:
        payload.lastSync ||
        payload.lastSyncedAt ||
        payload.meta?.fetchedAt ||
        payload.meta?.syncedAt ||
        new Date().toISOString()
    };
  }

  function renderKpis(live) {
    ui.el("#kpiImpressions").textContent = ui.formatNumber(live.kpis.impressions);
    ui.el("#kpiReach").textContent = ui.formatNumber(live.kpis.reach);
    ui.el("#kpiClicks").textContent = ui.formatNumber(live.kpis.clicks);
    ui.el("#kpiEngagementRate").textContent = ui.formatPercent(live.kpis.engagementRate);
    ui.el("#lastSyncValue").textContent = ui.formatDate(live.lastSync);

    const badge = ui.el("#apiHealthBadge");
    if (badge) {
      const health = String(live.health || "unknown").toLowerCase();
      badge.textContent = "API: " + health;
      badge.style.color = health === "ok" ? "#0d6f35" : "#9b1c1c";
      badge.style.background = health === "ok" ? "#eaf7ef" : "#fbe8e8";
    }
  }

  function renderPlatformBreakdown(items) {
    const container = ui.el("#platformBreakdown");
    if (!container) {
      return;
    }
    if (!items.length) {
      container.innerHTML = "<p class=\"owner-status\">No platform data available yet.</p>";
      return;
    }

    container.innerHTML = items.map(function card(item) {
      const label = platformLabel(normalizePlatform(item.platform));
      return [
        "<article class=\"owner-platform-card\">",
        "<h3>" + escapeHtml(label) + "</h3>",
        "<p class=\"owner-platform-metric\">Impressions: <strong>" + ui.formatNumber(item.impressions) + "</strong></p>",
        "<p class=\"owner-platform-metric\">Reach: <strong>" + ui.formatNumber(item.reach) + "</strong></p>",
        "<p class=\"owner-platform-metric\">Clicks: <strong>" + ui.formatNumber(item.clicks) + "</strong></p>",
        "<p class=\"owner-platform-metric\">Eng. Rate: <strong>" + ui.formatPercent(item.engagementRate) + "</strong></p>",
        "</article>"
      ].join("");
    }).join("");
  }

  function formatRankedPost(item) {
    const title = item.title || item.name || "Untitled post";
    const platform = platformLabel(normalizePlatform(item.platform || "unknown"));
    const rate = ui.safeNumber(item.engagementRate || item.rate);
    const clicks = ui.safeNumber(item.clicks);

    return (
      "<li class=\"owner-ranked-item\">" +
      "<strong>" + escapeHtml(title) + "</strong>" +
      "<p class=\"owner-ranked-meta\">" +
      escapeHtml(platform) + " \u2022 " + ui.formatPercent(rate) + " \u2022 " + ui.formatNumber(clicks) + " clicks" +
      "</p>" +
      "</li>"
    );
  }

  function renderRanked() {
    const top = state.live ? state.live.topPosts : [];
    const bottom = state.live ? state.live.bottomPosts : [];
    const topList = ui.el("#topPostsList");
    const bottomList = ui.el("#bottomPostsList");

    if (topList) {
      topList.innerHTML = top.length
        ? top.map(formatRankedPost).join("")
        : "<li class=\"owner-ranked-item\"><strong>No top posts yet.</strong><p class=\"owner-ranked-meta\">Data will appear after sync.</p></li>";
    }
    if (bottomList) {
      bottomList.innerHTML = bottom.length
        ? bottom.map(formatRankedPost).join("")
        : "<li class=\"owner-ranked-item\"><strong>No bottom posts yet.</strong><p class=\"owner-ranked-meta\">Data will appear after sync.</p></li>";
    }
  }

  function renderAlerts() {
    const alerts = state.live ? state.live.alerts : [];
    const target = ui.el("#alertsList");
    if (!target) {
      return;
    }

    if (!alerts.length) {
      target.innerHTML = "<li class=\"owner-alert-item\"><strong>No active alerts.</strong><p class=\"owner-alert-meta\">Performance is currently stable.</p></li>";
      return;
    }

    target.innerHTML = alerts.map(function mapAlert(alertItem) {
      if (typeof alertItem === "string") {
        return "<li class=\"owner-alert-item\"><strong>Notice</strong><p class=\"owner-alert-meta\">" + escapeHtml(alertItem) + "</p></li>";
      }
      const title = alertItem.title || alertItem.type || "Alert";
      const detail = alertItem.message || alertItem.description || "Review this item in detail.";
      return (
        "<li class=\"owner-alert-item\">" +
        "<strong>" + escapeHtml(title) + "</strong>" +
        "<p class=\"owner-alert-meta\">" + escapeHtml(detail) + "</p>" +
        "</li>"
      );
    }).join("");
  }

  function parseSortValue(value) {
    const parts = String(value || "").split(":");
    return {
      key: parts[0] || "engagementRate",
      direction: parts[1] === "asc" ? "asc" : "desc"
    };
  }

  function applyFiltersAndRenderTable() {
    const searchInput = ui.el("#postSearchInput");
    const platformFilter = ui.el("#platformFilter");
    const sortFilter = ui.el("#sortFilter");

    const query = String(searchInput && searchInput.value || "").trim().toLowerCase();
    const selectedPlatform = String(platformFilter && platformFilter.value || "all").toLowerCase();
    const sortSpec = parseSortValue(sortFilter && sortFilter.value);

    state.filteredPosts = state.posts.filter(function filterPost(post) {
      const matchesPlatform = selectedPlatform === "all" || post.platform === selectedPlatform;
      if (!matchesPlatform) {
        return false;
      }
      if (!query) {
        return true;
      }
      const haystack = [
        post.title,
        post.id,
        post.platform
      ].join(" ").toLowerCase();
      return haystack.includes(query);
    }).sort(function sortPosts(a, b) {
      const aVal = a[sortSpec.key];
      const bVal = b[sortSpec.key];
      let diff;
      if (sortSpec.key === "publishedAt") {
        diff = new Date(aVal || 0).getTime() - new Date(bVal || 0).getTime();
      } else {
        diff = ui.safeNumber(aVal) - ui.safeNumber(bVal);
      }
      return sortSpec.direction === "asc" ? diff : -diff;
    });

    const body = ui.el("#postsTableBody");
    const count = ui.el("#postsCount");
    if (count) {
      count.textContent = String(state.filteredPosts.length);
    }
    if (!body) {
      return;
    }
    if (!state.filteredPosts.length) {
      body.innerHTML = "<tr><td colspan=\"7\">No posts match your search/filter.</td></tr>";
      return;
    }

    body.innerHTML = state.filteredPosts.map(function row(post) {
      const postTitle = post.url
        ? "<a href=\"" + escapeHtml(post.url) + "\" target=\"_blank\" rel=\"noopener noreferrer\">" + escapeHtml(post.title) + "</a>"
        : escapeHtml(post.title);
      return [
        "<tr>",
        "<td>" + postTitle + "<br><small>" + escapeHtml(post.id) + "</small></td>",
        "<td>" + escapeHtml(platformLabel(post.platform)) + "</td>",
        "<td>" + escapeHtml(ui.formatDate(post.publishedAt)) + "</td>",
        "<td>" + ui.formatNumber(post.impressions) + "</td>",
        "<td>" + ui.formatNumber(post.reach) + "</td>",
        "<td>" + ui.formatPercent(post.engagementRate) + "</td>",
        "<td>" + ui.formatNumber(post.clicks) + "</td>",
        "</tr>"
      ].join("");
    }).join("");
  }

  function appendChat(role, text) {
    const chatContainer = ui.el("#chatMessages");
    if (!chatContainer) {
      return;
    }
    const bubble = document.createElement("div");
    bubble.className = "owner-chat-bubble " + (role === "user" ? "user" : "assistant");
    bubble.textContent = text;
    chatContainer.appendChild(bubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function latestUserPrompt() {
    for (let i = state.chatHistory.length - 1; i >= 0; i -= 1) {
      if (state.chatHistory[i].role === "user") {
        return state.chatHistory[i].text;
      }
    }
    return "Provide a concise owner action plan for campaign performance this week.";
  }

  function chatContext() {
    const live = state.live || { kpis: {} };
    return {
      kpis: live.kpis || {},
      platformBreakdown: live.platformBreakdown || [],
      topPosts: (live.topPosts || []).slice(0, 3),
      bottomPosts: (live.bottomPosts || []).slice(0, 3),
      visiblePosts: state.filteredPosts.slice(0, 20)
    };
  }

  async function handleChatSubmit(event) {
    event.preventDefault();
    const input = ui.el("#chatInput");
    const submitButton = ui.el("#chatForm button[type='submit']");
    if (!input) {
      return;
    }
    const message = input.value.trim();
    if (!message) {
      return;
    }

    input.value = "";
    state.chatHistory.push({ role: "user", text: message });
    appendChat("user", message);

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.textContent = "Sending...";
    }

    const response = await ui.fetchJson("/api/owner/chat", {
      method: "POST",
      body: {
        message: message,
        context: chatContext(),
        history: state.chatHistory.slice(-12)
      }
    });

    if (submitButton) {
      submitButton.disabled = false;
      submitButton.textContent = "Send";
    }

    if (!response.ok) {
      appendChat("assistant", "I could not reach owner chat right now. Please retry in a moment.");
      return;
    }

    const payload = ui.toPayload(response.data) || {};
    const reply = payload.reply || payload.response || payload.message || "I reviewed the latest numbers and prepared recommendations.";
    const suggestions = Array.isArray(payload.suggestions) ? payload.suggestions : [];
    const suggestionText = suggestions.length
      ? "\n\nSuggestions:\n- " + suggestions.join("\n- ")
      : "";
    const assistantText = reply + suggestionText;
    appendChat("assistant", assistantText);
    state.chatHistory.push({ role: "assistant", text: assistantText });

    const exportPrompt = payload.exportPrompt || payload.cursorPrompt || payload.prompt;
    if (exportPrompt) {
      state.lastExportPrompt = String(exportPrompt);
    }
    if (payload.changeRequest && typeof payload.changeRequest === "object") {
      state.lastChangeRequest = payload.changeRequest;
    }
  }

  async function handleExportPrompt() {
    const output = ui.el("#exportPromptOutput");
    const button = ui.el("#exportPromptButton");
    if (button) {
      button.disabled = true;
      button.textContent = "Exporting...";
    }

    const response = await ui.fetchJson("/api/owner/export-request", {
      method: "POST",
      body: {
        changeRequest: state.lastChangeRequest || {
          ownerMessage: latestUserPrompt(),
          focusAreas: [],
          metricsSnapshot: chatContext(),
          suggestedActions: []
        }
      }
    });

    if (button) {
      button.disabled = false;
      button.textContent = "Export prompt";
    }

    if (!output) {
      return;
    }

    if (!response.ok) {
      output.hidden = false;
      output.textContent = "Export failed: " + (response.error || "Unknown error");
      return;
    }

    const payload = ui.toPayload(response.data) || {};
    const prompt = payload.prompt || payload.exportPrompt || payload.cursorPrompt || state.lastExportPrompt;
    if (!prompt) {
      output.hidden = false;
      output.textContent = "No export prompt returned.";
      return;
    }

    state.lastExportPrompt = String(prompt);
    output.hidden = false;
    output.textContent = state.lastExportPrompt;

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(state.lastExportPrompt).catch(function noop() {});
    }
  }

  async function refreshData() {
    const [liveResponse, postsResponse] = await Promise.all([
      ui.fetchJson("/api/performance/live"),
      ui.fetchJson("/api/performance/posts")
    ]);

    if (postsResponse.ok) {
      state.posts = normalizePosts(postsResponse.data);
    }

    if (liveResponse.ok || postsResponse.ok) {
      state.live = normalizeLive(liveResponse.data, state.posts, liveResponse.ok && postsResponse.ok);
    } else {
      state.live = normalizeLive(null, state.posts, false);
      state.live.alerts = [{
        title: "Data fetch failed",
        message: "Unable to load live metrics from API endpoints."
      }];
    }

    renderKpis(state.live);
    renderPlatformBreakdown(state.live.platformBreakdown);
    renderRanked();
    renderAlerts();
    applyFiltersAndRenderTable();
  }

  function attachFilterHandlers() {
    const search = ui.el("#postSearchInput");
    const platform = ui.el("#platformFilter");
    const sort = ui.el("#sortFilter");
    [search, platform, sort].forEach(function register(control) {
      if (control) {
        control.addEventListener("input", applyFiltersAndRenderTable);
        control.addEventListener("change", applyFiltersAndRenderTable);
      }
    });
  }

  function attachActions() {
    const refreshButton = ui.el("#refreshNowButton");
    const chatForm = ui.el("#chatForm");
    const exportButton = ui.el("#exportPromptButton");

    if (refreshButton) {
      refreshButton.addEventListener("click", refreshData);
    }
    if (chatForm) {
      chatForm.addEventListener("submit", handleChatSubmit);
    }
    if (exportButton) {
      exportButton.addEventListener("click", handleExportPrompt);
    }
  }

  async function init() {
    const session = await ui.checkSession({
      redirectIfUnauthed: true,
      redirectIfAuthed: false
    });
    if (!session) {
      return;
    }

    appendChat(
      "assistant",
      "Welcome back. Ask for performance insights, recommended campaign edits, or a cursor-ready change prompt."
    );

    attachFilterHandlers();
    attachActions();
    await refreshData();

    if (state.refreshTimerId) {
      clearInterval(state.refreshTimerId);
    }
    state.refreshTimerId = setInterval(refreshData, ui.REFRESH_MS);
  }

  document.addEventListener("DOMContentLoaded", function onLoaded() {
    init();
  });
})();
