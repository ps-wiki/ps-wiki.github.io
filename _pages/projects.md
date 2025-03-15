---
layout: page
title: wiki
permalink: /wiki/
description:
nav: true
nav_order: 3
display_categories: [wiki]
horizontal: false
---

**Reliability, Security, and Stability**

- [<u>Stability</u>](/wiki/stability) &nbsp; [<u>Resonance Stability</u>](/wiki/resonance-stability) &nbsp; [<u>Rotor Angle Stability</u>](/wiki/rotor-angle-stability) &nbsp; [<u>Voltage Stability</u>](/wiki/voltage-stability) &nbsp; [<u>Frequency Stability</u>](/wiki/frequency-stability)
- [<u>Small Signal Stability</u>](/wiki/small-signal-stability) &nbsp; [<u>Stability Limits</u>](/wiki/stability-limits)
- [<u>Security</u>](/wiki/security) &nbsp; [<u>Security Constrained Economic Dispatch</u>](/wiki/economic-dispatch)
- [<u>Reliability</u>](/wiki/reliability) &nbsp; [<u>Real-Time Reliability Model</u>](/wiki/real-time-reliability-model) &nbsp; [<u>Operating Reliability</u>](/wiki/operating-reliability) &nbsp; [<u>Adequacy</u>](/wiki/adequacy)

**Frequency**

- [<u>FFR</u>](/wiki/fast-frequency-response) &nbsp; [<u>PFR</u>](/wiki/primary-frequency-response) &nbsp; [<u>AGC</u>](/wiki/automatic-generation-control) &nbsp; [<u>CPS1</u>](/wiki/control-performance-standard-1) &nbsp; [<u>CPS2</u>](/wiki/control-performance-standard-2) &nbsp; [<u>ACE</u>](/wiki/area-control-error)
- [<u>Frequency Response</u>](/wiki/frequnecy-response) &nbsp; [<u>Primary Control</u>](/wiki/primary-control) &nbsp; [<u>Secondary Control</u>](/wiki/secondary-control) &nbsp; [<u>Tertiary Control</u>](/wiki/tertiary-control)
- [<u>Frequency Deviation</u>](/wiki/frequency-deviation) &nbsp; [<u>Frequency Regulation</u>](/wiki/frequency-regulation)

<br>

<!-- pages/projects.md -->
<div class="projects">
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category }}</h2>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate cards for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate cards for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1 row-cols-md-2">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1 row-cols-md-3">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>
