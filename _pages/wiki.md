---
layout: page
title: wiki
permalink: /wiki/
description:
nav: true
nav_order: 2
horizontal: false
---

{% capture wiki-quicklink %}
{% include_relative wiki-quicklink.md %}
{% endcapture %}

{{ wiki-quicklink }}

<!-- pages/wiki.md -->
<div class="wiki">
{% if site.enable_pswiki_categories and page.display_categories %}
  <!-- Display categorized wiki -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_pswiki = site.wiki | where: "category", category %}
  {% assign sorted_pswiki = categorized_pswiki | sort: "importance" %}
  <!-- Generate cards for each wiki -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for wiki in sorted_pswiki %}
      {% include pswiki_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for wiki in sorted_pswiki %}
      {% include wiki.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display wiki without categories -->

{% assign sorted_pswiki = site.wiki | sort: "importance" %}

  <!-- Generate cards for each wiki -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for wiki in sorted_pswiki %}
      {% include pswiki_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for wiki in sorted_pswiki %}
      {% include wiki.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>

<br>
