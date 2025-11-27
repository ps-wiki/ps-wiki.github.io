---
title: Security Constrained Unit Commitment
description: SCUC.
tags:
  - system-operator
  - nyiso
related: []
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.0
date: 2025-03-15
lastmod: 2025-06-22
generated: 2025-11-26
---

### Definition by NYISO

Source: <d-cite key="nyiso2024dayahead"></d-cite> p8, Version 8.0

> The SCUC produces the generating unit commitment schedule and Firm Transaction schedules for the next day’s operation. Factors considered by SCUC are:
>
> - Current generating unit operating status
> - Constraints on the minimum up and down time of the generators
> - Generation and start up bid prices
> - Plant-related startup and shutdown constraints
> - Minimum and maximum generation constraints
> - Generation and reserve requirements
> - Transmission facility maintenance schedules
> - Transmission constraints
> - Phase angle regulator settings
> - Transaction bids
> - Minimum and Maximum Energy Level constraints (for Energy Storage Resources (ESR) only)
> - Bid Beginning Energy Level for ESR (for ISO Managed ESR only)
> - Co-located Storage Resources (CSR) Scheduling Limits (Only for solar/wind Intermittent Power Resource (IPR) and ESR Generators that participate in a CSR). Aggregations comprised of ESR, Wind, or Solar only are not eligible to participate in a CSR.
