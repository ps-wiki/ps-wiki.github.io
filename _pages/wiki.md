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

- [<u>Stability</u>](/wiki/stability) &nbsp; [<u>Resonance Stability</u>](/wiki/resonance-stability) &nbsp; [<u>Rotor Angle Stability</u>](/wiki/rotor-angle-stability) &nbsp; [<u>Voltage Stability</u>](/wiki/voltage-stability) &nbsp; [<u>Frequency Stability</u>](/wiki/frequency-stability) &nbsp; [<u>Converter-Driven Stability</u>](/wiki/converter-driven-stability)
- [<u>Security</u>](/wiki/security) &nbsp; [<u>Security Constrained Economic Dispatch</u>](/wiki/economic-dispatch)
- [<u>Reliability</u>](/wiki/reliability) &nbsp; [<u>Operating Reliability</u>](/wiki/operating-reliability) &nbsp; [<u>Adequacy</u>](/wiki/adequacy) &nbsp; [<u>Real-Time Reliability Model</u>](/wiki/real-time-reliability-model)

- [<u>Small Signal Stability</u>](/wiki/small-signal-stability) &nbsp; [<u>Stability Limits</u>](/wiki/stability-limits)

**Frequency**

- [<u>FFR</u>](/wiki/fast-frequency-response) &nbsp; [<u>PFR</u>](/wiki/primary-frequency-response) &nbsp; [<u>AGC</u>](/wiki/automatic-generation-control) &nbsp; [<u>CPS1</u>](/wiki/control-performance-standard-1) &nbsp; [<u>CPS2</u>](/wiki/control-performance-standard-2) &nbsp; [<u>ACE</u>](/wiki/area-control-error)
- [<u>Frequency Response</u>](/wiki/frequnecy-response) &nbsp; [<u>Primary Control</u>](/wiki/primary-control) &nbsp; [<u>Secondary Control</u>](/wiki/secondary-control) &nbsp; [<u>Tertiary Control</u>](/wiki/tertiary-control)
- [<u>Frequency Deviation</u>](/wiki/frequency-deviation) &nbsp; [<u>Frequency Regulation</u>](/wiki/frequency-regulation)

**Reserve**

- [<u>Contingency Reserve</u>](/wiki/contingency-reserve) &nbsp; [<u>Regulating Reserve</u>](/wiki/regulating-reserve)
- [<u>Spinning Reserve</u>](/wiki/spinning-reserve) &nbsp; [<u>Non-Spinning Reserve</u>](/wiki/non-spinning-reserve)
- [<u>Operating Reserve</u>](/wiki/operting-reserve) [<u>Operating Reserve – Spinning</u>](/wiki/operating-reserve-spinning) &nbsp; [<u>Operating Reserve – Non-Spinning</u>](/wiki/operating-reserve-non-spinning)

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
