#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PS-Wiki REST API Contract Test Suite (Pydantic v2 compatible)
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin

try:
    # Pydantic v2 imports
    from pydantic import (
        BaseModel,
        Field,
        ValidationError,
        field_validator,
        model_validator,
        RootModel,
    )
except Exception:
    print(
        "ERROR: pydantic v2 is required. Install with `pip install pydantic>=2`.",
        file=sys.stderr,
    )
    sys.exit(2)

try:
    from urllib3.util.retry import Retry
except Exception:
    print(
        "ERROR: urllib3 is required. Install with `pip install urllib3`.",
        file=sys.stderr,
    )
    sys.exit(2)


# --- Pretty printing helpers ---
class Style:
    BOLD = "\033[1m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    DIM = "\033[2m"
    END = "\033[0m"


def ok(msg: str) -> None:
    print(f"{Style.GREEN}✓ PASS{Style.END} {msg}")


def fail(msg: str) -> None:
    print(f"{Style.RED}✗ FAIL{Style.END} {msg}")


def warn(msg: str) -> None:
    print(f"{Style.YELLOW}! WARN{Style.END} {msg}")


def header(title: str) -> None:
    line = "═" * max(40, len(title) + 10)
    print(f"\n{Style.BLUE}╔{line}╗{Style.END}")
    print(f"{Style.BLUE}║{Style.END}  {Style.BOLD}{title}{Style.END}")
    print(f"{Style.BLUE}╚{line}╝{Style.END}\n")


# --- Pydantic models reflecting the OpenAPI schemas ---

DATE_RX = re.compile(r"^\d{4}-\d{2}-\d{2}$")  # ISO date (YYYY-MM-DD)


class TermSummary(BaseModel):
    id: str
    title: str
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    updated_at: str = Field(..., description="ISO date (YYYY-MM-DD)")

    @field_validator("updated_at")
    @classmethod
    def _date_format(cls, v: str) -> str:
        if not DATE_RX.match(v):
            raise ValueError("updated_at must be ISO date YYYY-MM-DD")
        return v


# In v2, use RootModel for "arbitrary JSON object" payloads
class Term(RootModel[Dict[str, Any]]):
    @model_validator(mode="before")
    @classmethod
    def ensure_object(cls, v):
        if not isinstance(v, dict):
            raise ValueError("Term payload must be an object")
        return v


class TagItem(BaseModel):
    tag: str
    count: int


class TagsResponse(BaseModel):
    tags: List[TagItem]


class ChangesItem(BaseModel):
    id: str
    updated_at: str

    @field_validator("updated_at")
    @classmethod
    def _date_format(cls, v: str) -> str:
        if not DATE_RX.match(v):
            raise ValueError("updated_at must be ISO date YYYY-MM-DD")
        return v


class ChangesResponse(BaseModel):
    items: List[ChangesItem]


class TermsResponse(BaseModel):
    items: List[TermSummary]
    next_cursor: Optional[str] = None  # string or null


# --- HTTP client with retries ---
def make_session(timeout_s: int = 10, total_retries: int = 2) -> requests.Session:
    sess = requests.Session()
    retry = Retry(
        total=total_retries,
        backoff_factor=0.3,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)
    sess.request = _wrap_with_timeout(sess.request, timeout_s)  # type: ignore
    return sess


def _wrap_with_timeout(fn, timeout_s: int):
    def inner(method, url, **kwargs):
        kwargs.setdefault("timeout", timeout_s)
        return fn(method, url, **kwargs)

    return inner


# --- Validators corresponding to each endpoint ---


def validate_terms_payload(
    payload: Dict[str, Any], do_schema: bool
) -> Tuple[bool, str, List[TermSummary]]:
    try:
        if do_schema:
            parsed = TermsResponse.model_validate(payload)
        else:
            if "items" not in payload or not isinstance(payload["items"], list):
                raise ValueError("items[] missing or not a list")
            parsed = TermsResponse(items=[], next_cursor=payload.get("next_cursor"))
            for it in payload["items"]:
                parsed.items.append(
                    TermSummary(
                        id=str(it.get("id", "")),
                        title=str(it.get("title", "")),
                        summary=it.get("summary"),
                        tags=it.get("tags"),
                        updated_at=str(it.get("updated_at", "1970-01-01")),
                    )
                )
        return True, "Valid /v1/terms payload", parsed.items
    except (ValidationError, ValueError) as e:
        return False, f"/v1/terms schema mismatch: {e}", []


def validate_term_payload(payload: Dict[str, Any], do_schema: bool) -> Tuple[bool, str]:
    try:
        if do_schema:
            _ = Term.model_validate(payload)
        else:
            if not isinstance(payload, dict):
                raise ValueError("Payload is not an object")
        return True, "Valid /v1/terms/{id} payload"
    except (ValidationError, ValueError) as e:
        return False, f"/v1/terms/{{id}} schema mismatch: {e}"


def validate_tags_payload(payload: Dict[str, Any], do_schema: bool) -> Tuple[bool, str]:
    try:
        if do_schema:
            _ = TagsResponse.model_validate(payload)
        else:
            if "tags" not in payload or not isinstance(payload["tags"], list):
                raise ValueError("tags[] missing or not a list")
        return True, "Valid /v1/tags payload"
    except (ValidationError, ValueError) as e:
        return False, f"/v1/tags schema mismatch: {e}"


def validate_changes_payload(
    payload: Dict[str, Any], do_schema: bool
) -> Tuple[bool, str]:
    try:
        if do_schema:
            _ = ChangesResponse.model_validate(payload)
        else:
            if "items" not in payload or not isinstance(payload["items"], list):
                raise ValueError("items[] missing or not a list")
        return True, "Valid /v1/changes payload"
    except (ValidationError, ValueError) as e:
        return False, f"/v1/changes schema mismatch: {e}"


# --- Test runner ---


@dataclass
class TestConfig:
    base_url: str
    query: Optional[str]
    tag: Optional[str]
    since: str
    validate_schema: bool
    limit_for_page: int = 3


def get_json(
    session: requests.Session, url: str, params: Dict[str, Any] | None = None
) -> Tuple[int, Dict[str, Any]]:
    r = session.get(url, params=params)
    status = r.status_code
    try:
        data = r.json()
    except Exception:
        data = {}
    return status, data


def test_terms_list(
    sess: requests.Session, cfg: TestConfig
) -> Tuple[bool, Optional[str], List[TermSummary]]:
    url = urljoin(cfg.base_url.rstrip("/") + "/", "v1/terms")
    params = {"limit": cfg.limit_for_page}
    if cfg.query:
        params["query"] = cfg.query
    if cfg.tag:
        params["tag"] = cfg.tag

    status, data = get_json(sess, url, params=params)
    if status != 200:
        fail(f"GET /v1/terms -> HTTP {status}")
        return False, None, []
    ok("GET /v1/terms -> HTTP 200")

    valid, msg, items = validate_terms_payload(data, cfg.validate_schema)
    if valid:
        ok(msg)
    else:
        fail(msg)
        return False, None, []

    next_cursor = data.get("next_cursor", None)
    if next_cursor:
        status2, data2 = get_json(
            sess, url, params={"cursor": next_cursor, "limit": cfg.limit_for_page}
        )
        if status2 == 200:
            ok("GET /v1/terms (pagination) -> HTTP 200")
            v2, m2, items2 = validate_terms_payload(data2, cfg.validate_schema)
            if v2:
                ok("Pagination payload valid")
                if items and items2 and items[0].id == items2[0].id:
                    warn(
                        "First items of page1 and page2 are identical; verify cursor behavior"
                    )
            else:
                fail(m2)
        else:
            warn(f"GET /v1/terms with cursor returned HTTP {status2}")

    return True, (items[0].id if items else None), items


def test_term_detail(
    sess: requests.Session, cfg: TestConfig, any_id: Optional[str]
) -> bool:
    if not any_id:
        warn("Skip GET /v1/terms/{id}: no id from listing")
        return True
    url = urljoin(cfg.base_url.rstrip("/") + "/", f"v1/terms/{any_id}")
    status, data = get_json(sess, url)
    if status != 200:
        fail(f"GET /v1/terms/{any_id} -> HTTP {status}")
        return False
    ok(f"GET /v1/terms/{any_id} -> HTTP 200")

    valid, msg = validate_term_payload(data, cfg.validate_schema)
    if valid:
        ok(msg)
        return True
    else:
        fail(msg)
        return False


def test_tags(sess: requests.Session, cfg: TestConfig) -> bool:
    url = urljoin(cfg.base_url.rstrip("/") + "/", "v1/tags")
    status, data = get_json(sess, url)
    if status != 200:
        fail(f"GET /v1/tags -> HTTP {status}")
        return False
    ok("GET /v1/tags -> HTTP 200")

    valid, msg = validate_tags_payload(data, cfg.validate_schema)
    if valid:
        ok(msg)
        return True
    else:
        fail(msg)
        return False


def test_changes(sess: requests.Session, cfg: TestConfig) -> bool:
    url = urljoin(cfg.base_url.rstrip("/") + "/", "v1/changes")
    status, data = get_json(sess, url, params={"since": cfg.since})
    if status != 200:
        fail(f"GET /v1/changes?since=... -> HTTP {status}")
        return False
    ok("GET /v1/changes?since=... -> HTTP 200")

    valid, msg = validate_changes_payload(data, cfg.validate_schema)
    if valid:
        ok(msg)
        return True
    else:
        fail(msg)
        return False


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="PS-Wiki API Contract Test Suite")
    parser.add_argument(
        "--base-url",
        default="https://ps-wiki.github.io",
        help="Base URL (default: https://ps-wiki.github.io). Examples: http://localhost:8787 or https://pswiki-api.jinninggm.workers.dev",
    )
    parser.add_argument("--query", help="Optional free-text query for /v1/terms")
    parser.add_argument("--tag", help="Optional tag filter for /v1/terms")
    parser.add_argument(
        "--since",
        default="2024-01-01",
        help="ISO date (YYYY-MM-DD) for /v1/changes (default: 2024-01-01)",
    )
    parser.add_argument(
        "--validate-schema",
        action="store_true",
        help="Enable strict schema validation with Pydantic",
    )
    parser.add_argument(
        "--timeout", type=int, default=10, help="HTTP timeout seconds (default 10)"
    )
    args = parser.parse_args(argv)

    header("PS-Wiki API Contract Test Suite")
    print(f"Testing base URL: {Style.BOLD}{args.base_url}{Style.END}\n")

    sess = make_session(timeout_s=args.timeout, total_retries=2)
    cfg = TestConfig(
        base_url=args.base_url,
        query=args.query,
        tag=args.tag,
        since=args.since,
        validate_schema=args.validate_schema,
    )

    overall_ok = True

    passed_terms, first_id, _items = test_terms_list(sess, cfg)
    overall_ok &= passed_terms
    overall_ok &= test_term_detail(sess, cfg, first_id)
    overall_ok &= test_tags(sess, cfg)
    overall_ok &= test_changes(sess, cfg)

    print()
    if overall_ok:
        print(f"{Style.BOLD}{Style.GREEN}All tests passed ✅{Style.END}")
        return 0
    else:
        print(f"{Style.BOLD}{Style.RED}One or more tests failed ❌{Style.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
