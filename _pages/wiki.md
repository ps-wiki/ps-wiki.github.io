---
layout: page
title: wiki
permalink: /wiki/
description: Glossary of terms used in power systems
nav: true
nav_order: 2
---

<div class="d-flex flex-wrap align-items-center mb-3 gap-2">
  <div class="col-auto">
    <a href="/wiki-tag/" class="btn btn-sm wiki-tags-button" style="background-color: #28A745; border-color: #28A745; color: #FFFFFF; padding: 0.25rem 0.5rem; font-size: 0.875rem;">
      <i class="fas fa-filter"></i> Tags
    </a>
  </div>
  
  <div class="wiki-sort-controls d-flex align-items-center gap-2">
    <label for="wiki-sort-criteria" class="mb-0" style="font-size: 0.875rem;">Sort by:</label>
    <select id="wiki-sort-criteria" class="form-select form-select-sm" style="width: auto;">
      <option value="title">Alphabetical</option>
      <option value="date">Add Time</option>
      <option value="lastmod">Last Modified</option>
    </select>
    
    <label for="wiki-sort-order" class="mb-0" style="font-size: 0.875rem;">Order:</label>
    <select id="wiki-sort-order" class="form-select form-select-sm" style="width: auto;">
      <option value="asc">Ascending</option>
      <option value="desc">Descending</option>
    </select>
  </div>
</div>

<ul class="wiki-list">
  {% assign sorted_wiki_terms = site.wiki | sort:"title" %}

{% for term in sorted_wiki_terms %}

<li data-title="{{ term.title }}" data-date="{{ term.date | date: '%Y-%m-%d' }}" data-lastmod="{{ term.lastmod | date: '%Y-%m-%d' }}">
<a href="{{ term.url | relative_url }}">{{ term.title }}</a>
{% if term.description %}
<p>{{ term.description }}</p>
{% endif %}
</li>
{% endfor %}

</ul>

<script src="{{ '/assets/js/wiki-sort.js' | relative_url }}"></script>
