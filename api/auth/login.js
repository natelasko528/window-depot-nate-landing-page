const { guardMethods, parseJsonBody, sendError, sendJson } = require("../_lib/http");
const { createSignedOwnerSession, verifyOwnerPassword } = require("../_lib/auth");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["POST"])) return;

  try {
    if (!process.env.OWNER_DASHBOARD_PASSWORD) {
      sendError(res, 500, "OWNER_DASHBOARD_PASSWORD is not configured");
      return;
    }

    const body = await parseJsonBody(req);
    const inputPassword = typeof body?.password === "string" ? body.password : "";

    if (!inputPassword) {
      sendError(res, 400, "Password is required");
      return;
    }

    const isValid = verifyOwnerPassword(inputPassword);
    if (!isValid) {
      sendError(res, 401, "Invalid credentials");
      return;
    }

    const session = createSignedOwnerSession({
      role: "owner",
    });

    res.setHeader("Set-Cookie", session.cookie);
    sendJson(res, 200, {
      ok: true,
      authenticated: true,
      expiresAt: session.expiresAt.toISOString(),
    });
  } catch (error) {
    const statusCode = Number(error.statusCode || 500);
    sendError(res, statusCode, error.message || "Login failed");
  }
};
