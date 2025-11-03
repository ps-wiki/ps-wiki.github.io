---
layout: page
title: add new term
permalink: /add-new/
description:
nav: false
horizontal: false
---

There are two ways to add a new term to the wiki: using a Markdown file or a JSON file.

# Add new term from example Markdown file

Use [stability.md](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/_wiki/stability.md) as a reference for creating new term entries.

After creating the Markdown file, convert it back to JSON format using the provided script:

```bash
python database/pyscripts/md2json.py --input _wiki/stability.md --output database/json/stability.json
```

*In the website deployment process, the JSON files are automatically converted back to Markdown for rendering.*
Note there can be minor formatting differences between the original Markdown and the converted Markdown due to the conversion process.

# Add new term from example JSON File

Use [stability.json](https://github.com/ps-wiki/ps-wiki.github.io/blob/main/database/json/stability.json) as a reference for creating new term entries.

After creating the JSON file, you can convert it to Markdown format using the provided script:

```bash
python database/pyscripts/json2md.py --input database/json/stability.json --output _wiki/stability.md
```

Following conventions should be observed when creating or editing term JSON files:

- File Naming: Each term is stored in a separate JSON file named `<term-id>.json`.
- The `id` field should match the filename, e.g. stability.json → "id": "stability".
- The `source_keys` in each section and figure should correspond to entries in the bibliography file located at `assets/bibliography/papers.bib`.
- The `body_md` field contains the main content in Markdown format. Use standard Markdown syntax for headings, lists, and formatting.
- Figures should be stored in the `assets/img/pswiki/` directory, and their paths should be correctly referenced in the JSON.
- In each figure entry: 1) Use a relative path such as "/assets/img/pswiki/example-figure.png". 2) Include a concise caption_md (in Markdown) and the relevant source_keys. 3) Set "zoomable": true for figures intended to support click-to-zoom in Jekyll.
