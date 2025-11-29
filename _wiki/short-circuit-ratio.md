---
title: Short-Circuit Ratio
description: SCR. The ratio between short circuit apparent power from a 3LG fault at a given location in the power system to the rating of the location.
tags:
  - stability
  - nerc
related:
  - grid-strength
  - stability
  - weighted-short-circuit-ratio
  - composite-short-circuit-ratio
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

### Definition by NERC

Source: <d-cite key="nerc2017integrating"></d-cite> p1

> SCR is defined as the ratio between short circuit apparent power (SCMVA) from a 3LG fault at a given location in the power system to the rating of the inverter-based resource connected to that location. Since the numerator of the SCR metric is dependent on the specific measurement location, this location is usually stated along with the SCR number.
>
> $ SCR_{POI} = \frac{SCMVA_{POI}}{MW_{VER}} $
>
> Where $SCMVA_{POI}$ is the short circuit MVA level at the POI without the current contribution of the inverter-based resource, and $MW_{VER}$ is the nominal power rating of the inverter-based resource being connected at the POI.
