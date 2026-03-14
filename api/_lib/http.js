const DEFAULT_JSON_HEADERS = {
  "Content-Type": "application/json; charset=utf-8",
  "Cache-Control": "no-store",
};

function sendJson(res, statusCode, payload, extraHeaders = {}) {
  res.statusCode = statusCode;
  const headers = { ...DEFAULT_JSON_HEADERS, ...extraHeaders };
  Object.entries(headers).forEach(([key, value]) => {
    res.setHeader(key, value);
  });
  res.end(JSON.stringify(payload));
}

function sendError(res, statusCode, message, extra = {}) {
  sendJson(res, statusCode, {
    ok: false,
    error: message,
    ...extra,
  });
}

function methodNotAllowed(res, allowedMethods) {
  res.setHeader("Allow", allowedMethods.join(", "));
  sendError(res, 405, "Method not allowed", { allowedMethods });
}

function normalizeMethods(methods) {
  if (!Array.isArray(methods)) {
    return [String(methods || "").toUpperCase()].filter(Boolean);
  }
  return methods.map((method) => String(method || "").toUpperCase()).filter(Boolean);
}

function guardMethods(req, res, allowedMethods) {
  const normalizedAllowedMethods = normalizeMethods(allowedMethods);
  const requestMethod = String(req.method || "").toUpperCase();
  if (!normalizedAllowedMethods.includes(requestMethod)) {
    methodNotAllowed(res, normalizedAllowedMethods);
    return false;
  }
  return true;
}

function parseCookies(req) {
  const header = req.headers?.cookie;
  if (!header) return {};

  return header.split(";").reduce((acc, segment) => {
    const [key, ...rest] = segment.trim().split("=");
    if (!key) return acc;
    acc[key] = decodeURIComponent(rest.join("=") || "");
    return acc;
  }, {});
}

function parseQuery(req) {
  const url = new URL(req.url || "/", "http://localhost");
  return Object.fromEntries(url.searchParams.entries());
}

async function parseJsonBody(req, options = {}) {
  const maxBytes = Number(options.maxBytes || 1024 * 1024);

  if (req.body && typeof req.body === "object") {
    return req.body;
  }

  if (typeof req.body === "string" && req.body.length > 0) {
    try {
      return JSON.parse(req.body);
    } catch (error) {
      const parseError = new Error("Invalid JSON body");
      parseError.statusCode = 400;
      throw parseError;
    }
  }

  return new Promise((resolve, reject) => {
    let raw = "";
    let totalBytes = 0;

    req.on("data", (chunk) => {
      totalBytes += chunk.length;
      if (totalBytes > maxBytes) {
        const sizeError = new Error("Request body too large");
        sizeError.statusCode = 413;
        reject(sizeError);
        req.destroy();
        return;
      }
      raw += chunk.toString("utf8");
    });

    req.on("end", () => {
      if (!raw.trim()) {
        resolve({});
        return;
      }

      try {
        resolve(JSON.parse(raw));
      } catch (error) {
        const parseError = new Error("Invalid JSON body");
        parseError.statusCode = 400;
        reject(parseError);
      }
    });

    req.on("error", (error) => {
      reject(error);
    });
  });
}

module.exports = {
  sendJson,
  sendError,
  methodNotAllowed,
  guardMethods,
  parseCookies,
  parseQuery,
  parseJsonBody,
};
