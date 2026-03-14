# GoHighLevel API Reference — Social Planner

> Verified against the official OpenAPI spec at `github.com/GoHighLevel/highlevel-api-docs`
> and confirmed with live API calls on March 14, 2026.

---

## Authentication

All requests use **Bearer token** auth with a **Private Integration Token (PIT)**.

```
Authorization: Bearer pit-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX
Version: 2021-07-28
Content-Type: application/json
```

Token is generated in GHL → Settings → Private Integrations.

**Rate limit:** 100 requests per 10 seconds per resource.

---

## Env Vars (Cursor Cloud Agent Secrets)

| Secret Name | Value Format | Example |
|-------------|-------------|---------|
| `GHL_API_TOKEN` | `pit-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | Private Integration Token |
| `GHL_LOCATION_ID` | Alphanumeric string | `Rkjt05VeS56IUr5caLBD` |

---

## Endpoint 1: Get Accounts

Returns all connected social media accounts and groups for a location.

```
GET /social-media-posting/{locationId}/accounts
```

### Response (200)

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Fetched Accounts",
  "results": {
    "accounts": [
      {
        "id": "69338440ffbf8adc5de6ef3e_Rkjt05VeS56IUr5caLBD_999513493239724_page",
        "oauthId": "69338440ffbf8adc5de6ef3e",
        "profileId": "6976d1f211a9c01a61bd6f42",
        "name": "RevolutionAi",
        "platform": "facebook",
        "type": "page",
        "expire": "2024-03-11T19:29:59.785Z",
        "isExpired": false,
        "meta": {}
      }
    ],
    "groups": [
      {
        "id": "6284c43d519161e96cc09c13",
        "name": "RevolutionAi Marketing Group",
        "accountIds": ["account_id_1", "account_id_2"]
      }
    ]
  }
}
```

**Key fields:**
- `accounts[].id` — used in `posts/list` body `accounts` filter and in `accountIds` on each post
- `accounts[].profileId` — used in the `/statistics` endpoint's `profileIds` body
- `accounts[].platform` — one of: `google`, `facebook`, `instagram`, `linkedin`, `twitter`, `tiktok`, `youtube`
- `accounts[].name` — display name

### Nate's Connected Accounts (verified live)

| Platform | Name | Account ID | Profile ID |
|----------|------|-----------|-----------|
| facebook | RevolutionAi | `69338440…_999513493239724_page` | `6976d1f211a9c01a61bd6f42` |
| facebook | Happy Homes of Wisconsin | `69338440…_639452246138430_page` | `697db4bb50434332a0a0c76b` |
| facebook | Lasko Health Solutions | `69338440…_186917172600_page` | `697db4eecd609119536316ea` |
| facebook | Daily Motivation and Inspiration | `69338440…_235337363007052_page` | `6976d1cf287ff09169274459` |
| instagram | natelasko528 | `69338466…_17841428950943404` | `6933846d95529a7a63da72ad` |
| linkedin | Nate Lasko | `69338480…_ppTjrCc6FX_profile` | `696efc1c4904d28f212f3a76` |
| youtube | Nate Lasko | `696efc32…_UCxdoH7Ke0xFLfCsAgue7KtQ_profile` | `696efc35c715df2e5c3b5bd8` |

---

## Endpoint 2: List Posts

Retrieves posts with filtering and pagination.

```
POST /social-media-posting/{locationId}/posts/list
```

### Request Body (all values are strings)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `skip` | string | **Yes** | Pagination offset. `"0"` for first page |
| `limit` | string | **Yes** | Page size. Max `"100"` |
| `fromDate` | string | **Yes** | ISO 8601 start date |
| `toDate` | string | **Yes** | ISO 8601 end date |
| `includeUsers` | string | **Yes** | `"true"` or `"false"` |
| `type` | string | No | Filter: `all`, `published`, `scheduled`, `draft`, `failed`, `in_review`, `in_progress`, `deleted` |
| `accounts` | string | No | Comma-separated account IDs to filter |
| `postType` | string | No | `post`, `story`, `reel` |

### Response (201)

```json
{
  "success": true,
  "statusCode": 201,
  "message": "Fetched Posts",
  "results": {
    "posts": [
      {
        "_id": "69b47369b6586ba103dbc7d0",
        "platform": "google",
        "status": "scheduled",
        "summary": "Post caption text...",
        "media": [
          { "url": "https://assets.cdn.filesafe.space/...", "type": "image/png" }
        ],
        "accountIds": ["account_id_string"],
        "parentPostId": "uuid-grouping-multi-platform-posts",
        "scheduleDate": "2026-04-27T13:42:00.000Z",
        "publishedAt": null,
        "displayDate": "2026-04-27T13:42:00.000Z",
        "createdAt": "2026-03-13T20:28:25.428Z",
        "updatedAt": "2026-03-13T20:28:25.472Z",
        "locationId": "Rkjt05VeS56IUr5caLBD",
        "createdBy": "5x0U1s3UwojNVv9aK78P",
        "type": "post",
        "tags": [],
        "source": "composer",
        "channel": "public",
        "deleted": false,
        "error": null,
        "postApprovalDetails": { "approvalStatus": "not_required" }
      }
    ],
    "count": 428
  }
}
```

**Key fields:**
- `results.posts[]` — array of post objects
- `results.count` — total number of matching posts (for pagination)
- `_id` — unique post ID
- `platform` — `facebook`, `instagram`, `linkedin`, `google`, `youtube`, `tiktok`
- `status` — `published`, `scheduled`, `draft`, `failed`, `in_review`, `in_progress`, `deleted`
- `summary` — the post caption/text
- `media[]` — array of `{url, type}` objects
- `parentPostId` — groups multi-platform posts together (same content, different platforms)
- `scheduleDate` — when the post is/was scheduled
- `publishedAt` — when it was published (null if not yet)
- `accountIds[]` — which connected accounts this post was sent to

**Note:** The list endpoint does NOT return engagement metrics (likes, comments, etc.). Metrics come from the Statistics endpoint.

### Nate's Post Distribution (verified live, 428 total)

| Skip | Platforms | Statuses |
|------|-----------|----------|
| 0–99 | google: 90, facebook: 7, linkedin: 1, instagram: 2 | scheduled: 90, published: 10 |
| 100–199 | linkedin: 33, facebook: 34, instagram: 33 | published: 98, failed: 2 |
| 200–299 | instagram: 31, linkedin: 30, facebook: 38, youtube: 1 | published: 100 |
| 300–399 | linkedin: 26, facebook: 46, instagram: 26, youtube: 2 | published: 100 |
| 400–427 | facebook: 11, instagram: 7, linkedin: 9, youtube: 1 | published: 26, failed: 2 |

---

## Endpoint 3: Get Single Post

```
GET /social-media-posting/{locationId}/posts/{id}
```

### Response (200)

```json
{
  "success": true,
  "statusCode": 200,
  "message": "Fetched Post",
  "results": {
    "post": { /* same GetPostFormattedSchema as list */ }
  }
}
```

---

## Endpoint 4: Get Statistics

Aggregate analytics for connected accounts. Returns last 7 days with comparison to prior 7 days.

```
POST /social-media-posting/statistics?locationId={locationId}
```

**Important:** `locationId` goes as a **query parameter**, not in the body.

### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `profileIds` | string[] | **Yes** | Array of `profileId` values from the `/accounts` endpoint (min 1) |
| `platforms` | string[] | No | Filter: `facebook`, `instagram`, `linkedin`, `google`, `pinterest`, `youtube`, `tiktok` |

### Response (201)

```json
{
  "results": {
    "dayRange": ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"],
    "totals": {
      "posts": 9,
      "likes": 4,
      "followers": 2,
      "impressions": 304,
      "comments": 2
    },
    "postPerformance": {
      "posts": { "facebook": [0,1,2,...], "instagram": [1,0,1,...] },
      "impressions": [17, 21, 63, 68, 46, 64, 25],
      "likes": [2, 0, 0, 0, 0, 1, 1],
      "comments": [0, 0, 1, 0, 1, 0, 0]
    },
    "breakdowns": {
      "posts": {
        "total": 9,
        "totalChange": "-73.53",
        "platforms": {
          "instagram": { "value": 5, "change": "-66.67" },
          "facebook": { "value": 4, "change": "-78.95" }
        }
      },
      "impressions": {
        "total": 304,
        "totalChange": "-75.58",
        "platforms": {
          "instagram": { "value": 209, "change": "-80.67" },
          "facebook": { "value": 95, "change": "-42.07" }
        }
      },
      "reach": {
        "total": 85,
        "totalChange": "-86.64",
        "platforms": {
          "instagram": { "value": 73, "change": "-85.85" },
          "facebook": { "value": 12, "change": "-90.00" }
        }
      },
      "engagement": {
        "instagram": { "likes": 4, "comments": 2, "shares": 0, "change": "-75.00" },
        "facebook": { "likes": 0, "comments": 0, "shares": 0, "change": 0 }
      }
    },
    "platformTotals": {
      "impressions": {
        "facebook": { "total": 95, "series": [0,5,20,...] },
        "instagram": { "total": 209, "series": [17,16,43,...] }
      },
      "followers": { ... },
      "likes": { ... }
    },
    "demographics": {
      "gender": { "totals": { "male": {"total":0,"percentage":0}, "female": {...}, "unknown": {...} } },
      "age": { "totals": { "13-17": 0, "18-24": 0, "25-34": 0, "35-44": 0, "45-54": 0, "55-64": 0, "65+": 0 } }
    }
  },
  "message": "Analytics Built Successfully",
  "traceId": "uuid"
}
```

**Key fields:**
- `totals` — aggregate totals for the 7-day period
- `breakdowns.posts/impressions/reach` — per-platform breakdown with `total`, `totalChange` (% vs prior 7d), and `platforms.{name}.{value, change}`
- `breakdowns.engagement.{platform}` — likes, comments, shares per platform with change %
- `postPerformance` — daily arrays (7 values, matching `dayRange`) for impressions, likes, comments
- `platformTotals` — per-platform daily series for impressions, followers, likes
- `demographics` — gender and age breakdowns

---

## Workflow: Dashboard Live Data

1. **On load / sync:** Call `GET /accounts` → store `profileId` values and `id` values
2. **For post list:** Call `POST /posts/list` with pagination (100 per page) until all fetched
3. **For analytics:** Call `POST /statistics?locationId=X` with `profileIds` from step 1
4. **Map posts to platforms:** Use post `platform` field directly
5. **Map engagement to posts:** Statistics gives aggregate + daily series; individual post metrics are not available via API — only aggregate per-platform breakdowns
