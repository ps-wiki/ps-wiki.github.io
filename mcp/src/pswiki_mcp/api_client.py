"""REST API client for PS-Wiki."""

import httpx
from typing import Any, Optional
from pydantic import BaseModel


class TermSummary(BaseModel):
    """Summary of a term from the API."""

    id: str
    title: str
    summary: str = ""
    tags: list[str] = []
    updated_at: str = ""


class APIClient:
    """Client for PS-Wiki REST API."""

    def __init__(self, base_url: str = "https://pswiki-api.jinninggm.workers.dev"):
        """Initialize API client.

        Args:
            base_url: Base URL for the API (default: production API)
        """
        self.base_url = base_url.rstrip("/")
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def search_terms(
        self, query: Optional[str] = None, tag: Optional[str] = None, limit: int = 20
    ) -> list[TermSummary]:
        """Search for terms.

        Args:
            query: Free-text search query
            tag: Filter by tag (case-insensitive)
            limit: Maximum number of results (1-100)

        Returns:
            List of term summaries

        Raises:
            httpx.HTTPError: If the API request fails
        """
        params: dict[str, Any] = {"limit": min(max(limit, 1), 100)}
        if query:
            params["query"] = query
        if tag:
            params["tag"] = tag

        response = await self.client.get(f"{self.base_url}/v1/terms", params=params)
        response.raise_for_status()

        data = response.json()
        return [TermSummary(**item) for item in data.get("items", [])]

    async def get_term(self, term_id: str) -> dict[str, Any]:
        """Get full term details by ID.

        Args:
            term_id: Term identifier (e.g., "voltage-stability")

        Returns:
            Full term data as dictionary

        Raises:
            httpx.HTTPError: If the API request fails or term not found
        """
        response = await self.client.get(f"{self.base_url}/v1/terms/{term_id}")
        response.raise_for_status()
        return response.json()

    async def list_tags(self) -> list[dict[str, Any]]:
        """List all tags with counts.

        Returns:
            List of {tag: str, count: int} dictionaries

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(f"{self.base_url}/v1/tags")
        response.raise_for_status()

        data = response.json()
        return data.get("tags", [])

    async def get_changes(self, since: str) -> list[dict[str, str]]:
        """Get terms updated since a timestamp.

        Args:
            since: ISO 8601 timestamp or date (YYYY-MM-DD)

        Returns:
            List of {id: str, updated_at: str} dictionaries

        Raises:
            httpx.HTTPError: If the API request fails
        """
        response = await self.client.get(f"{self.base_url}/v1/changes", params={"since": since})
        response.raise_for_status()

        data = response.json()
        return data.get("items", [])
