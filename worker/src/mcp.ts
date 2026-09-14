import { createMcpHandler } from "agents/mcp/server";
import { McpServer } from "@modelcontextprotocol/server";
import { z } from "zod";

import type { McpEnv } from "./env";

const DEFAULT_API_BASE = "https://api.ps-wiki.ning.guru";
const DEFAULT_TIMEOUT_MS = 5_000;
const DEFAULT_MAX_RESPONSE_BYTES = 1_000_000;
const MAX_SEARCH_LIMIT = 50;
const MAX_RELATED_TERMS = 25;
const MAX_LOGGED_UPSTREAM_STATUSES = 100;

type ToolResult = {
  isError?: boolean;
  content: Array<{ type: "text"; text: string }>;
};

type ToolTelemetry = {
  toolName: string;
  startedAt: number;
  upstreamStatuses: number[];
  errorClasses: string[];
};

type TermSummary = {
  id: string;
  title: string;
  summary?: string;
  description?: string;
  tags?: string[];
  updated_at?: string;
  url?: string;
};

type ApiAttribution = {
  provider?: string;
  url?: string;
  license?: { name?: string; url?: string };
};

type ApiTermsResponse = {
  items?: TermSummary[];
  next_cursor?: string | null;
  attribution?: ApiAttribution;
};

class ApiError extends Error {
  constructor(
    readonly code: "not_found" | "upstream_error" | "invalid_response",
    readonly status?: number,
  ) {
    super(code);
  }
}

function parsePositiveInt(value: string | undefined, fallback: number, maximum: number): number {
  const parsed = Number.parseInt(value ?? "", 10);
  return Number.isFinite(parsed) && parsed > 0 ? Math.min(parsed, maximum) : fallback;
}

function splitHostnames(value: string | undefined, fallback: string[]): string[] {
  const hostnames = (value ?? "")
    .split(",")
    .map((hostname) => hostname.trim().toLowerCase())
    .filter(Boolean);
  return hostnames.length > 0 ? hostnames : fallback;
}

function jsonText(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function success(value: unknown): ToolResult {
  return { content: [{ type: "text" as const, text: jsonText(value) }] };
}

function failure(error: unknown): ToolResult {
  if (error instanceof ApiError) {
    return {
      isError: true,
      content: [
        {
          type: "text" as const,
          text: jsonText({
            error: error.code,
            ...(error.status ? { status: error.status } : {}),
            message: error.code === "not_found" ? "The requested PS-Wiki term was not found." : "The PS-Wiki REST API could not complete the request.",
          }),
        },
      ],
    };
  }

  return {
    isError: true,
    content: [{ type: "text" as const, text: jsonText({ error: "internal_error" }) }],
  };
}

function createToolTelemetry(toolName: string): ToolTelemetry {
  return { toolName, startedAt: Date.now(), upstreamStatuses: [], errorClasses: [] };
}

function recordUpstreamStatus(telemetry: ToolTelemetry | undefined, status: number): void {
  if (telemetry && telemetry.upstreamStatuses.length < MAX_LOGGED_UPSTREAM_STATUSES) {
    telemetry.upstreamStatuses.push(status);
  }
}

function errorClass(error: unknown): string {
  if (error instanceof ApiError) return error.code;
  if (error instanceof Error && error.name) return error.name;
  return "unknown";
}

function recordErrorClass(telemetry: ToolTelemetry, error: unknown): void {
  const className = errorClass(error);
  if (telemetry.errorClasses.length < MAX_LOGGED_UPSTREAM_STATUSES) {
    telemetry.errorClasses.push(className);
  }
}

function logToolTelemetry(telemetry: ToolTelemetry, error: unknown = undefined): void {
  const statuses = telemetry.upstreamStatuses;
  const errorClasses = telemetry.errorClasses;
  console.log({
    event: "mcp_tool",
    tool_name: telemetry.toolName,
    upstream_status: statuses.length === 1 ? statuses[0] : null,
    upstream_statuses: statuses,
    error_class: error === undefined ? (errorClasses.length > 0 ? "partial_failure" : "none") : errorClass(error),
    ...(errorClasses.length > 0 ? { error_classes: errorClasses } : {}),
    latency_ms: Math.max(0, Date.now() - telemetry.startedAt),
  });
}

async function withToolTelemetry(
  toolName: string,
  operation: (telemetry: ToolTelemetry) => Promise<ToolResult>,
): Promise<ToolResult> {
  const telemetry = createToolTelemetry(toolName);
  let failureReason: unknown;
  try {
    return await operation(telemetry);
  } catch (error) {
    failureReason = error;
    recordErrorClass(telemetry, error);
    return failure(error);
  } finally {
    logToolTelemetry(telemetry, failureReason);
  }
}

async function readJson(response: Response, maxBytes: number): Promise<unknown> {
  const contentLength = Number.parseInt(response.headers.get("Content-Length") ?? "", 10);
  if (Number.isFinite(contentLength) && contentLength > maxBytes) {
    throw new ApiError("upstream_error", 502);
  }

  if (!response.body) {
    return response.json();
  }

  const reader = response.body.getReader();
  const chunks: Uint8Array[] = [];
  let total = 0;

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      total += value.byteLength;
      if (total > maxBytes) throw new ApiError("upstream_error", 502);
      chunks.push(value);
    }
  } finally {
    reader.releaseLock();
  }

  const bytes = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    bytes.set(chunk, offset);
    offset += chunk.byteLength;
  }

  try {
    return JSON.parse(new TextDecoder().decode(bytes));
  } catch {
    throw new ApiError("invalid_response", 502);
  }
}

async function fetchJson(path: string, env: McpEnv, telemetry?: ToolTelemetry): Promise<unknown> {
  const base = (env.MCP_API_BASE ?? DEFAULT_API_BASE).replace(/\/+$/, "");
  const timeoutMs = parsePositiveInt(env.MCP_TIMEOUT_MS, DEFAULT_TIMEOUT_MS, 30_000);
  const maxBytes = parsePositiveInt(
    env.MCP_MAX_RESPONSE_BYTES,
    DEFAULT_MAX_RESPONSE_BYTES,
    5_000_000,
  );
  const controller = new AbortController();
  let timeout: ReturnType<typeof setTimeout> | undefined;

  try {
    let response: Response;
    try {
      const request = fetch(`${base}${path}`, {
        headers: { Accept: "application/json" },
        signal: controller.signal,
      });
      const deadline = new Promise<never>((_, reject) => {
        timeout = setTimeout(() => {
          controller.abort();
          reject(new ApiError("upstream_error", 502));
        }, timeoutMs);
      });
      response = await Promise.race([request, deadline]);
    } catch {
      throw new ApiError("upstream_error", 502);
    }

    recordUpstreamStatus(telemetry, response.status);
    if (response.status === 404) throw new ApiError("not_found", 404);
    if (!response.ok) throw new ApiError("upstream_error", 502);
    return await readJson(response, maxBytes);
  } finally {
    if (timeout) clearTimeout(timeout);
  }
}

function asRecord(value: unknown): Record<string, unknown> {
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new ApiError("invalid_response", 502);
  }
  return value as Record<string, unknown>;
}

function asTermsResponse(value: unknown): ApiTermsResponse {
  const record = asRecord(value);
  if (record.items !== undefined && !Array.isArray(record.items)) {
    throw new ApiError("invalid_response", 502);
  }
  return record as ApiTermsResponse;
}

async function searchTerms(
  env: McpEnv,
  query: string,
  limit: number,
  telemetry: ToolTelemetry,
): Promise<ApiTermsResponse> {
  const params = new URLSearchParams({ query, limit: String(limit) });
  return asTermsResponse(await fetchJson(`/v1/terms?${params}`, env, telemetry));
}

async function getTerm(
  env: McpEnv,
  termId: string,
  telemetry: ToolTelemetry,
): Promise<Record<string, unknown>> {
  return asRecord(await fetchJson(`/v1/terms/${encodeURIComponent(termId)}`, env, telemetry));
}

async function relatedTermSummaries(
  env: McpEnv,
  relatedIds: string[],
  telemetry: ToolTelemetry,
): Promise<Array<{ id: unknown; title: unknown; summary: unknown; url: unknown }>> {
  const results = await Promise.allSettled(
    relatedIds.slice(0, MAX_RELATED_TERMS).map(async (id) => {
      const term = await getTerm(env, id, telemetry);
      return {
        id: term.id ?? id,
        title: term.title,
        summary: term.description ?? term.summary ?? "",
        url: term.url,
      };
    }),
  );
  return results.flatMap((result) => {
    if (result.status === "rejected") recordErrorClass(telemetry, result.reason);
    return result.status === "fulfilled" ? [result.value] : [];
  });
}

function createServer(env: McpEnv): McpServer {
  const server = new McpServer({ name: "pswiki-mcp", version: "1.0.0" });

  server.registerTool(
    "search_terms",
    {
      description: "Search PS-Wiki terminology by keyword, phrase, or concept. Use this to discover candidate terms before requesting a complete definition.",
      annotations: {
        title: "Search PS-Wiki terms",
        readOnlyHint: true,
        openWorldHint: false,
        destructiveHint: false,
        idempotentHint: true,
      },
      inputSchema: {
        query: z.string().trim().min(1).max(200).describe("Keyword, phrase, or concept to search for."),
        limit: z.number().int().min(1).max(MAX_SEARCH_LIMIT).optional().default(10).describe("Maximum number of matching term summaries to return; defaults to 10."),
      },
    },
    async ({ query, limit }) =>
      withToolTelemetry("search_terms", async (telemetry) => {
        const data = await searchTerms(env, query, limit, telemetry);
        return success({ query, count: data.items?.length ?? 0, results: data.items ?? [], attribution: data.attribution });
      }),
  );

  server.registerTool(
    "get_term",
    {
      description: "Retrieve the complete PS-Wiki definition for one known term ID, including description, equations, citations, related terms, canonical URL, and attribution.",
      annotations: {
        title: "Get a PS-Wiki term",
        readOnlyHint: true,
        openWorldHint: false,
        destructiveHint: false,
        idempotentHint: true,
      },
      inputSchema: {
        term_id: z.string().trim().min(1).max(200).describe("Kebab-case PS-Wiki term ID, such as voltage-stability."),
      },
    },
    async ({ term_id }) =>
      withToolTelemetry("get_term", async (telemetry) => success(await getTerm(env, term_id, telemetry))),
  );

  server.registerTool(
    "get_related_terms",
    {
      description: "Explore concepts related to a known PS-Wiki term. Use depth 1 for direct relationships; depth 2 also includes a bounded set of second-level concepts.",
      annotations: {
        title: "Get related PS-Wiki terms",
        readOnlyHint: true,
        openWorldHint: false,
        destructiveHint: false,
        idempotentHint: true,
      },
      inputSchema: {
        term_id: z.string().trim().min(1).max(200).describe("Kebab-case PS-Wiki term ID."),
        depth: z.number().int().min(1).max(2).optional().default(1).describe("Relationship depth: 1 or 2; defaults to 1."),
      },
    },
    async ({ term_id, depth }) =>
      withToolTelemetry("get_related_terms", async (telemetry) => {
        const term = await getTerm(env, term_id, telemetry);
        const relatedIds = Array.isArray(term.related)
          ? term.related.filter((value): value is string => typeof value === "string")
          : [];
        const relatedTerms = await relatedTermSummaries(env, relatedIds, telemetry);
        const result: Record<string, unknown> = {
          term_id,
          term_title: term.title,
          depth,
          related_terms: relatedTerms,
          attribution: term.attribution,
        };

        if (depth >= 2) {
          const secondLevelIds = new Set<string>();
          const relatedFull = await Promise.allSettled(
            relatedTerms.map(async (related) => getTerm(env, String(related.id), telemetry)),
          );
          for (const related of relatedFull) {
            if (related.status !== "fulfilled") {
              recordErrorClass(telemetry, related.reason);
              continue;
            }
            if (!Array.isArray(related.value.related)) continue;
            for (const secondId of related.value.related) {
              if (typeof secondId === "string" && secondId !== term_id && !relatedIds.includes(secondId)) {
                secondLevelIds.add(secondId);
              }
            }
          }
          result.second_level_terms = await relatedTermSummaries(env, [...secondLevelIds], telemetry);
        }

        return success(result);
      }),
  );

  server.registerTool(
    "list_tags",
    {
      description: "List PS-Wiki categories/tags and their usage counts. Use this to browse the taxonomy before filtering terms by a tag.",
      annotations: {
        title: "List PS-Wiki tags",
        readOnlyHint: true,
        openWorldHint: false,
        destructiveHint: false,
        idempotentHint: true,
      },
      inputSchema: {},
    },
    async () =>
      withToolTelemetry("list_tags", async (telemetry) => {
        const data = asRecord(await fetchJson("/v1/tags", env, telemetry));
        const tags = Array.isArray(data.tags) ? data.tags : [];
        return success({ tags, count: tags.length, attribution: data.attribution });
      }),
  );

  server.registerTool(
    "get_terms_by_tag",
    {
      description: "Browse PS-Wiki terms in one category/tag. Use this when the user wants a taxonomy-based list rather than a free-text concept search.",
      annotations: {
        title: "List PS-Wiki terms by tag",
        readOnlyHint: true,
        openWorldHint: false,
        destructiveHint: false,
        idempotentHint: true,
      },
      inputSchema: {
        tag: z.string().trim().min(1).max(100).describe("Case-insensitive PS-Wiki tag, such as stability or control."),
      },
    },
    async ({ tag }) =>
      withToolTelemetry("get_terms_by_tag", async (telemetry) => {
        const params = new URLSearchParams({ tag, limit: "100" });
        const data = asTermsResponse(await fetchJson(`/v1/terms?${params}`, env, telemetry));
        return success({ tag, count: data.items?.length ?? 0, terms: data.items ?? [], attribution: data.attribution });
      }),
  );

  return server;
}

export async function handleMcp(request: Request, env: McpEnv, ctx: ExecutionContext): Promise<Response> {
  const handler = createMcpHandler(() => createServer(env), {
    route: "/mcp",
    allowedHostnames: splitHostnames(env.MCP_ALLOWED_HOSTS, [
      "mcp.ps-wiki.ning.guru",
      "pswiki-mcp.jinning.workers.dev",
      "localhost",
      "127.0.0.1",
      "[::1]",
    ]),
    allowedOriginHostnames: splitHostnames(env.MCP_ALLOWED_ORIGINS, [
      "mcp.ps-wiki.ning.guru",
      "pswiki-mcp.jinning.workers.dev",
      "localhost",
      "127.0.0.1",
      "[::1]",
    ]),
  });
  return handler(request, env, ctx);
}
