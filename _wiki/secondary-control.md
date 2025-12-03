---
title: Secondary Control
description: Balancing services deployed in the minutes time frame.
tags:
  - frequency-control
  - generation
  - nerc
related:
  - fast-frequency-response
  - primary-control
  - tertiary-control
  - frequency-regulation
  - automatic-generation-control
  - frequency-stability
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.0
date: 2025-03-15
lastmod: 2025-06-22
generated: 2025-12-02
---

### Definition by NERC

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/frequency_trend.png"
        zoomable=true %}
        Typical Frequency Trend for the Loss of a Generating Resource (from <d-cite key="nerc2021balancing"></d-cite>).
    </div>
</div>

<br>

Source: <d-cite key="nerc2021balancing"></d-cite>

> Typically includes the balancing services deployed in the “minutes” time frame. Some resources, such as hydroelectric generation, can respond faster in many cases.
> This control is accomplished using the Balancing Authority’s control computer (terms most often associated with this are **“Load-Frequency Control”** or [**“Automatic Generation Control”**](/wiki/automatic-generation-control/)) and the manual actions taken by the dispatcher to provide additional adjustments. Secondary Control also includes initial reserve deployment for disturbances.
>
> In short, Secondary Control maintains the minute-to-minute balance throughout the day and is used to restore frequency to its scheduled value, usually 60 Hz, following a disturbance.
> Secondary Control is provided by both [**Spinning**](/wiki/spinning-reserve) and [**Non-Spinning Reserves**](/wiki/non-spinning-reserve).
