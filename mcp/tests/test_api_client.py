"""Deterministic tests for the PS-Wiki REST API client."""

import httpx
import pytest

from pswiki_mcp.api_client import APIClient, TermSummary


@pytest.fixture
async def client():
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/v1/terms" and request.url.params.get("query") == "stability":
            return httpx.Response(
                200,
                request=request,
                json={
                    "items": [
                        {
                            "id": "voltage-stability",
                            "title": "Voltage Stability",
                            "summary": "Maintaining acceptable voltages.",
                            "tags": ["stability"],
                            "updated_at": "2026-09-01",
                        }
                    ]
                },
            )
        if request.url.path == "/v1/terms" and request.url.params.get("tag") == "stability":
            return httpx.Response(
                200,
                request=request,
                json={
                    "items": [
                        {
                            "id": "voltage-stability",
                            "title": "Voltage Stability",
                            "tags": ["stability"],
                            "updated_at": "2026-09-01",
                        }
                    ]
                },
            )
        if request.url.path == "/v1/terms/voltage-stability":
            return httpx.Response(
                200,
                request=request,
                json={"id": "voltage-stability", "title": "Voltage Stability"},
            )
        if request.url.path == "/v1/terms/missing-term":
            return httpx.Response(404, request=request, json={"error": "not_found"})
        if request.url.path == "/v1/tags":
            return httpx.Response(
                200,
                request=request,
                json={"tags": [{"tag": "stability", "count": 12}]},
            )
        return httpx.Response(502, request=request, json={"error": "upstream_error"})

    transport = httpx.MockTransport(handler)
    http_client = httpx.AsyncClient(transport=transport)
    api_client = APIClient(client=http_client)
    yield api_client
    await http_client.aclose()


@pytest.mark.asyncio
async def test_search_terms(client):
    results = await client.search_terms(query="stability", limit=5)
    assert isinstance(results[0], TermSummary)
    assert results[0].id == "voltage-stability"


@pytest.mark.asyncio
async def test_get_term(client):
    term = await client.get_term("voltage-stability")
    assert term == {"id": "voltage-stability", "title": "Voltage Stability"}


@pytest.mark.asyncio
async def test_list_tags(client):
    assert await client.list_tags() == [{"tag": "stability", "count": 12}]


@pytest.mark.asyncio
async def test_search_by_tag(client):
    results = await client.search_terms(tag="stability", limit=10)
    assert results[0].tags == ["stability"]


@pytest.mark.asyncio
async def test_http_errors_are_preserved(client):
    with pytest.raises(httpx.HTTPStatusError) as error:
        await client.get_term("missing-term")
    assert error.value.response.status_code == 404
