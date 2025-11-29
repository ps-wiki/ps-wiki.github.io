---
title: Short-Circuit Ratio with Interaction Factors
description: SCRIF. The ratio between short circuit apparent power from a 3LG fault at a given location in the power system to the rating of the location.
tags:
  - reliability
  - nerc
related:
  - grid-strength
  - reliability
  - short-circuit-ratio
  - weighted-short-circuit-ratio
  - composite-short-circuit-ratio
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.0
date: 2025-11-29
lastmod: 2025-11-29
generated: 2025-11-29
---

### Definition by NERC

Source: <d-cite key="nerc2017integrating"></d-cite> p3

> SCR with Interaction Factors (SCRIF) has been proposed to capture the change in bus voltage at one bus corresponding resulting from a change in bus voltage at another bus. Electrically close inverter-based resource buses will have a relatively higher Interaction Factor (IF) than inverter-based resource buses that are electrically separated. When multiple inverter-based resources are located very close to each other, they share the grid strength and short circuit level; hence, the grid strength is actually much lower than the overall short circuit level calculated at that bus or buses. SCRIF captures the voltage sensitivity between inverter-based resources as a screening tool for potential controls issues by using inverter-based resource interaction factors, as follows:
>
> $ SCRIF_{i} = \frac{S_{i}}{P_{i} + \sum_{j} (IF_{ji} \cdot P_{j})} $
>
> Where $IF$ is the change in bus voltage at bus $i$ ($\Delta V_{i}$) for a change in bus voltage at bus $j$ ($\Delta V_{j}$), as follows:
>
> $ IF_{ij} = \frac{\Delta V_{i}}{\Delta V_{j}} $
>
> An advantage of the use of SCRIF is that it can be readily amended to cater for any conceivable configuration for connection of multiple inverter-based resources.
