---
title: Weighted Short-Circuit Ratio
description: A metric that accounts for interactions between wind plants to better estimate system strength.
tags:
  - stability
related:
  - grid-strength
  - stability
  - short-circuit-ratio
  - composite-short-circuit-ratio
  - short-circuit-ratio-with-interaction-factors
  - generalized-short-circuit-ratio
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-11-29
lastmod: 2025-11-29
---

### Definition in an Article

Source: <d-cite key="zhang2014evaluating"></d-cite>

> To take into account the effect of interactions between wind plants and therefore to give a better estimate of the system strength, a more appropriate quantity is the weighted short circuit ratio (WSCR), defined by:
>
> $ WSCR= \frac{\sum_{i}^{N} S_{SCMVA_i} \cdot P_{RMW_i}}{\left(\sum_{i}^{N} P_{RMW_i}\right)^2} $
>
> Where $S_{SCMVA_i}$ is the short circuit capacity at bus $i$ before the connection of wind plant $i$ and $P_{RMW_i}$ is the MW rating of wind plant $i$ to be connected. $N$ is the number of wind plants fully interacting with each other and $i$ is the wind plant index.
