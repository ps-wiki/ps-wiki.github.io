#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Shared utilities for PS-Wiki database scripts.

This module provides common functions used across multiple scripts to:
- Load and write JSON files consistently
- Validate terms against JSON schema
- Handle file dates and timestamps
- Provide string manipulation utilities
"""

import json
import sys
from datetime import datetime, date as date_cls
from pathlib import Path
from typing import Any, Dict, List, Optional

# Schema URL constant
SCHEMA_URL = "https://ps-wiki.github.io/schema/v1/term.schema.json"

# Directory constants
DEFAULT_WIKI_DIR = Path("_wiki")
DEFAULT_JSON_DIR = Path("database/json")
DEFAULT_SCHEMA_PATH = Path("database/schema/v1/term.schema.json")
DEFAULT_BUILD_DIR = Path("database/build")


# ---------- JSON I/O ----------


def load_json(path: Path) -> Dict[str, Any]:
    """
    Load JSON file with error handling.

    Args:
        path: Path to JSON file

    Returns:
        Parsed JSON data as dictionary

    Raises:
        RuntimeError: If file cannot be read or parsed
    """
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise RuntimeError(f"File not found: {path}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Invalid JSON in {path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to load {path}: {e}")


def load_term_json(path: Path) -> Dict[str, Any]:
    """
    Load a term JSON file with validation of basic structure.

    Args:
        path: Path to term JSON file

    Returns:
        Term data dictionary

    Raises:
        RuntimeError: If file is invalid or missing required fields
    """
    data = load_json(path)

    # Basic structure validation
    if not isinstance(data, dict):
        raise RuntimeError(f"{path}: Root must be an object")

    if "id" not in data:
        raise RuntimeError(f"{path}: Missing required field 'id'")

    return data


def write_json(path: Path, data: Dict[str, Any], indent: int = 2) -> None:
    """
    Write JSON file with consistent formatting.

    Args:
        path: Output path
        data: Data to write
        indent: Indentation level (default: 2)
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(data, ensure_ascii=False, indent=indent) + "\n"
    path.write_text(content, encoding="utf-8")


def write_if_changed(path: Path, content: str) -> bool:
    """
    Write file only if content differs from existing file.

    Args:
        path: Output path
        content: Content to write

    Returns:
        True if file was written, False if skipped (unchanged)
    """
    if path.exists():
        try:
            existing = path.read_text(encoding="utf-8")
            if existing == content:
                return False
        except Exception:
            pass  # If we can't read, write anyway

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


# ---------- Schema Validation ----------


def validate_term_schema(
    term: Dict[str, Any], schema_path: Optional[Path] = None
) -> List[str]:
    """
    Validate a term against the JSON schema.

    Args:
        term: Term data to validate
        schema_path: Path to schema file (optional, uses default if not provided)

    Returns:
        List of validation error messages (empty if valid)
    """
    try:
        from jsonschema.validators import Draft202012Validator
    except ImportError:
        return ["jsonschema package not installed (pip install jsonschema)"]

    # Default schema path
    if schema_path is None:
        schema_path = (
            Path(__file__).parent.parent / "schema" / "v1" / "term.schema.json"
        )

    if not schema_path.exists():
        return [f"Schema file not found: {schema_path}"]

    try:
        schema = load_json(schema_path)
        validator = Draft202012Validator(schema)
    except Exception as e:
        return [f"Failed to load schema: {e}"]

    errors = []
    for e in validator.iter_errors(term):
        # Build path string
        path_parts = []
        for p in e.path:
            if isinstance(p, int):
                path_parts.append(f"[{p}]")
            else:
                if path_parts and not path_parts[-1].startswith("["):
                    path_parts.append(".")
                path_parts.append(str(p))

        location = "".join(path_parts) or "(root)"
        errors.append(f"{location}: {e.message}")

    return errors


def ensure_schema_reference(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensure $schema field is present in term data.

    Args:
        data: Term data dictionary

    Returns:
        Modified data with $schema field (creates new dict if needed)
    """
    if "$schema" not in data:
        # Put $schema first
        return {"$schema": SCHEMA_URL, **data}
    return data


# ---------- Date Handling ----------


def iso_date_from_ts(ts: float) -> str:
    """
    Convert POSIX timestamp to ISO date string (YYYY-MM-DD).

    Args:
        ts: POSIX timestamp

    Returns:
        ISO date string
    """
    return datetime.fromtimestamp(ts).date().isoformat()


def derive_file_dates(path: Path) -> Dict[str, str]:
    """
    Derive creation and modification dates from file metadata.

    Args:
        path: File path

    Returns:
        Dictionary with 'created' and 'last_modified' ISO date strings
    """
    st = path.stat()

    # Try to get creation time (macOS has st_birthtime, Linux uses st_ctime)
    created_ts = getattr(st, "st_birthtime", None)
    if created_ts is None:
        created_ts = st.st_ctime

    return {
        "created": iso_date_from_ts(created_ts),
        "last_modified": iso_date_from_ts(st.st_mtime),
    }


def coerce_date_str(v: Any) -> str:
    """
    Coerce various date formats to ISO string (YYYY-MM-DD).

    Args:
        v: Date value (datetime, date, or string)

    Returns:
        ISO date string, or empty string if invalid
    """
    if isinstance(v, datetime):
        return v.date().isoformat()
    if isinstance(v, date_cls):
        return v.isoformat()
    if isinstance(v, str):
        return v.strip()
    return ""


# ---------- String Utilities ----------


def slugify_kebab(s: str) -> str:
    """
    Convert string to kebab-case slug.

    Args:
        s: Input string

    Returns:
        Kebab-case slug (lowercase, hyphens, alphanumeric only)
    """
    import re

    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"


# ---------- List Utilities ----------


def ensure_list(v: Any) -> List[Any]:
    """
    Normalize value to list (handles None, singleton, or existing list).

    Args:
        v: Value to normalize

    Returns:
        List (empty if None, singleton list if not already a list)
    """
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


# ---------- Progress Reporting ----------


class ProgressReporter:
    """Simple progress reporter for batch operations."""

    def __init__(self, total: int, verbose: bool = False):
        """
        Initialize progress reporter.

        Args:
            total: Total number of items to process
            verbose: Whether to show verbose output
        """
        self.total = total
        self.verbose = verbose
        self.current = 0
        self.errors = 0
        self.warnings = 0

    def update(self, status: str = "OK", message: str = ""):
        """
        Update progress.

        Args:
            status: Status string ("OK", "ERROR", "WARN", "SKIP")
            message: Optional message to display
        """
        self.current += 1

        if status == "ERROR":
            self.errors += 1
        elif status == "WARN":
            self.warnings += 1

        if self.verbose or status in ("ERROR", "WARN"):
            prefix = f"[{self.current}/{self.total}]"
            print(f"{prefix} {status:5s} {message}")

    def summary(self) -> str:
        """
        Get summary string.

        Returns:
            Summary of processing results
        """
        return (
            f"Processed {self.current}/{self.total} items: "
            f"{self.errors} errors, {self.warnings} warnings"
        )


# ---------- Color Output (Optional) ----------


class Colors:
    """ANSI color codes for terminal output."""

    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    GRAY = "\033[90m"

    @staticmethod
    def enabled() -> bool:
        """Check if colors should be enabled (TTY check)."""
        return sys.stdout.isatty()

    @classmethod
    def error(cls, text: str) -> str:
        """Format error text in red."""
        if cls.enabled():
            return f"{cls.RED}{text}{cls.RESET}"
        return text

    @classmethod
    def success(cls, text: str) -> str:
        """Format success text in green."""
        if cls.enabled():
            return f"{cls.GREEN}{text}{cls.RESET}"
        return text

    @classmethod
    def warning(cls, text: str) -> str:
        """Format warning text in yellow."""
        if cls.enabled():
            return f"{cls.YELLOW}{text}{cls.RESET}"
        return text

    @classmethod
    def info(cls, text: str) -> str:
        """Format info text in blue."""
        if cls.enabled():
            return f"{cls.BLUE}{text}{cls.RESET}"
        return text
