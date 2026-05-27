---
title: Changelog
description: Major changes in this wiki
---

This page records major changes in this wiki.

## 2026

### 05-27

- Added reference URL health scanner (`python pswiki.py check-refs`) — checks all citation URLs in `papers.bib` for broken links, with optional Wayback Machine recovery for NERC entries; reduced false positives by reclassifying HTTP 403 (bot-blocking CDNs) as temporary rather than broken
- Added quarterly CI workflow for automated reference health scanning; results are surfaced in a persistent GitHub Issue
- Fixed 7 broken citations in `papers.bib`: 5 NERC URLs replaced with Wayback Machine archive snapshots, 2 PJM manual entries pinned from floating current-doc URLs to versioned archive paths
- Sanitized `papers.bib`: removed al-folio display fields (`pdf`, `html`, `bibtex_show`) no longer used by MkDocs renderer
- Removed per-term `version` field; term pages now show last-modified date only (`version` no longer appears in `/v1/terms/{id}` API responses)
- Fixed edit-page button to link to the correct GitHub repo (`ps-wiki.github.io`) and source file (`_wiki/<id>.md`)
- Added MCP Server documentation page
- Completed Jekyll/al-folio cleanup: removed Docker configs, Ruby plugins, 9 stale CI workflows, and `_config.yml` (repo is now Python-only)
- Consolidated Python dependencies into `requirements-dev.txt` at repo root
- Added `pswiki.py` centralized CLI — all developer workflows (`new`, `process`, `validate`, `serve`, `build`, `check-refs`) go through one entry point

### 05-26

- Migrated site from al-folio/Jekyll to MkDocs Material
- Added prev/next alphabetical navigation on each term page
- Added sortable All Terms table
- Added Development and REST API documentation pages
- Removed per-term `version` field; term pages now show last-modified date only (`version` no longer appears in `/v1/terms/{id}` API responses)
- Citation footnotes now link to `https://doi.org/{doi}` when a DOI is available
- Fixed edit-page button to link directly to the source `_wiki/<id>.md` file on GitHub

## 2025

### 12-04

- Add search bar in wiki page

### 11-26

- Improve pyscript support

### 11-03

- Add REST API for term search

### 11-01

- Add JSON based database, now the term is mainly stored in JSON files
- Add pyscripts to convert between JSON and MD

### 10-30

- Add terms
- Wording

### 06-19

- Major update to the wiki structure
- Scan all terms

### 06-17

- Change format to include last updated date
- Revise terms
- Simplify change log

### 03-14

- Refactor ps-wiki as an individual repository

## 2024

### 12-11

- Start this wiki
