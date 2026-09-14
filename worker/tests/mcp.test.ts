import { beforeEach, describe, expect, it, vi } from "vitest";

import worker from "../mcp-entry";
import type { McpEnv } from "../src/env";

const env: McpEnv = {
  TRAFFIC_LOGS: { put: vi.fn(async () => undefined) } as unknown as R2Bucket,
  MCP_API_BASE: "https://api.ps-wiki.ning.guru",
  MCP_ALLOWED_HOSTS: "mcp.ps-wiki.ning.guru",
  MCP_ALLOWED_ORIGINS: "mcp.ps-wiki.ning.guru",
  MCP_TIMEOUT_MS: "20",
  MCP_MAX_RESPONSE_BYTES: "100000",
};

const context = {
  waitUntil: vi.fn(),
  passThroughOnException: vi.fn(),
} as unknown as ExecutionContext;

type McpReply = {
  result?: {
    serverInfo?: { name?: string };
    tools?: Array<{
      name: string;
      annotations?: {
        title?: string;
        readOnlyHint?: boolean;
        openWorldHint?: boolean;
        destructiveHint?: boolean;
        idempotentHint?: boolean;
      };
    }>;
    isError?: boolean;
    content?: Array<{ text: string }>;
  };
  error?: { code: number };
};

function apiResponse(body: unknown, status = 200, headers: Record<string, string> = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...headers },
  });
}

function initializeRequest(id = 1) {
  return {
    jsonrpc: "2.0",
    id,
    method: "initialize",
    params: {
      protocolVersion: "2025-06-18",
      capabilities: {},
      clientInfo: { name: "pswiki-test", version: "1.0.0" },
    },
  };
}

async function mcpRequest(body: unknown, origin?: string, requestEnv: McpEnv = env) {
  const response = await worker.fetch(
    new Request("https://mcp.ps-wiki.ning.guru/mcp", {
      method: "POST",
      headers: {
        Accept: "application/json, text/event-stream",
        "Content-Type": "application/json",
        Host: "mcp.ps-wiki.ning.guru",
        ...(origin ? { Origin: origin } : {}),
      },
      body: JSON.stringify(body),
    }),
    requestEnv,
    context,
  );
  const text = await response.text();
  const payload = response.headers.get("Content-Type")?.includes("text/event-stream")
    ? text
        .split("\n")
        .find((line) => line.startsWith("data: "))
        ?.slice("data: ".length) ?? "null"
    : text;
  return {
    response,
    body: response.status === 204 ? null : JSON.parse(payload) as McpReply,
  };
}

describe("remote MCP Worker", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL) => {
        const url = String(input);
        if (url.endsWith("/v1/terms?query=stability&limit=10")) {
          return apiResponse({
            items: [
              {
                id: "voltage-stability",
                title: "Voltage Stability",
                summary: "Ability to maintain acceptable bus voltages.",
                tags: ["stability"],
                updated_at: "2026-09-01",
                url: "https://ps-wiki.ning.guru/wiki/voltage-stability/",
              },
            ],
            next_cursor: null,
            attribution: { provider: "PS-Wiki" },
          });
        }
        if (url.endsWith("/v1/terms/voltage-stability")) {
          return apiResponse({
            id: "voltage-stability",
            title: "Voltage Stability",
            description: "The ability of a power system to maintain steady voltages.",
            related: ["loadability"],
            url: "https://ps-wiki.ning.guru/wiki/voltage-stability/",
            attribution: { provider: "PS-Wiki" },
          });
        }
        if (url.endsWith("/v1/terms/missing-term")) return apiResponse({ error: "not_found" }, 404);
        if (url.endsWith("/v1/tags")) {
          return apiResponse({ tags: [{ tag: "stability", count: 12 }], attribution: { provider: "PS-Wiki" } });
        }
        throw new Error(`Unexpected upstream URL: ${url}`);
      }),
    );
  });

  it("initializes and lists the five read-only tools", async () => {
    const initialized = await mcpRequest(initializeRequest());
    expect(initialized.response.status).toBe(200);
    expect(initialized.body!.result!.serverInfo!.name).toBe("pswiki-mcp");

    const listed = await mcpRequest({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} });
    expect(listed.response.status).toBe(200);
    expect(listed.body!.result!.tools!.map((tool) => tool.name)).toEqual([
      "search_terms",
      "get_term",
      "get_related_terms",
      "list_tags",
      "get_terms_by_tag",
    ]);
    expect(listed.body!.result!.tools!.map((tool) => tool.annotations)).toEqual([
      { title: "Search PS-Wiki terms", readOnlyHint: true, openWorldHint: false, destructiveHint: false, idempotentHint: true },
      { title: "Get a PS-Wiki term", readOnlyHint: true, openWorldHint: false, destructiveHint: false, idempotentHint: true },
      { title: "Get related PS-Wiki terms", readOnlyHint: true, openWorldHint: false, destructiveHint: false, idempotentHint: true },
      { title: "List PS-Wiki tags", readOnlyHint: true, openWorldHint: false, destructiveHint: false, idempotentHint: true },
      { title: "List PS-Wiki terms by tag", readOnlyHint: true, openWorldHint: false, destructiveHint: false, idempotentHint: true },
    ]);
  });

  it("calls search_terms through the REST API", async () => {
    const log = vi.spyOn(console, "log").mockImplementation(() => {});
    await mcpRequest(initializeRequest());
    const called = await mcpRequest({
      jsonrpc: "2.0",
      id: 3,
      method: "tools/call",
      params: { name: "search_terms", arguments: { query: "stability" } },
    });

    expect(called.response.status).toBe(200);
    expect(called.body!.result!.isError).toBeUndefined();
    expect(JSON.parse(called.body!.result!.content![0].text).results[0].id).toBe("voltage-stability");

    const telemetry = log.mock.calls
      .map(([value]) => value)
      .find((value): value is Record<string, unknown> =>
        typeof value === "object" && value !== null && (value as Record<string, unknown>).event === "mcp_tool",
      );
    expect(telemetry).toMatchObject({
      event: "mcp_tool",
      tool_name: "search_terms",
      upstream_status: 200,
      upstream_statuses: [200],
      error_class: "none",
    });
    expect(telemetry).toHaveProperty("latency_ms");
    expect(telemetry).not.toHaveProperty("query");
  });

  it("returns a protocol validation error for invalid arguments", async () => {
    const called = await mcpRequest({
      jsonrpc: "2.0",
      id: 4,
      method: "tools/call",
      params: { name: "get_term", arguments: {} },
    });

    expect(called.response.status).toBe(200);
    expect(called.body!.result!.isError).toBe(true);
    expect(called.body!.result!.content![0].text).toContain("Invalid arguments");
  });

  it("returns a safe error for an unknown term", async () => {
    const log = vi.spyOn(console, "log").mockImplementation(() => {});
    const called = await mcpRequest({
      jsonrpc: "2.0",
      id: 5,
      method: "tools/call",
      params: { name: "get_term", arguments: { term_id: "missing-term" } },
    });
    expect(called.body!.result!.isError).toBe(true);
    expect(JSON.parse(called.body!.result!.content![0].text)).toMatchObject({ error: "not_found" });

    const telemetry = log.mock.calls
      .map(([value]) => value)
      .find((value): value is Record<string, unknown> =>
        typeof value === "object" && value !== null && (value as Record<string, unknown>).event === "mcp_tool",
      );
    expect(telemetry).toMatchObject({
      event: "mcp_tool",
      tool_name: "get_term",
      upstream_status: 404,
      upstream_statuses: [404],
      error_class: "not_found",
    });
    expect(telemetry).not.toHaveProperty("term_id");
  });

  it("returns a safe error when the REST API times out", async () => {
    vi.mocked(fetch).mockImplementationOnce(() => new Promise<Response>(() => {}));
    const called = await mcpRequest({
      jsonrpc: "2.0",
      id: 6,
      method: "tools/call",
      params: { name: "list_tags", arguments: {} },
    });
    expect(called.body!.result!.isError).toBe(true);
    expect(JSON.parse(called.body!.result!.content![0].text)).toMatchObject({ error: "upstream_error" });
  });

  it("returns a safe error when the REST API response is too large", async () => {
    vi.mocked(fetch).mockImplementationOnce(async () =>
      apiResponse({ tags: ["x".repeat(100)] }),
    );
    const called = await mcpRequest(
      {
        jsonrpc: "2.0",
        id: 7,
        method: "tools/call",
        params: { name: "list_tags", arguments: {} },
      },
      undefined,
      { ...env, MCP_MAX_RESPONSE_BYTES: "32" },
    );
    expect(called.body!.result!.isError).toBe(true);
    expect(JSON.parse(called.body!.result!.content![0].text)).toMatchObject({ error: "upstream_error" });
  });

  it("rejects malformed MCP JSON and disallowed origins", async () => {
    const malformed = await worker.fetch(
      new Request("https://mcp.ps-wiki.ning.guru/mcp", {
        method: "POST",
        headers: { Accept: "application/json, text/event-stream", "Content-Type": "application/json", Host: "mcp.ps-wiki.ning.guru" },
        body: "not-json",
      }),
      env,
      context,
    );
    expect(malformed.status).toBe(400);

    const disallowed = await mcpRequest(initializeRequest(8), "https://evil.example");
    expect(disallowed.response.status).toBe(403);
  });
});
