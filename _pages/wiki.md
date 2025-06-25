---
layout: page
title: wiki
permalink: /wiki/
description: Glossary of terms used in power systems
nav: true
nav_order: 2
---

<div class="col-auto mb-3">
  <a href="/wiki-tag/" class="btn btn-sm wiki-tags-button" style="background-color: #28A745; border-color: #28A745; color: #FFFFFF; padding: 0.25rem 0.5rem; font-size: 0.875rem;">
    <i class="fas fa-filter"></i> Tags
  </a>
</div>

<ul class="wiki-list">
  {% assign sorted_wiki_terms = site.wiki | sort:"title" %}

{% for term in sorted_wiki_terms %}

<li>
<a href="{{ term.url | relative_url }}">{{ term.title }}</a>
{% if term.description %}
<p>{{ term.description }}</p>
{% endif %}
</li>
{% endfor %}

</ul>
