---
layout: page
title: overview
permalink: /wiki-overview/
description:
nav: false
horizontal: false
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
