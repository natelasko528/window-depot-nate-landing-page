const GRAPH_BASE = 'https://graph.facebook.com/v21.0';

function isMetaConfigured() {
  return !!(process.env.META_PAGE_TOKEN && process.env.META_PAGE_ID);
}

function hasInstagram() {
  return !!process.env.META_IG_USER_ID;
}

async function graphFetch(path, token) {
  const sep = path.includes('?') ? '&' : '?';
  const url = `${GRAPH_BASE}${path}${sep}access_token=${token}`;
  const resp = await fetch(url);
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(`Meta API ${resp.status}: ${err.error?.message || resp.statusText}`);
  }
  return resp.json();
}

async function fetchFBPagePosts(pageId, token, limit = 100) {
  const fields = [
    'id', 'message', 'created_time', 'full_picture', 'permalink_url',
    'shares', 'likes.summary(true).limit(0)', 'comments.summary(true).limit(0)',
    'insights.metric(post_impressions,post_impressions_unique,post_engaged_users,post_clicks){values}',
  ].join(',');

  const posts = [];
  let url = `/${pageId}/published_posts?fields=${fields}&limit=${Math.min(limit, 100)}`;

  while (url && posts.length < limit) {
    const data = await graphFetch(url, token);
    if (data.data) posts.push(...data.data);
    const nextUrl = data.paging?.next;
    if (nextUrl && posts.length < limit) {
      url = nextUrl.replace(GRAPH_BASE, '').replace(`access_token=${token}`, '').replace('&&', '&');
    } else {
      break;
    }
  }

  return posts.map(normalizeFBPost);
}

function normalizeFBPost(raw) {
  const insights = {};
  if (raw.insights?.data) {
    for (const metric of raw.insights.data) {
      const val = metric.values?.[0]?.value ?? 0;
      insights[metric.name] = val;
    }
  }

  return {
    id: raw.id,
    platform: 'facebook',
    caption: raw.message || '',
    imageUrl: raw.full_picture || null,
    permalink: raw.permalink_url || null,
    publishedAt: raw.created_time,
    status: 'published',
    metrics: {
      impressions: insights.post_impressions || 0,
      reach: insights.post_impressions_unique || 0,
      engagements: insights.post_engaged_users || 0,
      clicks: insights.post_clicks || 0,
      likes: raw.likes?.summary?.total_count || 0,
      comments: raw.comments?.summary?.total_count || 0,
      shares: raw.shares?.count || 0,
      saves: 0,
    },
  };
}

async function fetchIGMedia(igUserId, token, limit = 100) {
  const fields = [
    'id', 'caption', 'media_url', 'thumbnail_url', 'permalink',
    'timestamp', 'media_type', 'like_count', 'comments_count',
    'insights.metric(reach,engagement,saved){values}',
  ].join(',');

  const media = [];
  let url = `/${igUserId}/media?fields=${fields}&limit=${Math.min(limit, 100)}`;

  while (url && media.length < limit) {
    const data = await graphFetch(url, token);
    if (data.data) media.push(...data.data);
    const nextUrl = data.paging?.next;
    if (nextUrl && media.length < limit) {
      url = nextUrl.replace(GRAPH_BASE, '').replace(`access_token=${token}`, '').replace('&&', '&');
    } else {
      break;
    }
  }

  return media.map(normalizeIGMedia);
}

function normalizeIGMedia(raw) {
  const insights = {};
  if (raw.insights?.data) {
    for (const metric of raw.insights.data) {
      const val = metric.values?.[0]?.value ?? 0;
      insights[metric.name] = val;
    }
  }

  return {
    id: raw.id,
    platform: 'instagram',
    caption: raw.caption || '',
    imageUrl: raw.media_url || raw.thumbnail_url || null,
    permalink: raw.permalink || null,
    publishedAt: raw.timestamp,
    status: 'published',
    mediaType: raw.media_type,
    metrics: {
      impressions: 0,
      reach: insights.reach || 0,
      engagements: insights.engagement || 0,
      clicks: 0,
      likes: raw.like_count || 0,
      comments: raw.comments_count || 0,
      shares: 0,
      saves: insights.saved || 0,
    },
  };
}

async function fetchAllMetaPosts() {
  const token = process.env.META_PAGE_TOKEN;
  const pageId = process.env.META_PAGE_ID;
  const igUserId = process.env.META_IG_USER_ID;

  const posts = [];

  if (pageId && token) {
    try {
      const fbPosts = await fetchFBPagePosts(pageId, token);
      posts.push(...fbPosts);
    } catch (err) {
      console.error('FB posts fetch error:', err.message);
    }
  }

  if (igUserId && token) {
    try {
      const igPosts = await fetchIGMedia(igUserId, token);
      posts.push(...igPosts);
    } catch (err) {
      console.error('IG media fetch error:', err.message);
    }
  }

  return posts;
}

module.exports = { isMetaConfigured, hasInstagram, fetchAllMetaPosts, fetchFBPagePosts, fetchIGMedia };
