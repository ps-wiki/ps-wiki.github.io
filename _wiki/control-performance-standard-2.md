---
title: Control Performance Standard 2
description: CPS2. A standard intended to limit unscheduled flows.
tags:
  - frequency-control
  - nerc
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
lastmod: 2025-06-20
---

### Definition by NERC

Source: <d-cite key="nerc2015bal001"></d-cite> p22

> Initially, a 10-minute metric called CPS2 was developed to keep average ACE within specific bounds.
> CPS2 was originally used to help prevent excessive transmission flows due to large values of ACE.
> The problem with CPS2 was that it was not dependent on ACE’s impact on frequency.
> Additionally, CPS2 could cause control actions that moved against frequency.
> If a BA had very bad performance in one direction for five minutes, the BA could correct this by having equally bad performance in the opposite direction for the next five minutes.
> Finally, ACE could be totally unbounded for 10% of the month and it didn’t matter whether it was 1 or 1000 MW over the limit.
> CPS2 did not provide the correct signal for maintaining frequency.

### Calculation by NERC

Source: <d-cite key="nerc2015bal0011"></d-cite> p3

$$
CPS2 = \left[ 1 - \frac{\text{Violations}_{\text{month}}}{\text{Total Periods}_{\text{month}} - \text{Unavailable Periods}_{\text{month}}} \right] \times 100
$$
