"""Tool implementations for PS-Wiki MCP server."""

from typing import Any
from .api_client import APIClient


async def search_terms_tool(client: APIClient, args: dict[str, Any]) -> dict[str, Any]:
    """Search for terms.

    Args:
        client: API client instance
        args: Tool arguments with 'query' and optional 'limit'

    Returns:
        Dictionary with search results
    """
    query = args.get("query", "")
    limit = args.get("limit", 10)

    terms = await client.search_terms(query=query, limit=limit)

    return {
        "query": query,
        "count": len(terms),
        "results": [
            {
                "id": term.id,
                "title": term.title,
                "summary": term.summary,
                "tags": term.tags,
                "updated_at": term.updated_at,
            }
            for term in terms
        ],
    }


async def get_term_tool(client: APIClient, args: dict[str, Any]) -> dict[str, Any]:
    """Get full term details.

    Args:
        client: API client instance
        args: Tool arguments with 'term_id'

    Returns:
        Full term data
    """
    term_id = args.get("term_id", "")
    if not term_id:
        raise ValueError("term_id is required")

    term = await client.get_term(term_id)
    return term


async def get_related_terms_tool(client: APIClient, args: dict[str, Any]) -> dict[str, Any]:
    """Get related terms.

    Args:
        client: API client instance
        args: Tool arguments with 'term_id' and optional 'depth'

    Returns:
        Dictionary with related terms
    """
    term_id = args.get("term_id", "")
    depth = args.get("depth", 1)

    if not term_id:
        raise ValueError("term_id is required")

    # Get the main term
    term = await client.get_term(term_id)
    related_ids = term.get("related", [])

    # Fetch related terms
    related_terms = []
    for rel_id in related_ids:
        try:
            rel_term = await client.get_term(rel_id)
            related_terms.append(
                {
                    "id": rel_term.get("id"),
                    "title": rel_term.get("title"),
                    "summary": rel_term.get("description", ""),
                }
            )
        except Exception:
            # Skip if term not found
            continue

    result = {
        "term_id": term_id,
        "term_title": term.get("title"),
        "depth": 1,
        "related_terms": related_terms,
    }

    # If depth=2, fetch second-level relations
    if depth >= 2:
        second_level = []
        for rel_term in related_terms:
            try:
                rel_full = await client.get_term(rel_term["id"])
                for second_id in rel_full.get("related", []):
                    if second_id != term_id and second_id not in related_ids:
                        try:
                            second_term = await client.get_term(second_id)
                            second_level.append(
                                {
                                    "id": second_term.get("id"),
                                    "title": second_term.get("title"),
                                    "via": rel_term["id"],
                                }
                            )
                        except Exception:
                            continue
            except Exception:
                continue

        result["depth"] = 2
        result["second_level_terms"] = second_level

    return result


async def list_tags_tool(client: APIClient, args: dict[str, Any]) -> dict[str, Any]:
    """List all tags.

    Args:
        client: API client instance
        args: Tool arguments (none required)

    Returns:
        Dictionary with tags and counts
    """
    tags = await client.list_tags()
    return {"tags": tags, "count": len(tags)}


async def get_terms_by_tag_tool(client: APIClient, args: dict[str, Any]) -> dict[str, Any]:
    """Get terms by tag.

    Args:
        client: API client instance
        args: Tool arguments with 'tag'

    Returns:
        Dictionary with terms matching the tag
    """
    tag = args.get("tag", "")
    if not tag:
        raise ValueError("tag is required")

    terms = await client.search_terms(tag=tag, limit=100)

    return {
        "tag": tag,
        "count": len(terms),
        "terms": [
            {
                "id": term.id,
                "title": term.title,
                "summary": term.summary,
                "updated_at": term.updated_at,
            }
            for term in terms
        ],
    }
