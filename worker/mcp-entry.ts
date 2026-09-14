import { handleMcp } from "./src/mcp";
import { logTrafficWithRequest } from "./src/shared/traffic-logger";
import type { McpEnv } from "./src/env";

export default {
  fetch(request: Request, env: McpEnv, ctx: ExecutionContext) {
    return logTrafficWithRequest("mcp-server", env, ctx, request, async () => {
      return handleMcp(request, env, ctx);
    });
  },
} satisfies ExportedHandler<McpEnv>;
