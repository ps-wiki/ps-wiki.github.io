import { describe, expect, it, vi } from "vitest";

import { logTrafficWithRequest } from "../src/shared/traffic-logger";

describe("traffic logger", () => {
  it("stores route metadata without query text and does not delay the response", async () => {
    const put = vi.fn(async () => undefined);
    const waitUntil = vi.fn();
    const response = await logTrafficWithRequest(
      "rest-api",
      { TRAFFIC_LOGS: { put } as unknown as R2Bucket },
      { waitUntil },
      new Request("https://api.ps-wiki.ning.guru/v1/terms?query=private-value&limit=5"),
      async () => new Response("ok", { status: 200 }),
    );

    expect(response.status).toBe(200);
    expect(waitUntil).toHaveBeenCalledOnce();
    expect(put).toHaveBeenCalledOnce();
    const [key, body] = put.mock.calls[0] as unknown as [string, string];
    expect(key).toMatch(/^rest-api\/\d{4}-\d{2}-\d{2}\/.+\.json$/);
    expect(JSON.parse(body)).toMatchObject({
      worker: "rest-api",
      method: "GET",
      url: "https://api.ps-wiki.ning.guru/v1/terms",
      pathname: "/v1/terms",
      status: 200,
    });
    expect(body).not.toContain("private-value");
  });
});
