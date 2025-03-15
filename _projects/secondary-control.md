---
layout: distill
title: Secondary Control
description: Balancing services deployed in the “minutes” time frame.
tags: frequency, generator
importance: 2
category: wiki
bibliography: papers.bib
---

Relevant items: [Fast Frequency Response](/pswiki/fast-frequency-response); [Primary Control](/pswiki/primary-control); [Tertiary Control](/pswiki/tertiary-control); [Frequency Regulation](/pswiki/frequency-regulation); [Automatic Generation Control](/pswiki/automatic-generation-control); [Frequency Stability](/pswiki/frequency-stability)

**Secondary Control** <d-cite key="nerc2021balancing"></d-cite>

Typically includes the balancing services deployed in the “minutes” time frame. Some resources, such as hydroelectric generation, can respond faster in many cases.
This control is accomplished using the Balancing Authority’s control computer (terms most often associated with this are **“Load-Frequency Control”** or [**“Automatic Generation Control”**](/pswiki/automatic-generation-control/)) and the manual actions taken by the dispatcher to provide additional adjustments. Secondary Control also includes initial reserve deployment for disturbances.

In short, Secondary Control maintains the minute-to-minute balance throughout the day and is used to restore frequency to its scheduled value, usually 60 Hz, following a disturbance.
Secondary Control is provided by both [**Spinning**](/pswiki/spinning-reserve) and [**Non-Spinning Reserves**](/pswiki/non-spinning-reserve).

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/frequency_trend.png"
        zoomable=true %}
        Typical Frequency Trend for the Loss of a Generating Resource (from <d-cite key="nerc2021balancing"></d-cite>).
        Point A is defined as the pre-disturbance frequency;
        Point C or Nadir is the maximum deviation due to loss of resource;
        Point B is defined as the stabilizing frequency and;
        Point D is the time the contingent BA begins the recovery from the loss of resource.
    </div>
</div>
