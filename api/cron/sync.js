const { fetchGHLPosts, isGHLConfigured } = require('../_lib/ghl');

module.exports = async (req, res) => {
  const cronSecret = process.env.CRON_SECRET;
  if (cronSecret && req.headers['authorization'] !== `Bearer ${cronSecret}`) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (!isGHLConfigured()) {
    return res.status(200).json({ ok: true, message: 'GHL not configured — skipping sync', synced: 0 });
  }

  try {
    const posts = await fetchGHLPosts(process.env.GHL_LOCATION_ID, process.env.GHL_API_KEY);
    console.log(`[CRON] Synced ${posts.length} posts from GHL at ${new Date().toISOString()}`);
    res.status(200).json({ ok: true, synced: posts.length, timestamp: new Date().toISOString() });
  } catch (err) {
    console.error('[CRON] Sync failed:', err.message);
    res.status(500).json({ error: 'Sync failed', message: err.message });
  }
};
