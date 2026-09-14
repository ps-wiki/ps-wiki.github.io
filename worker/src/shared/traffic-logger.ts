/**
 * Traffic Logger — Drop-in module for writing request logs to R2.
 *
 * Works on the Workers Free plan. No Logpush or Tail Worker required.
 * Each request writes one JSON object to your R2 bucket via an R2 binding.
 *
 * Usage in your Worker:
 *
 *   import { logTraffic } from "./traffic-logger";
 *
 *   export default {
 *     async fetch(request, env, ctx) {
 *       return logTraffic("rest-api", env, ctx, async () => {
 *         // ...your existing handler logic...
 *         return new Response("hello");
 *       });
 *     },
 *   };
 *
 * R2 binding required in wrangler.jsonc:
 *
 *   "r2_buckets": [
 *     { "binding": "TRAFFIC_LOGS", "bucket_name": "<your-bucket-name>" }
 *   ]
 */

export interface TrafficLogEntry {
  timestamp: string;
  worker: string;
  method: string;
  url: string;
  pathname: string;
  status: number;
  durationMs: number;
  requestId: string;
  cf?: {
    colo?: string;
    country?: string;
    asn?: number;
  };
  error?: string;
}

/**
 * Wraps a request handler and logs traffic to R2.
 *
 * @param workerName  - Identifier for this Worker (e.g. "rest-api", "mcp-server")
 * @param env         - Worker env (must contain TRAFFIC_LOGS R2 binding)
 * @param ctx         - ExecutionContext (for waitUntil)
 * @param handler     - Your actual request handler
 * @returns           - The response from your handler
 */
export function logTraffic(
  workerName: string,
  env: { TRAFFIC_LOGS: R2Bucket },
  ctx: { waitUntil: (p: Promise<unknown>) => void },
  handler: () => Promise<Response>,
): Promise<Response> {
  return logTrafficWithRequest(workerName, env, ctx, null, handler);
}

/**
 * Full version — pass the original Request if you want cf metadata captured.
 */
export function logTrafficWithRequest(
  workerName: string,
  env: { TRAFFIC_LOGS: R2Bucket },
  ctx: { waitUntil: (p: Promise<unknown>) => void },
  request: Request | null,
  handler: () => Promise<Response>,
): Promise<Response> {
  const start = Date.now();
  const requestId = crypto.randomUUID();
  const timestamp = new Date().toISOString();

  // Run the handler first, then log — logging is fire-and-forget
  return handler().then(
    (response) => {
      writeLogEntry(
        env, ctx, workerName, request, response.status, start,
        requestId, timestamp, undefined,
      );
      return response;
    },
    (error) => {
      writeLogEntry(
        env, ctx, workerName, request, 500, start,
        requestId, timestamp, String(error),
      );
      throw error;
    },
  );
}

function writeLogEntry(
  env: { TRAFFIC_LOGS: R2Bucket },
  ctx: { waitUntil: (p: Promise<unknown>) => void },
  workerName: string,
  request: Request | null,
  status: number,
  startMs: number,
  requestId: string,
  timestamp: string,
  error: string | undefined,
): void {
  const durationMs = Date.now() - startMs;

  const entry: TrafficLogEntry = {
    timestamp,
    worker: workerName,
    method: request?.method ?? "UNKNOWN",
    url: request?.url ?? "",
    pathname: request ? new URL(request.url).pathname : "",
    status,
    durationMs,
    requestId,
  };

  // Capture Cloudflare cf metadata if available
  const cf = (request as any)?.cf as Record<string, unknown> | undefined;
  if (cf) {
    entry.cf = {
      colo: cf.colo as string | undefined,
      country: cf.country as string | undefined,
      asn: cf.asn as number | undefined,
    };
  }

  if (error) {
    entry.error = error;
  }

  // R2 key format: <worker>/<YYYY-MM-DD>/<requestId>.json
  const datePart = timestamp.slice(0, 10); // YYYY-MM-DD
  const key = `${workerName}/${datePart}/${requestId}.json`;

  // Fire-and-forget — don't block the response
  ctx.waitUntil(
    env.TRAFFIC_LOGS.put(key, JSON.stringify(entry), {
      httpMetadata: { contentType: "application/json" },
    }),
  );
}
