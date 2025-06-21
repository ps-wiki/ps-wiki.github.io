---
layout: page
title: archive
permalink: /wiki-tag/
description:
nav: false
horizontal: false
---

<div class="wiki-archive-page">
  <p><strong>{{ site.wiki | size }}</strong> terms in total</p>

  <h2>All Wiki Tags</h2>
  <ul class="tag-list list-inline">
    {% assign all_wiki_tags = "" %}
    {% for wiki_term in site.wiki %}
      {% if wiki_term.tags %}
        {% for tag in wiki_term.tags %}
        {% assign cleaned_tag = tag | strip | downcase %}
        {% assign all_wiki_tags = all_wiki_tags | append: cleaned_tag | append: "," %}
        {% endfor %}
      {% endif %}
    {% endfor %}
    {% assign all_wiki_tags = all_wiki_tags | split: "," | uniq | sort %}

    {% for tag in all_wiki_tags %}
      {% if tag != "" %}
      <li class="list-inline-item">
        <a href="#{{ tag | slugify }}">
          {{ tag }} ({{ site.wiki | where_exp: "item", "item.tags contains tag" | size }})
        </a>
      </li>
      {% endif %}
    {% endfor %}

  </ul>

  <hr>

  <h2>Wiki Terms by Tag</h2>
  {% for tag in all_wiki_tags %}
    {% if tag != "" %}
    <h3 id="{{ tag | slugify }}">{{ tag }}</h3>
    <ul class="wiki-tag-items">
      {% assign tagged_wiki_terms = site.wiki | where_exp: "item", "item.tags contains tag" | sort: "title" %}
      {% for term in tagged_wiki_terms %}
        <li><a href="{{ term.url | relative_url }}">{{ term.title }}</a></li>
      {% endfor %}
    </ul>
    {% endif %}
  {% endfor %}
</div>
