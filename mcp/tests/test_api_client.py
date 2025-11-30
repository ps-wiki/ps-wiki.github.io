"""Tests for API client."""

import pytest
from pswiki_mcp.api_client import APIClient, TermSummary


@pytest.fixture
async def client():
    """Create API client for testing."""
    client = APIClient()
    yield client
    await client.close()


@pytest.mark.asyncio
async def test_search_terms(client):
    """Test searching for terms."""
    results = await client.search_terms(query="stability", limit=5)
    assert isinstance(results, list)
    assert len(results) <= 5
    if results:
        assert isinstance(results[0], TermSummary)
        assert hasattr(results[0], "id")
        assert hasattr(results[0], "title")


@pytest.mark.asyncio
async def test_get_term(client):
    """Test getting a specific term."""
    # First search to get a valid term ID
    results = await client.search_terms(query="stability", limit=1)
    if not results:
        pytest.skip("No terms found to test with")

    term_id = results[0].id
    term = await client.get_term(term_id)

    assert isinstance(term, dict)
    assert "id" in term
    assert "title" in term
    assert term["id"] == term_id


@pytest.mark.asyncio
async def test_list_tags(client):
    """Test listing tags."""
    tags = await client.list_tags()
    assert isinstance(tags, list)
    if tags:
        assert "tag" in tags[0]
        assert "count" in tags[0]
        assert isinstance(tags[0]["count"], int)


@pytest.mark.asyncio
async def test_search_by_tag(client):
    """Test searching by tag."""
    # First get available tags
    tags = await client.list_tags()
    if not tags:
        pytest.skip("No tags found to test with")

    tag_name = tags[0]["tag"]
    results = await client.search_terms(tag=tag_name, limit=10)

    assert isinstance(results, list)
    # All results should have the tag
    for result in results:
        assert tag_name.lower() in [t.lower() for t in result.tags]
