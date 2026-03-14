const { guardMethods, sendJson } = require("../_lib/http");
const { clearOwnerSessionCookie } = require("../_lib/auth");

module.exports = async function handler(req, res) {
  if (!guardMethods(req, res, ["POST"])) return;

  res.setHeader("Set-Cookie", clearOwnerSessionCookie());
  sendJson(res, 200, {
    ok: true,
    authenticated: false,
  });
};
