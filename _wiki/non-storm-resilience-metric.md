---
title: Non-Storm Resilience Metric
description: A metric focuses on robustness and the ability to withstand events.
tags:
  - resilience
  - metrics
  - ieee
related:
  - resilience
  - performance-based-metrics
  - storm-resilience-metric
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.1
date: 2025-03-15
lastmod: 2025-11-03
generated: 2025-11-26
---

### Definition in an IEEE Techical Report

Source: <d-cite key="chiu2020resilience"></d-cite> p13

> This metric focuses on robustness and the ability to withstand events.
> It is designed to capture the **total number of gray sky days** (GSD) in a calendar year with no more than the threshold value of customer interruptions.
> The metric is **measured in a percentage of GSDs** that does not exceed the threshold value.
> The threshold value varies by utility size and is defined as the percentage of customer interruptions over the total customer base (e.g., 0.375% of the total number of customers).
> GSD excludes any calendar day with at least one reportable storm-related outage.
