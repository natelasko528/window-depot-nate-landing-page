const THEMES = [
  'Windows - Winter Energy', 'Windows - Twilight Curb Appeal', 'Windows - Spring Fresh',
  'Windows - Comfort Interior', 'Windows - Before/After', 'Doors - Entry Upgrade',
  'Doors - Patio Living', 'Doors - Security', 'Doors - Curb Appeal', 'Doors - Spring',
  'Siding - Transformation', 'Siding - Weather Protection', 'Siding - Color Options',
  'Siding - Durability', 'Siding - Modern Look', 'Roofing - Storm Ready',
  'Roofing - Metal Premium', 'Roofing - Warranty', 'Roofing - Before/After',
  'Roofing - Seasonal', 'Bathroom - 1 Day Install', 'Bathroom - Spa Luxury',
  'Bathroom - Accessibility', 'Bathroom - Walk-In Shower', 'Bathroom - Tub to Shower',
  'Whole Home - Full Remodel', 'Whole Home - Energy Audit', 'Whole Home - Showroom Tour',
  'Whole Home - Customer Story', 'Whole Home - Spring Package',
];

const PLATFORMS = ['facebook', 'instagram', 'linkedin'];

function seededRandom(seed) {
  let s = seed;
  return function() {
    s = (s * 1103515245 + 12345) & 0x7fffffff;
    return s / 0x7fffffff;
  };
}

function generateDemoData() {
  const rng = seededRandom(42);
  const posts = [];
  const now = Date.now();
  const dayMs = 86400000;

  for (let p = 0; p < PLATFORMS.length; p++) {
    for (let i = 0; i < 30; i++) {
      const postNum = i + 1;
      const daysAgo = Math.floor(30 - (i * 0.9) + rng() * 3);
      const pubDate = new Date(now - daysAgo * dayMs);
      const schedDate = new Date(pubDate.getTime() - 3600000);

      const baseReach = 400 + Math.floor(rng() * 2600);
      const engagementRate = 0.02 + rng() * 0.08;
      const baseEng = Math.floor(baseReach * engagementRate);
      const likes = Math.floor(baseEng * (0.4 + rng() * 0.3));
      const comments = Math.floor(baseEng * (0.08 + rng() * 0.15));
      const shares = Math.floor(baseEng * (0.05 + rng() * 0.12));
      const saves = PLATFORMS[p] === 'instagram' ? Math.floor(baseEng * (0.03 + rng() * 0.08)) : 0;
      const clicks = Math.floor(baseReach * (0.01 + rng() * 0.04));

      const platformMultiplier = PLATFORMS[p] === 'instagram' ? 1.2 : PLATFORMS[p] === 'facebook' ? 1.0 : 0.85;

      posts.push({
        id: `demo_${PLATFORMS[p]}_${String(postNum).padStart(2, '0')}`,
        postNumber: postNum,
        platform: PLATFORMS[p],
        theme: THEMES[i % THEMES.length],
        status: daysAgo > 0 ? 'published' : 'scheduled',
        caption: getDemoCaption(THEMES[i % THEMES.length]),
        scheduledAt: schedDate.toISOString(),
        publishedAt: daysAgo > 0 ? pubDate.toISOString() : null,
        imageUrl: null,
        metrics: {
          impressions: Math.floor(baseReach * (1.3 + rng() * 0.5) * platformMultiplier),
          reach: Math.floor(baseReach * platformMultiplier),
          engagements: Math.floor(baseEng * platformMultiplier),
          likes: Math.floor(likes * platformMultiplier),
          comments: Math.floor(comments * platformMultiplier),
          shares: Math.floor(shares * platformMultiplier),
          saves: Math.floor(saves * platformMultiplier),
          clicks: Math.floor(clicks * platformMultiplier),
        },
      });
    }
  }

  return posts;
}

function getDemoCaption(theme) {
  const captions = {
    'Windows': 'Wisconsin winters hit hard — and your old windows are letting heat escape. Triple-pane at dual-pane prices.',
    'Doors': 'First impressions start at the front door. ProVia fiberglass entry doors — beautiful, secure, energy efficient.',
    'Siding': 'Transform your home\'s exterior. CraneBoard and ASCEND composite cladding — built for Wisconsin weather.',
    'Roofing': 'Your roof protects everything underneath it. NorthGate shingles + ProVia metal roofing options.',
    'Bathroom': 'Spa-luxury bathroom remodel installed in just 1 day. Bath Makeover acrylic systems.',
    'Whole Home': 'Your home deserves the full treatment. Windows, doors, siding, roofing — all from one trusted team.',
  };
  const key = Object.keys(captions).find(k => theme.startsWith(k)) || 'Windows';
  return captions[key];
}

function generateDemoTimeSeries(posts) {
  const dayMs = 86400000;
  const now = Date.now();
  const days = 30;
  const series = [];

  for (let d = days; d >= 0; d--) {
    const date = new Date(now - d * dayMs);
    const dateStr = date.toISOString().split('T')[0];
    const entry = { date: dateStr, facebook: 0, instagram: 0, linkedin: 0, total: 0 };

    posts.forEach(post => {
      if (!post.publishedAt) return;
      const pubDate = new Date(post.publishedAt);
      const daysSincePub = Math.floor((date.getTime() - pubDate.getTime()) / dayMs);
      if (daysSincePub >= 0 && daysSincePub < 7) {
        const dailyEng = Math.floor(post.metrics.engagements * (0.4 * Math.exp(-0.5 * daysSincePub)));
        entry[post.platform] += dailyEng;
        entry.total += dailyEng;
      }
    });

    series.push(entry);
  }

  return series;
}

module.exports = { generateDemoData, generateDemoTimeSeries };
