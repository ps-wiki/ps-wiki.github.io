---
layout: page
title: wiki
permalink: /wiki/
description: Glossary of terms used in power systems
nav: true
nav_order: 2
horizontal: true
---

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
