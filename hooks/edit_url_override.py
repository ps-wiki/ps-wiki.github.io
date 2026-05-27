def on_page_context(context, page, **kwargs):
    """Override page.edit_url from frontmatter edit_url, so generated wiki pages
    link back to _wiki/<id>.md in the source repo rather than docs/wiki/<id>.md."""
    if "edit_url" in page.meta:
        page.edit_url = page.meta["edit_url"]
    return context
