const { guardMethods, sendJson } = require("../_lib/http");
const { getOwnerSessionFromRequest } = require("../_lib/auth");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["GET"])) return;

  const result = getOwnerSessionFromRequest(req);
  sendJson(res, 200, {
    ok: true,
    authenticated: result.authenticated,
    session: result.authenticated
      ? {
          role: result.session.role || "owner",
          exp: result.session.exp,
          expiresAt: new Date(Number(result.session.exp || 0) * 1000).toISOString(),
        }
      : null,
    reason: result.reason,
  });
};
