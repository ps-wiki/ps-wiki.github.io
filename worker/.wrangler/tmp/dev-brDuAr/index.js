var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// src/index.ts
var CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization"
};
var src_default = {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { headers: CORS });
    const u = new URL(req.url);
    const p = u.pathname.replace(/\/+$/, "");
    try {
      if (p === "/" || p === "") return text("PS-Wiki API v1");
      if (p === "/openapi.json") return json(env.OPENAPI_JSON ?? DEFAULT_OPENAPI, 200);
      if (p === "/v1/terms") return listTerms(u, env);
      if (p.startsWith("/v1/terms/")) {
        const id = decodeURIComponent(p.split("/").pop() || "");
        return getTerm(id, env);
      }
      if (p === "/v1/tags") return passthrough(env.TAGS_URL);
      if (p === "/v1/changes") return changes(u, env);
      return json({ error: "not_found" }, 404);
    } catch (e) {
      return json({ error: "internal_error", message: String(e?.message ?? e) }, 500);
    }
  }
};
async function fetchJSON(url) {
  const r = await fetch(url, { headers: { "Accept": "application/json" }, cf: { cacheTtl: 300, cacheEverything: true } });
  if (!r.ok) throw new Error(`Fetch failed ${r.status} for ${url}`);
  return r.json();
}
__name(fetchJSON, "fetchJSON");
async function listTerms(u, env) {
  const q = (u.searchParams.get("query") || "").toLowerCase().trim();
  const tag = (u.searchParams.get("tag") || "").toLowerCase().trim();
  const limit = Math.max(1, Math.min(100, parseInt(u.searchParams.get("limit") || "20", 10)));
  const cursor = u.searchParams.get("cursor");
  const idx = await fetchJSON(env.INDEX_URL);
  let items = idx.items || [];
  if (q) {
    items = items.filter(
      (t) => t.title?.toLowerCase().includes(q) || t.summary?.toLowerCase().includes(q) || t.id?.toLowerCase().includes(q) || (t.tags || []).some((x) => x.toLowerCase().includes(q))
    );
  }
  if (tag) items = items.filter((t) => (t.tags || []).some((x) => x.toLowerCase() === tag));
  items = items.slice().sort((a, b) => (b.updated_at || "").localeCompare(a.updated_at || "") || a.title.localeCompare(b.title));
  let offset = 0;
  if (cursor) try {
    offset = JSON.parse(atob(cursor)).o || 0;
  } catch {
  }
  const page = items.slice(offset, offset + limit);
  const next_cursor = offset + limit < items.length ? btoa(JSON.stringify({ o: offset + limit })) : null;
  return json({ items: page, next_cursor });
}
__name(listTerms, "listTerms");
async function getTerm(id, env) {
  if (!id) return json({ error: "bad_request" }, 400);
  const url = `${env.ORIGIN_BASE}/${encodeURIComponent(id)}.json`;
  const r = await fetch(url, { headers: { "Accept": "application/json" }, cf: { cacheTtl: 300, cacheEverything: true } });
  if (r.status === 404) return json({ error: "not_found" }, 404);
  if (!r.ok) return json({ error: "upstream_error", status: r.status }, 502);
  const h = new Headers(r.headers);
  Object.entries(CORS).forEach(([k, v]) => h.set(k, v));
  h.set("Content-Type", "application/json");
  return new Response(r.body, { status: 200, headers: h });
}
__name(getTerm, "getTerm");
async function changes(u, env) {
  const since = u.searchParams.get("since");
  if (!since) return json({ error: "missing_since" }, 400);
  const idx = await fetchJSON(env.INDEX_URL);
  const items = (idx.items || []).filter((t) => t.updated_at && new Date(t.updated_at) >= new Date(since)).map((t) => ({ id: t.id, updated_at: t.updated_at })).sort((a, b) => b.updated_at.localeCompare(a.updated_at));
  return json({ items });
}
__name(changes, "changes");
async function passthrough(url) {
  const data = await fetchJSON(url);
  return json(data);
}
__name(passthrough, "passthrough");
function json(data, status = 200) {
  const h = new Headers({ ...CORS, "Content-Type": "application/json" });
  return new Response(typeof data === "string" ? data : JSON.stringify(data), { status, headers: h });
}
__name(json, "json");
function text(s, status = 200) {
  const h = new Headers({ ...CORS, "Content-Type": "text/plain; charset=utf-8" });
  return new Response(s + "\n", { status, headers: h });
}
__name(text, "text");
var DEFAULT_OPENAPI = JSON.stringify({
  openapi: "3.1.0",
  info: { title: "PS-Wiki API", version: "1.0.0", description: "Read-only access to PS-Wiki terms and tags." },
  servers: [{ url: "https://YOUR-WORKER.example/api" }],
  paths: {
    "/v1/terms": {
      get: {
        summary: "Search or list terms",
        parameters: [
          { in: "query", name: "query", schema: { type: "string" } },
          { in: "query", name: "tag", schema: { type: "string" } },
          { in: "query", name: "limit", schema: { type: "integer", minimum: 1, maximum: 100, default: 20 } },
          { in: "query", name: "cursor", schema: { type: "string" } }
        ],
        responses: { "200": { description: "OK" } }
      }
    },
    "/v1/terms/{id}": {
      get: {
        summary: "Get a term",
        parameters: [{ in: "path", name: "id", required: true, schema: { type: "string" } }],
        responses: { "200": { description: "OK" }, "404": { description: "Not found" } }
      }
    },
    "/v1/tags": { get: { summary: "List tags", responses: { "200": { description: "OK" } } } },
    "/v1/changes": { get: { summary: "Changes since", parameters: [{ in: "query", name: "since", required: true, schema: { type: "string", format: "date-time" } }], responses: { "200": { description: "OK" } } } }
  }
});

// node_modules/wrangler/templates/middleware/middleware-ensure-req-body-drained.ts
var drainBody = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } finally {
    try {
      if (request.body !== null && !request.bodyUsed) {
        const reader = request.body.getReader();
        while (!(await reader.read()).done) {
        }
      }
    } catch (e) {
      console.error("Failed to drain the unused request body.", e);
    }
  }
}, "drainBody");
var middleware_ensure_req_body_drained_default = drainBody;

// node_modules/wrangler/templates/middleware/middleware-miniflare3-json-error.ts
function reduceError(e) {
  return {
    name: e?.name,
    message: e?.message ?? String(e),
    stack: e?.stack,
    cause: e?.cause === void 0 ? void 0 : reduceError(e.cause)
  };
}
__name(reduceError, "reduceError");
var jsonError = /* @__PURE__ */ __name(async (request, env, _ctx, middlewareCtx) => {
  try {
    return await middlewareCtx.next(request, env);
  } catch (e) {
    const error = reduceError(e);
    return Response.json(error, {
      status: 500,
      headers: { "MF-Experimental-Error-Stack": "true" }
    });
  }
}, "jsonError");
var middleware_miniflare3_json_error_default = jsonError;

// .wrangler/tmp/bundle-Pzdnl8/middleware-insertion-facade.js
var __INTERNAL_WRANGLER_MIDDLEWARE__ = [
  middleware_ensure_req_body_drained_default,
  middleware_miniflare3_json_error_default
];
var middleware_insertion_facade_default = src_default;

// node_modules/wrangler/templates/middleware/common.ts
var __facade_middleware__ = [];
function __facade_register__(...args) {
  __facade_middleware__.push(...args.flat());
}
__name(__facade_register__, "__facade_register__");
function __facade_invokeChain__(request, env, ctx, dispatch, middlewareChain) {
  const [head, ...tail] = middlewareChain;
  const middlewareCtx = {
    dispatch,
    next(newRequest, newEnv) {
      return __facade_invokeChain__(newRequest, newEnv, ctx, dispatch, tail);
    }
  };
  return head(request, env, ctx, middlewareCtx);
}
__name(__facade_invokeChain__, "__facade_invokeChain__");
function __facade_invoke__(request, env, ctx, dispatch, finalMiddleware) {
  return __facade_invokeChain__(request, env, ctx, dispatch, [
    ...__facade_middleware__,
    finalMiddleware
  ]);
}
__name(__facade_invoke__, "__facade_invoke__");

// .wrangler/tmp/bundle-Pzdnl8/middleware-loader.entry.ts
var __Facade_ScheduledController__ = class ___Facade_ScheduledController__ {
  constructor(scheduledTime, cron, noRetry) {
    this.scheduledTime = scheduledTime;
    this.cron = cron;
    this.#noRetry = noRetry;
  }
  static {
    __name(this, "__Facade_ScheduledController__");
  }
  #noRetry;
  noRetry() {
    if (!(this instanceof ___Facade_ScheduledController__)) {
      throw new TypeError("Illegal invocation");
    }
    this.#noRetry();
  }
};
function wrapExportedHandler(worker) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return worker;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  const fetchDispatcher = /* @__PURE__ */ __name(function(request, env, ctx) {
    if (worker.fetch === void 0) {
      throw new Error("Handler does not export a fetch() function.");
    }
    return worker.fetch(request, env, ctx);
  }, "fetchDispatcher");
  return {
    ...worker,
    fetch(request, env, ctx) {
      const dispatcher = /* @__PURE__ */ __name(function(type, init) {
        if (type === "scheduled" && worker.scheduled !== void 0) {
          const controller = new __Facade_ScheduledController__(
            Date.now(),
            init.cron ?? "",
            () => {
            }
          );
          return worker.scheduled(controller, env, ctx);
        }
      }, "dispatcher");
      return __facade_invoke__(request, env, ctx, dispatcher, fetchDispatcher);
    }
  };
}
__name(wrapExportedHandler, "wrapExportedHandler");
function wrapWorkerEntrypoint(klass) {
  if (__INTERNAL_WRANGLER_MIDDLEWARE__ === void 0 || __INTERNAL_WRANGLER_MIDDLEWARE__.length === 0) {
    return klass;
  }
  for (const middleware of __INTERNAL_WRANGLER_MIDDLEWARE__) {
    __facade_register__(middleware);
  }
  return class extends klass {
    #fetchDispatcher = /* @__PURE__ */ __name((request, env, ctx) => {
      this.env = env;
      this.ctx = ctx;
      if (super.fetch === void 0) {
        throw new Error("Entrypoint class does not define a fetch() function.");
      }
      return super.fetch(request);
    }, "#fetchDispatcher");
    #dispatcher = /* @__PURE__ */ __name((type, init) => {
      if (type === "scheduled" && super.scheduled !== void 0) {
        const controller = new __Facade_ScheduledController__(
          Date.now(),
          init.cron ?? "",
          () => {
          }
        );
        return super.scheduled(controller);
      }
    }, "#dispatcher");
    fetch(request) {
      return __facade_invoke__(
        request,
        this.env,
        this.ctx,
        this.#dispatcher,
        this.#fetchDispatcher
      );
    }
  };
}
__name(wrapWorkerEntrypoint, "wrapWorkerEntrypoint");
var WRAPPED_ENTRY;
if (typeof middleware_insertion_facade_default === "object") {
  WRAPPED_ENTRY = wrapExportedHandler(middleware_insertion_facade_default);
} else if (typeof middleware_insertion_facade_default === "function") {
  WRAPPED_ENTRY = wrapWorkerEntrypoint(middleware_insertion_facade_default);
}
var middleware_loader_entry_default = WRAPPED_ENTRY;
export {
  __INTERNAL_WRANGLER_MIDDLEWARE__,
  middleware_loader_entry_default as default
};
//# sourceMappingURL=index.js.map
