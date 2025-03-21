---
layout: page
title: wiki
permalink: /wiki/
description:
nav: true
nav_order: 2
horizontal: false
---

**Reliability, Security, and Stability**

- [Stability](/wiki/stability) &nbsp; [Resonance Stability](/wiki/resonance-stability) &nbsp; [Rotor Angle Stability](/wiki/rotor-angle-stability) &nbsp; [Voltage Stability](/wiki/voltage-stability) &nbsp; [Frequency Stability](/wiki/frequency-stability) &nbsp; [Converter-Driven Stability](/wiki/converter-driven-stability)
- [Security](/wiki/security) &nbsp; [Security Constrained Economic Dispatch](/wiki/economic-dispatch)
- [Reliability](/wiki/reliability) &nbsp; [Operating Reliability](/wiki/operating-reliability) &nbsp; [Adequacy](/wiki/adequacy)

- [Small Signal Stability](/wiki/small-signal-stability)

- [Real-Time Reliability Model (a.k.a. EMS model)](/wiki/real-time-reliability-model) &nbsp; [Transient Stability Assessment](/wiki/transient-stability-assessment) &nbsp; [Stability Limits](/wiki/stability-limits)

**Frequency**

- [FFR](/wiki/fast-frequency-response) &nbsp; [PFR](/wiki/primary-frequency-response) &nbsp; [AGC](/wiki/automatic-generation-control) &nbsp; [CPS1](/wiki/control-performance-standard-1) &nbsp; [CPS2](/wiki/control-performance-standard-2) &nbsp; [ACE](/wiki/area-control-error)
- [Frequency Response](/wiki/frequnecy-response) &nbsp; [Primary Control](/wiki/primary-control) &nbsp; [Secondary Control](/wiki/secondary-control) &nbsp; [Tertiary Control](/wiki/tertiary-control)
- [Frequency Deviation](/wiki/frequency-deviation) &nbsp; [Frequency Regulation](/wiki/frequency-regulation)

**Reserve**

- [Contingency Reserve](/wiki/contingency-reserve) &nbsp; [Regulating Reserve](/wiki/regulating-reserve)
- [Spinning Reserve](/wiki/spinning-reserve) &nbsp; [Non-Spinning Reserve](/wiki/non-spinning-reserve)
- [Operating Reserve](/wiki/operting-reserve) &nbsp; [Operating Reserve – Spinning](/wiki/operating-reserve-spinning) &nbsp; [Operating Reserve – Non-Spinning](/wiki/operating-reserve-non-spinning)

- [Contingency](/wiki/contingency) &nbsp; [Contingency List](/wiki/contingency-list) &nbsp; [Contingency Analysis](/wiki/contingency-analysis)
- [Emergency](/wiki/emergency)

<br>

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
