---
layout: distill
title: Resilience
description: Concepts and its metrics.
tags: resilience, index, IEEE, FERC
category: wiki
bibliography: papers.bib
---

**Resilience** <d-cite key="nerc2018resilience"></d-cite> (p8)

FERC proposed to define resilience as the ability to withstand and reduce the magnitude and/or duration of disruptive events, which includes the capability to anticipate, absorb, adapt to, and/or rapidly recover from such an event.

Some other definitions of resilience <d-cite key="chiu2020resilience"></d-cite> (p8)

- **FERC**: The ability to withstand and reduce the magnitude and/or duration of disruptive events, which includes the capability to anticipate, absorb, adapt to, and/or rapidly recover from such event.
- **DOE**: The ability of a power system and its components to withstand and adapt to disruptions and rapidly recover from them.
- **NATF**: The ability of the system and its components (i.e., both the equipment and human components) to minimize damage and improve recovery from non-routine disruptions, including high impact, low frequency (HILF) events, in a reasonable amount of time.

The IEEE Technical Report PES-TR65 and FERC Docket No. AD18-7-000 defines resilience as “The ability to withstand and reduce the magnitude and/or duration of disruptive events, which includes the capability to anticipate, absorb, adapt to, and/or rapidly recover from such an event.”

**Storm Resilience Metric** by IEEE <d-cite key="chiu2020resilience"></d-cite> (p12)

This metric focuses on the **speed of system recovery** and is designed to capture the reduction of the number of customers without power for more than 12 hours from the time the customer loses power during a storm event.
The metric will consider the instances of customer service interruptions that have been restored automatically without requiring human intervention to capture the value of technology solutions such as distribution automation, advanced distribution management system (ADMS), or microgrids, that minimize customer impacts.
It will measure the number of reportable storms where recovery is favorable to threshold values divided by the total number of reportable storms.

**Non-Storm Resilience Metric** by IEEE <d-cite key="chiu2020resilience"></d-cite> (p13)

This metric focuses on robustness and the ability to withstand events.
It is designed to capture the **total number of gray sky days** (GSD) in a calendar year with no more than the threshold value of customer interruptions.
The metric is **measured in a percentage of GSDs** that does not exceed the threshold value.
The threshold value varies by utility size and is defined as the percentage of customer interruptions over the total customer base (e.g., 0.375% of the total number of customers).
GSD excludes any calendar day with at least one reportable storm-related outage.

**Multi-Criteria Decision Analysis (MCDA)-Based Metrics** by DOE GMLC <d-cite key="chiu2020resilience"></d-cite> (p13)

MCDA metrics generally try to answer the question, “what is the current state of the electric system’s resilience, and what enhances its resilience over time?”
These metrics can be used to assess the system’s baseline resilience relative to other systems.
They typically include categories of system properties beneficial to resilience, such as robustness, resourcefulness, adaptivity, and recoverability.
The application of these metrics requires following a process to review to what degree these properties are present within the system under analysis.
This usually involves collecting data through surveys, developing weighting factors, and performing calculations to obtain numerical scores.
MCDA metrics are used to calculate a resilience index (RI) that accounts for about 1,200 attributes grouped in 350 categories to characterize system resilience.

**Performance-Based Metrics** by DOE GMLC <d-cite key="chiu2020resilience"></d-cite> (p13)

Performance-based metrics (also known as **consequence-based metrics**) are generally quantitative approaches for answering the question, “How resilient is my system?”
These metrics interpret quantitative data that describe infrastructure performance during disruptive events.
The required data can be collected from historical events, subject matter estimates, and computational infrastructure models.
These metrics are suitable for benefit-cost and planning analyses because they measure the potential benefits and costs associated with proposed resilience improvements and investments.
Resilience metrics need to include a measure of consequences and the relevant statistical probability from the probability distribution of those consequences.
