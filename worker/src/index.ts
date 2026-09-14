export interface Env {
  // Point these to your GitHub raw files in main branch.
  // If your JSONs live in ./pswiki/json -> append that path.
  ORIGIN_BASE: string; // e.g., https://raw.githubusercontent.com/ps-wiki/ps-wiki.github.io/main/pswiki/json
  INDEX_URL:   string; // e.g., https://raw.githubusercontent.com/ps-wiki/ps-wiki.github.io/main/pswiki/database/build/index.json
  TAGS_URL:    string; // e.g., https://raw.githubusercontent.com/ps-wiki/ps-wiki.github.io/main/pswiki/database/build/tags.json
  SITE_BASE:   string; // e.g., https://ps-wiki.ning.guru
  OPENAPI_JSON?: string; // optional; can inline or serve static later
}

type TermSummary = { id: string; title: string; summary?: string; tags?: string[]; updated_at: string };
type IndexDoc = { items: TermSummary[]; generated_at?: string };
type Attribution = {
  provider: string;
  url: string;
  license: { name: string; url: string };
};

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    console.log(JSON.stringify({
      method: req.method,
      path: new URL(req.url).pathname,
      country: req.cf?.country ?? "unknown",
      colo: req.cf?.colo ?? "unknown",
      userAgent: req.headers.get("User-Agent") ?? "",
      referer: req.headers.get("Referer") ?? "",
      accept: req.headers.get("Accept") ?? "",
      timestamp: new Date().toISOString(),
    }));
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });

    const u = new URL(req.url);
    const p = u.pathname.replace(/\/+$/, "");

    try {
      if (p === "/" || p === "") return text("PS-Wiki API v1");
      if (p === "/openapi.json")  return json(env.OPENAPI_JSON ?? DEFAULT_OPENAPI, 200);

      if (p === "/v1/terms")      return listTerms(u, env);
      if (p.startsWith("/v1/terms/")) {
        const id = decodeURIComponent(p.split("/").pop() || "");
        return getTerm(id, env);
      }
      if (p === "/v1/tags")       return listTags(env);
      if (p === "/v1/changes")    return changes(u, env);

      return json({ error: "not_found" }, 404);
    } catch (e: any) {
      return json({ error: "internal_error", message: String(e?.message ?? e) }, 500);
    }
  }
};

async function fetchJSON(url: string): Promise<any> {
  const r = await fetch(url, { headers: { "Accept": "application/json" }, cf: { cacheTtl: 300, cacheEverything: true } as any });
  if (!r.ok) throw new Error(`Fetch failed ${r.status} for ${url}`);
  return r.json();
}

async function listTerms(u: URL, env: Env): Promise<Response> {
  const q = (u.searchParams.get("query") || "").toLowerCase().trim();
  const tag = (u.searchParams.get("tag") || "").toLowerCase().trim();
  const limit = Math.max(1, Math.min(100, parseInt(u.searchParams.get("limit") || "20", 10)));
  const cursor = u.searchParams.get("cursor");

  const idx: IndexDoc = await fetchJSON(env.INDEX_URL);
  let items = idx.items || [];

  if (q) {
    items = items.filter(t =>
      (t.title?.toLowerCase().includes(q)) ||
      (t.summary?.toLowerCase().includes(q)) ||
      (t.id?.toLowerCase().includes(q)) ||
      (t.tags || []).some(x => x.toLowerCase().includes(q))
    );
  }
  if (tag) items = items.filter(t => (t.tags || []).some(x => x.toLowerCase() === tag));

  // order: updated desc then title
  items = items.slice().sort((a, b) => (b.updated_at || "").localeCompare(a.updated_at || "") || a.title.localeCompare(b.title));

  let offset = 0;
  if (cursor) try { offset = JSON.parse(atob(cursor)).o || 0; } catch {}
  const page = items.slice(offset, offset + limit);
  const next_cursor = offset + limit < items.length ? btoa(JSON.stringify({ o: offset + limit })) : null;

  return json({
    items: page.map((item) => ({ ...item, url: canonicalTermUrl(env.SITE_BASE, item.id) })),
    next_cursor,
    attribution: makeAttribution(env.SITE_BASE),
  });
}

async function getTerm(id: string, env: Env): Promise<Response> {
  if (!id) return json({ error: "bad_request" }, 400);
  const url = `${env.ORIGIN_BASE}/${encodeURIComponent(id)}.json`;
  const r = await fetch(url, { headers: { "Accept": "application/json" }, cf: { cacheTtl: 300, cacheEverything: true } as any });
  if (r.status === 404) return json({ error: "not_found" }, 404);
  if (!r.ok) return json({ error: "upstream_error", status: r.status }, 502);

  const data: unknown = await r.json();
  if (!isRecord(data)) return json({ error: "upstream_error", message: "Term payload is not an object" }, 502);

  const termUrl = canonicalTermUrl(env.SITE_BASE, id);
  return json(
    {
      ...data,
      url: termUrl,
      attribution: makeAttribution(env.SITE_BASE),
    },
    200,
    {
      "Cache-Control": r.headers.get("Cache-Control") ?? "public, max-age=300",
      Link: `<${termUrl}>; rel="canonical"`,
    },
  );
}

async function changes(u: URL, env: Env): Promise<Response> {
  const since = u.searchParams.get("since");
  if (!since) return json({ error: "missing_since" }, 400);

  const idx: IndexDoc = await fetchJSON(env.INDEX_URL);
  const items = (idx.items || [])
    .filter(t => t.updated_at && new Date(t.updated_at) >= new Date(since))
    .map(t => ({ id: t.id, updated_at: t.updated_at, url: canonicalTermUrl(env.SITE_BASE, t.id) }))
    .sort((a, b) => b.updated_at.localeCompare(a.updated_at));

  return json({ items, attribution: makeAttribution(env.SITE_BASE) });
}

async function listTags(env: Env): Promise<Response> {
  const data = await fetchJSON(env.TAGS_URL);
  if (!isRecord(data)) return json({ error: "upstream_error", message: "Tags payload is not an object" }, 502);
  return json({ ...data, attribution: makeAttribution(env.SITE_BASE) });
}

function canonicalTermUrl(siteBase: string, id: string): string {
  return `${siteBase.replace(/\/+$/, "")}/wiki/${encodeURIComponent(id)}/`;
}

function makeAttribution(siteBase: string): Attribution {
  return {
    provider: "PS-Wiki",
    url: `${siteBase.replace(/\/+$/, "")}/`,
    license: {
      name: "CC BY-NC 4.0",
      url: "https://creativecommons.org/licenses/by-nc/4.0/",
    },
  };
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function json(data: unknown, status = 200, extraHeaders: HeadersInit = {}): Response {
  const h = new Headers({ ...CORS, ...extraHeaders, "Content-Type": "application/json" });
  return new Response(typeof data === "string" ? data : JSON.stringify(data), { status, headers: h });
}
function text(s: string, status = 200): Response {
  const h = new Headers({ ...CORS, "Content-Type": "text/plain; charset=utf-8" });
  return new Response(s + "\n", { status, headers: h });
}

const DEFAULT_OPENAPI = JSON.stringify({
  openapi: "3.1.0",
  info: { title: "PS-Wiki API", version: "1.1.0", description: "Read-only access to PS-Wiki terms and tags with attribution metadata." },
  servers: [{ url: "https://api.ning.guru" }],
  paths: {
    "/v1/terms": {
      get: {
        summary: "Search or list terms",
        parameters: [
          { in: "query", name: "query", schema: { type: "string" } },
          { in: "query", name: "tag",   schema: { type: "string" } },
          { in: "query", name: "limit", schema: { type: "integer", minimum: 1, maximum: 100, default: 20 } },
          { in: "query", name: "cursor",schema: { type: "string" } }
        ],
        responses: {
          "200": {
            description: "OK",
            content: {
              "application/json": { schema: { $ref: "#/components/schemas/TermsResponse" } }
            }
          }
        }
      }
    },
    "/v1/terms/{id}": {
      get: {
        summary: "Get a term",
        parameters: [{ in: "path", name: "id", required: true, schema: { type: "string" } }],
        responses: {
          "200": {
            description: "OK",
            headers: { Link: { schema: { type: "string" }, description: "Canonical PS-Wiki term page" } },
            content: { "application/json": { schema: { $ref: "#/components/schemas/Term" } } }
          },
          "404": { description: "Not found" }
        }
      }
    },
    "/v1/tags": {
      get: {
        summary: "List tags",
        responses: { "200": { description: "OK", content: { "application/json": { schema: { $ref: "#/components/schemas/TagsResponse" } } } } }
      }
    },
    "/v1/changes": {
      get: {
        summary: "Changes since",
        parameters:[{in:"query",name:"since",required:true,schema:{type:"string",format:"date-time"}}],
        responses: { "200": { description: "OK", content: { "application/json": { schema: { $ref: "#/components/schemas/ChangesResponse" } } } } }
      }
    }
  },
  components: {
    schemas: {
      Attribution: {
        type: "object",
        required: ["provider", "url", "license"],
        properties: {
          provider: { type: "string", example: "PS-Wiki" },
          url: { type: "string", format: "uri" },
          license: {
            type: "object",
            required: ["name", "url"],
            properties: { name: { type: "string" }, url: { type: "string", format: "uri" } }
          }
        }
      },
      TermSummary: {
        type: "object",
        required: ["id", "title", "updated_at", "url"],
        properties: {
          id: { type: "string" }, title: { type: "string" }, summary: { type: "string" },
          tags: { type: "array", items: { type: "string" } }, updated_at: { type: "string" },
          url: { type: "string", format: "uri" }
        }
      },
      TermsResponse: {
        type: "object",
        required: ["items", "next_cursor", "attribution"],
        properties: {
          items: { type: "array", items: { $ref: "#/components/schemas/TermSummary" } },
          next_cursor: { type: ["string", "null"] },
          attribution: { $ref: "#/components/schemas/Attribution" }
        }
      },
      Term: {
        type: "object",
        required: ["url", "attribution"],
        properties: {
          url: { type: "string", format: "uri" },
          attribution: { $ref: "#/components/schemas/Attribution" }
        },
        additionalProperties: true
      },
      TagsResponse: {
        type: "object",
        required: ["tags", "attribution"],
        properties: { tags: { type: "array" }, attribution: { $ref: "#/components/schemas/Attribution" } }
      },
      ChangesResponse: {
        type: "object",
        required: ["items", "attribution"],
        properties: {
          items: { type: "array", items: { type: "object", required: ["id", "updated_at", "url"], properties: { id: { type: "string" }, updated_at: { type: "string" }, url: { type: "string", format: "uri" } } } },
          attribution: { $ref: "#/components/schemas/Attribution" }
        }
      }
    }
  }
});
