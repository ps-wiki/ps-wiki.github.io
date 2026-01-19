---
title: Storm Resilience Metric
description: Focused on the speed of system recovery during storm events.
tags:
  - resilience
  - metrics
  - ieee
related:
  - resilience
  - performance-based-metrics
  - non-storm-resilience-metric
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.1
date: 2025-03-15
lastmod: 2025-11-03
generated: 2026-01-18
---

### Definition in an IEEE Techical Report

Source: <d-cite key="chiu2020resilience"></d-cite> p12

> This metric focuses on the **speed of system recovery** and is designed to capture the reduction of the number of customers without power for more than 12 hours from the time the customer loses power during a storm event.
> The metric will consider the instances of customer service interruptions that have been restored automatically without requiring human intervention to capture the value of technology solutions such as distribution automation, advanced distribution management system (ADMS), or microgrids, that minimize customer impacts.
> It will measure the number of reportable storms where recovery is favorable to threshold values divided by the total number of reportable storms.
