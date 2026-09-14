export interface McpEnv {
  OPENAPI_JSON?: string;
  MCP_API_BASE?: string;
  MCP_ALLOWED_HOSTS?: string;
  MCP_ALLOWED_ORIGINS?: string;
  MCP_TIMEOUT_MS?: string;
  MCP_MAX_RESPONSE_BYTES?: string;
}

export interface Env extends McpEnv {
  ORIGIN_BASE: string;
  INDEX_URL: string;
  TAGS_URL: string;
  SITE_BASE: string;
}
