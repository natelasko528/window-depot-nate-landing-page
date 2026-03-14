const fs = require("fs/promises");
const http = require("http");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const PORT = Number(process.env.OWNER_DEV_PORT || 4173);

const MIME_TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
};

function toFilePath(urlPath) {
  if (!urlPath || urlPath === "/") return path.join(ROOT, "index.html");
  if (urlPath === "/owner") return path.join(ROOT, "owner", "index.html");
  if (urlPath === "/owner/") return path.join(ROOT, "owner", "index.html");
  if (urlPath === "/owner/dashboard") return path.join(ROOT, "owner", "dashboard", "index.html");
  if (urlPath === "/owner/dashboard/") return path.join(ROOT, "owner", "dashboard", "index.html");
  return path.join(ROOT, decodeURIComponent(urlPath.replace(/^\/+/, "")));
}

function safeApiModulePath(urlPath) {
  const cleanPath = decodeURIComponent(urlPath.split("?")[0]).replace(/^\/+/, "");
  const modulePath = path.join(ROOT, `${cleanPath}.js`);
  if (!modulePath.startsWith(path.join(ROOT, "api"))) {
    return null;
  }
  return modulePath;
}

async function serveStatic(req, res) {
  const url = new URL(req.url || "/", "http://localhost");
  let filePath = toFilePath(url.pathname);
  try {
    let stat = await fs.stat(filePath);
    if (stat.isDirectory()) {
      filePath = path.join(filePath, "index.html");
      stat = await fs.stat(filePath);
    }
    if (!stat.isFile()) {
      throw new Error("Not a file");
    }

    const content = await fs.readFile(filePath);
    const ext = path.extname(filePath).toLowerCase();
    res.statusCode = 200;
    res.setHeader("Content-Type", MIME_TYPES[ext] || "application/octet-stream");
    res.end(content);
  } catch (_error) {
    res.statusCode = 404;
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(JSON.stringify({ ok: false, error: "Not found" }));
  }
}

async function serveApi(req, res) {
  const modulePath = safeApiModulePath(req.url || "");
  if (!modulePath) {
    res.statusCode = 400;
    res.end("Invalid API path");
    return;
  }
  try {
    delete require.cache[require.resolve(modulePath)];
    const handler = require(modulePath);
    await handler(req, res);
  } catch (error) {
    res.statusCode = Number(error.statusCode || 500);
    res.setHeader("Content-Type", "application/json; charset=utf-8");
    res.end(
      JSON.stringify({
        ok: false,
        error: "API handler failed",
        details: error.message,
      })
    );
  }
}

const server = http.createServer(async (req, res) => {
  const pathname = new URL(req.url || "/", "http://localhost").pathname;
  if (pathname.startsWith("/api/")) {
    await serveApi(req, res);
    return;
  }
  await serveStatic(req, res);
});

server.listen(PORT, () => {
  process.stdout.write(`Owner dev server running on http://localhost:${PORT}\n`);
});
