const { guardMethods, parseJsonBody, sendError, sendJson } = require("../_lib/http");
const { requireOwnerSession } = require("../_lib/auth");
const { buildCursorPrompt, createChangeRequest } = require("../_lib/owner-tools");

function safeString(value) {
  if (typeof value === "string") return value;
  if (value == null) return "";
  return String(value);
}

async function postWebhook(url, token, payload) {
  const abortController = new AbortController();
  const timeout = setTimeout(() => abortController.abort(), 10000);
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
      signal: abortController.signal,
    });

    const rawBody = await response.text();
    let parsedBody;
    try {
      parsedBody = JSON.parse(rawBody);
    } catch (error) {
      parsedBody = rawBody;
    }

    return {
      ok: response.ok,
      statusCode: response.status,
      response: parsedBody,
    };
  } finally {
    clearTimeout(timeout);
  }
}

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["POST"])) return;
  if (!requireOwnerSession(req, res)) return;

  try {
    const body = await parseJsonBody(req);
    let changeRequest = body?.changeRequest;

    if (!changeRequest && typeof body?.request === "string") {
      changeRequest = createChangeRequest({
        message: body.request,
        summary: body?.context?.kpis || {},
        rows: body?.context?.visiblePosts || [],
      });
    }

    if (!changeRequest || typeof changeRequest !== "object") {
      sendError(res, 400, "changeRequest is required");
      return;
    }

    const cursorPrompt = buildCursorPrompt(changeRequest);
    const webhookUrl = safeString(process.env.CURSOR_AGENT_WEBHOOK_URL).trim();
    const webhookToken = safeString(process.env.CURSOR_AGENT_WEBHOOK_TOKEN).trim();

    let webhook = {
      attempted: false,
      dispatched: false,
      skippedReason: null,
    };

    if (webhookUrl && webhookToken) {
      webhook.attempted = true;
      const webhookPayload = {
        source: "owner_dashboard",
        exportedAt: new Date().toISOString(),
        changeRequest,
        cursorPrompt,
      };

      try {
        const delivery = await postWebhook(webhookUrl, webhookToken, webhookPayload);
        webhook = {
          attempted: true,
          dispatched: delivery.ok,
          statusCode: delivery.statusCode,
          response: delivery.response,
        };
      } catch (error) {
        webhook = {
          attempted: true,
          dispatched: false,
          error: error?.message || "Webhook dispatch failed",
        };
      }
    } else {
      webhook.skippedReason =
        "Webhook not sent because CURSOR_AGENT_WEBHOOK_URL and CURSOR_AGENT_WEBHOOK_TOKEN must both be set";
    }

    sendJson(res, 200, {
      ok: true,
      cursorPrompt,
      webhook,
    });
  } catch (error) {
    const statusCode = Number(error.statusCode || 500);
    sendError(res, statusCode, error.message || "Unable to export owner request");
  }
};
