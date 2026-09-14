import { handleMcp } from "./src/mcp";
import type { McpEnv } from "./src/env";

export default {
  fetch(request: Request, env: McpEnv, ctx: ExecutionContext) {
    return handleMcp(request, env, ctx);
  },
} satisfies ExportedHandler<McpEnv>;
