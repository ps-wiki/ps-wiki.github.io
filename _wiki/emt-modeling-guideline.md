---
title: EMT Modeling Guideline
description: ISO/RTO/TSO guidelines on EMT modeling.
tags:
  - transmission
  - system-operator
  - EMT
  - nyiso
related: []
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.0
date: 2025-11-19
lastmod: 2025-11-19
generated: 2025-11-26
---

### Definition by NYISO

Source: <d-cite key="nyiso2025emtguideline"></d-cite> p7

> **4.7 EMT Model Response Must Align With Positive Sequence Phasor Domain (PSPD) Model**
>
> The behavior of the EMT model and the PSPD model used to represent the plant/equipment is expected to be in close alignment and will be verified by the NYISO. The models are used to represent the same plant and therefore should behave in a similar fashion. Selected tests in Section 7 will be used to verify alignment between the EMT model and the PSPD model. The NYISO and the model submitter must use the same PSPD model for the asset for this comparison. The NYISO will use the latest PSPD model submitted for the facility in this verification. As such, PSPD models do not need to be re-submitted at this stage.
>
> Differences that arise from increased modeling bandwidth in EMT domain are known to exist and will be allowed, as long as they can be justified. Differences in model response trends, post-transient steady state settling values, or any behavior in a timeframe that can be accurately captured by PSPD models with typical integration time steps used in those simulations (1-4ms) are not allowed and any discrepancies will require further explanation.
>
> All EMT and PSPD channels delivered must be overlayed (in the same plot) for each channel type (i.e., active power, reactive power, voltage, etc.). A qualitative criterion will be used to determine if the models are in good alignment and no quantitative criterion (e.g., signal envelopes, peak values, etc.) will be employed at this time
