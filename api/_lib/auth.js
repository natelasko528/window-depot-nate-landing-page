const crypto = require("crypto");
const { parseCookies, sendError } = require("./http");

const OWNER_SESSION_COOKIE = "owner_session";
const DEFAULT_SESSION_TTL_SECONDS = 60 * 60 * 12; // 12 hours

function base64UrlEncode(input) {
  return Buffer.from(input)
    .toString("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/g, "");
}

function base64UrlDecode(input) {
  const normalized = String(input || "").replace(/-/g, "+").replace(/_/g, "/");
  const padded = normalized + "=".repeat((4 - (normalized.length % 4)) % 4);
  return Buffer.from(padded, "base64").toString("utf8");
}

function safeString(value) {
  if (typeof value === "string") return value;
  if (value == null) return "";
  return String(value);
}

function timingSafeEqualString(a, b) {
  const left = Buffer.from(safeString(a));
  const right = Buffer.from(safeString(b));
  if (left.length !== right.length) return false;
  return crypto.timingSafeEqual(left, right);
}

function getSessionSecret() {
  return safeString(process.env.SESSION_SECRET);
}

function getCookieSecureFlag() {
  if (process.env.NODE_ENV === "development") return false;
  return true;
}

function signValue(value, secret) {
  return crypto.createHmac("sha256", secret).update(value).digest("hex");
}

function serializeCookie(name, value, options = {}) {
  const parts = [`${name}=${encodeURIComponent(value || "")}`];

  if (typeof options.maxAge === "number") {
    parts.push(`Max-Age=${Math.max(0, Math.floor(options.maxAge))}`);
  }

  if (options.expires instanceof Date) {
    parts.push(`Expires=${options.expires.toUTCString()}`);
  }

  parts.push(`Path=${options.path || "/"}`);

  if (options.httpOnly !== false) parts.push("HttpOnly");
  if (options.secure) parts.push("Secure");
  if (options.sameSite) parts.push(`SameSite=${options.sameSite}`);

  return parts.join("; ");
}

function createSignedOwnerSession(payload = {}, options = {}) {
  const secret = getSessionSecret();
  if (!secret) {
    const error = new Error("SESSION_SECRET is not configured");
    error.statusCode = 500;
    throw error;
  }

  const ttlSeconds = Number(options.ttlSeconds || DEFAULT_SESSION_TTL_SECONDS);
  const nowSeconds = Math.floor(Date.now() / 1000);
  const sessionPayload = {
    sub: "owner",
    iat: nowSeconds,
    exp: nowSeconds + ttlSeconds,
    ...payload,
  };

  const encodedPayload = base64UrlEncode(JSON.stringify(sessionPayload));
  const signature = signValue(encodedPayload, secret);
  const token = `${encodedPayload}.${signature}`;
  const expiresAt = new Date(sessionPayload.exp * 1000);

  const cookie = serializeCookie(OWNER_SESSION_COOKIE, token, {
    maxAge: ttlSeconds,
    expires: expiresAt,
    path: "/",
    httpOnly: true,
    secure: options.secure ?? getCookieSecureFlag(),
    sameSite: "Lax",
  });

  return {
    token,
    expiresAt,
    cookie,
  };
}

function clearOwnerSessionCookie() {
  return serializeCookie(OWNER_SESSION_COOKIE, "", {
    maxAge: 0,
    expires: new Date(0),
    path: "/",
    httpOnly: true,
    secure: getCookieSecureFlag(),
    sameSite: "Lax",
  });
}

function verifyOwnerSessionToken(token) {
  if (!token || typeof token !== "string" || !token.includes(".")) {
    return { valid: false, reason: "missing_token" };
  }

  const secret = getSessionSecret();
  if (!secret) {
    return { valid: false, reason: "missing_secret" };
  }

  const [encodedPayload, signature] = token.split(".");
  if (!encodedPayload || !signature) {
    return { valid: false, reason: "invalid_token_format" };
  }

  const expectedSignature = signValue(encodedPayload, secret);
  if (!timingSafeEqualString(signature, expectedSignature)) {
    return { valid: false, reason: "signature_mismatch" };
  }

  try {
    const payload = JSON.parse(base64UrlDecode(encodedPayload));
    const exp = Number(payload?.exp || 0);
    if (exp <= Math.floor(Date.now() / 1000)) {
      return { valid: false, reason: "session_expired" };
    }

    return { valid: true, payload };
  } catch (error) {
    return { valid: false, reason: "payload_decode_failed" };
  }
}

function getOwnerSessionFromRequest(req) {
  const cookies = parseCookies(req);
  const token = cookies[OWNER_SESSION_COOKIE];
  const verified = verifyOwnerSessionToken(token);

  if (!verified.valid) {
    return {
      authenticated: false,
      reason: verified.reason,
      session: null,
    };
  }

  return {
    authenticated: true,
    reason: "ok",
    session: verified.payload,
  };
}

function requireOwnerSession(req, res) {
  const sessionResult = getOwnerSessionFromRequest(req);
  if (!sessionResult.authenticated) {
    sendError(res, 401, "Authentication required");
    return null;
  }
  return sessionResult.session;
}

function verifyOwnerPassword(inputPassword) {
  const expectedPassword = safeString(process.env.OWNER_DASHBOARD_PASSWORD);
  if (!expectedPassword) return false;
  return timingSafeEqualString(inputPassword, expectedPassword);
}

function getCronAuthToken(req) {
  const authHeader = safeString(req.headers?.authorization);
  if (authHeader.toLowerCase().startsWith("bearer ")) {
    return authHeader.slice(7).trim();
  }

  return safeString(req.headers?.["x-cron-secret"]);
}

function verifyCronRequest(req) {
  const sharedSecret = safeString(process.env.CRON_SHARED_SECRET || process.env.CRON_SECRET);
  if (!sharedSecret) {
    return {
      ok: true,
      enforced: false,
      reason: "CRON_SHARED_SECRET/CRON_SECRET not configured",
    };
  }

  const incoming = getCronAuthToken(req);
  if (!incoming) {
    return {
      ok: false,
      enforced: true,
      reason: "Missing cron auth token",
    };
  }

  if (!timingSafeEqualString(incoming, sharedSecret)) {
    return {
      ok: false,
      enforced: true,
      reason: "Invalid cron auth token",
    };
  }

  return {
    ok: true,
    enforced: true,
    reason: "Cron auth token verified",
  };
}

module.exports = {
  OWNER_SESSION_COOKIE,
  createSignedOwnerSession,
  clearOwnerSessionCookie,
  verifyOwnerSessionToken,
  getOwnerSessionFromRequest,
  requireOwnerSession,
  verifyOwnerPassword,
  verifyCronRequest,
};
