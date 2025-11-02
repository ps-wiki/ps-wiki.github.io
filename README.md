# Power Systems Wiki

This wiki is an open reference designed to compile and share terminologies used in the power systems engineering.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC_BY--NC_4.0-lightgrey.svg)](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/LICENSE)
[![Deploy site](https://github.com/ps-wiki/ps-wiki.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/ps-wiki/ps-wiki.github.io/actions/workflows/deploy.yml)
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![GitHub last commit (main)](https://img.shields.io/github/last-commit/ps-wiki/ps-wiki.github.io/main?label=last%20commit%20to%20master)](https://github.com/ps-wiki/ps-wiki.github.io/commits/main/)

## Why This Wiki Exists

Language is inherently ambiguous, and power system terminologies are no exception. Inspired by an email titled “Definitions of Smart Grids a Decade Ago – What Has Changed?” on Power-Globe in 2024, I decided to compile terminologies from papers, standards, reports, and other traceable sources to build this wiki.

## Contributing

We welcome contributions from the community! If you have suggestions, corrections, or new terms to add, please open an issue or submit a pull request.

## Website Overview

Built upon the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme, this website introduces significant enhancements, particularly in its new wiki section.

A custom [wiki layout](./_layouts/wiki.liquid) adapted from the `distill` layout, has been developed to effectively host item-based terminologies. Key features include:

- **Metadata Display**: Last update date, tags, and related term links
- **Navigation**: Previous/Next term links for easy Browse
- **Direct Editing**: A link to edit the term directly on GitHub
- **Community Engagement**: Integrated Giscus comments

## Database

The folder `database` contains the source data and scripts for generating the wiki:

- Folder `database/json` contains the source JSON files for the wiki.
- Folder `database/pyscripts` contains Python scripts for processing the data.

### Example JSON File

Use [stability.json](./database/json/stability.json) as a reference for creating new term entries.
Below is an example structure of a JSON file for a term:

```json
{
  "id": "example-term",
  "title": "Example Term",
  "description": "A concise description of this concept.",
  "language": "en",
  "tags": [
    // existing tags: https://ps-wiki.github.io/wiki-tag/#all-tags
    "tag1",
    "tag2"
  ],
  "related": ["other-term-id-1", "other-term-id-2"],
  "version": "1.0.0", // SemVer version of this term entry
  "breaking": false, // set to true if there are breaking changes of this term compared to previous version
  "dates": {
    "created": "2025-11-01",
    "last_modified": "2025-11-01"
  },
  "authors": [
    {
      "name": "Contributor Name",
      "url": "https://example.com"
    },
    {
      "name": "Another Contributor",
      "url": "https://example.org"
    }
  ],
  "content": {
    "sections": [
      {
        "order": 1,
        "id": "definition-by-institution1",
        "title": "Definition by Institution 1",
        "type": "definition", // "definition" for quoted content, "note" for others
        "source_keys": [
          "key1" // ensure the key exists in assets/bibliography/papers.bib
        ],
        "page": "p45", // or "p45, Revision 2" if applicable to indicate specific revision
        "body_md": "> The ability of an electric power system to maintain a state of equilibrium during normal and abnormal conditions or disturbances.\n",
        "figures": []
      },
      {
        "order": 2,
        "id": "elaboration-in-article",
        "title": "Elaboration in an Article",
        "type": "definition",
        "source_keys": [],
        "page": null,
        "body_md": "This section elaborates on the concept, its relevance, or provides historical context.\n",
        "figures": [
          {
            "path": "/assets/img/pswiki/example-figure.png",
            "caption_md": "Fig. 1. Example figure caption. (from <d-cite key=\"example2024reference\"></d-cite>)",
            "zoomable": true,
            "source_keys": ["example2024reference"]
          }
        ]
      }
    ]
  }
}
```

Following conventions should be observed when creating or editing term JSON files:

- File Naming: Each term is stored in a separate JSON file named `<term-id>.json`.
- The `id` field should match the filename, e.g. stability.json → "id": "stability".
- The `source_keys` in each section and figure should correspond to entries in the bibliography file located at `assets/bibliography/papers.bib`.
- The `body_md` field contains the main content in Markdown format. Use standard Markdown syntax for headings, lists, and formatting.
- Figures should be stored in the `assets/img/pswiki/` directory, and their paths should be correctly referenced in the JSON.
- In each figure entry: 1) Use a relative path such as "/assets/img/pswiki/example-figure.png". 2) Include a concise caption_md (in Markdown) and the relevant source_keys. 3) Set "zoomable": true for figures intended to support click-to-zoom in Jekyll.

### Conda Environment

Use the following command to create the conda environment for local development:

```
conda env create --file ./pswiki/database/environment.yml
```

Use the following command to export minimal-history export (only explicit user-installed packages)

```
conda env export --from-history --file ./pswiki/database/environment.yml
```

## License

This project is licensed under the [CC-BY-NC 4.0](./LICENSE).
