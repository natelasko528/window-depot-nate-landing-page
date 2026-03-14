const fs = require("fs/promises");
const path = require("path");

const DASHBOARD_DATA_DIR = path.join(
  process.cwd(),
  "ad-drafts",
  "30-posts",
  "owner-dashboard-data"
);
const LATEST_PERFORMANCE_FILE = path.join(DASHBOARD_DATA_DIR, "latest-performance.json");
const LATEST_ALERTS_FILE = path.join(DASHBOARD_DATA_DIR, "latest-alerts.json");

async function ensureDashboardDataDir() {
  await fs.mkdir(DASHBOARD_DATA_DIR, { recursive: true });
}

async function readJsonFile(filePath, fallback = null) {
  try {
    const raw = await fs.readFile(filePath, "utf8");
    return JSON.parse(raw);
  } catch (error) {
    if (error.code === "ENOENT") return fallback;
    throw error;
  }
}

async function writeJsonFile(filePath, payload) {
  await ensureDashboardDataDir();
  const serialized = `${JSON.stringify(payload, null, 2)}\n`;
  await fs.writeFile(filePath, serialized, "utf8");
}

function buildSnapshotFilePath(timestampISO) {
  const safeTimestamp = timestampISO.replace(/[:.]/g, "-");
  return path.join(DASHBOARD_DATA_DIR, `performance-${safeTimestamp}.json`);
}

async function writePerformanceSnapshot(snapshot) {
  const timestampISO = snapshot.generatedAt || new Date().toISOString();
  const payload = {
    ...snapshot,
    generatedAt: timestampISO,
  };

  try {
    const snapshotFilePath = buildSnapshotFilePath(timestampISO);
    await writeJsonFile(snapshotFilePath, payload);
    await writeJsonFile(LATEST_PERFORMANCE_FILE, payload);
    return {
      persisted: true,
      latestFile: LATEST_PERFORMANCE_FILE,
      snapshotFile: snapshotFilePath,
    };
  } catch (error) {
    return {
      persisted: false,
      error: error.message,
    };
  }
}

async function readLatestPerformanceSnapshot() {
  return readJsonFile(LATEST_PERFORMANCE_FILE, null);
}

async function writeAlertsSnapshot(alertPayload) {
  const timestampISO = alertPayload.generatedAt || new Date().toISOString();
  const payload = {
    ...alertPayload,
    generatedAt: timestampISO,
  };

  try {
    const snapshotFile = path.join(
      DASHBOARD_DATA_DIR,
      `alerts-${timestampISO.replace(/[:.]/g, "-")}.json`
    );
    await writeJsonFile(snapshotFile, payload);
    await writeJsonFile(LATEST_ALERTS_FILE, payload);
    return { persisted: true, latestFile: LATEST_ALERTS_FILE, snapshotFile };
  } catch (error) {
    return { persisted: false, error: error.message };
  }
}

async function readLatestAlertsSnapshot() {
  return readJsonFile(LATEST_ALERTS_FILE, null);
}

module.exports = {
  DASHBOARD_DATA_DIR,
  readLatestPerformanceSnapshot,
  writePerformanceSnapshot,
  readLatestAlertsSnapshot,
  writeAlertsSnapshot,
};
