---
title: Composite Short-Circuit Ratio
description: CSCR. The equivalent system impedance seen by multiple inverter-based resources by creating a common medium voltage bus and tying all inverter-based resources of interest together at that common bus.
tags:
  - stability
  - nerc
related:
  - grid-strength
  - stability
  - short-circuit-ratio
  - weighted-short-circuit-ratio
  - short-circuit-ratio-with-interaction-factors
  - generalized-short-circuit-ratio
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.0
date: 2025-11-29
lastmod: 2025-11-29
generated: 2025-11-29
---

### Definition in an Article

Source: <d-cite key="nerc2017integrating"></d-cite> p2

> Composite short circuit ratio (CSCR) estimates the equivalent system impedance seen by multiple inverter-based resources by creating a common medium voltage bus and tying all inverter-based resources of interest together at that common bus. The composite short circuit MVA at the common bus without current contribution from the inverter-based resources, $CSC_{MVA}$, is then calculated. CSCR can then be calculated as
>
> $ CSCR = \frac{CSC_{MVA}}{MW_{VER}} $
>
> where $MW_{VER}$ is the sum of the nominal power rating of all inverter-based resources considered. This method calculates an aggregate SCR for multiple inverter-based resources, rather than each resource like the conventional SCR approach.
