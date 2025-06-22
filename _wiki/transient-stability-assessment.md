---
title: Transient Stability Assessment
description: TSA. Monitor and determine transient stability of the system.
tags:
  - stability
  - software
  - system-operator
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
last_update: 2025-06-20
---

### Definition by PJM

Source: <d-cite key="pjm2024m3"></d-cite> p61, Revision 67

> In addition to the special operating procedures addressing stability limit issues in Manual-03B, PJM utilizes a real-time Transient Stability Assessment (TSA) tool.
> TSA can monitor and determine transient stability of the system subject to **a select set of EMS contingencies** for balanced and unbalanced faults.
> PJM models a select set of three-phase faults with normal clearing and single-phase faults with delayed clearing.
> The contingencies or faults are in alignment with most planning events as defined in TPL-001-4 categories P1 through P4.
>
> TSA will also monitor and control for dynamic stability using a 3% damping criteria for the RTO.
> TSA will display contingencies and impacted generators not meeting 3% damping criteria for units 10 MVA or above, as simulated between 10 and 15 seconds.
> PJM will perform additional simulations to validate damping results not meeting criteria in Real-time.
>
> TSA is also utilized to assess transient voltage response.
> The transient voltage criteria is recovery to a minimum of 0.7 p.u after 2.5 seconds (0.7 p.u. of nominal voltage).
> Refer to Manual-37: Reliability Coordination for additional information.
> The typical controlling actions for transient voltage exceedance are switching of static reactive devices, such as capacitor and reactors, to maintain a strong pre-contingency voltage profile and reserving dynamic reactive output from SVCs, STATCOMs, and generators, for post-contingency voltage support.
>
> TSA computes stability limits by using real time network models.
> It **interfaces** with the [EMS](/wiki/real-time-reliability-model) and uses the State Estimation solution.
> Other input data includes the dynamic model for over 3000 generators and fault clearing times for specific equipment.
> For equipment without a specific fault clearing time, TSA will use zonal default clearing times.
> TSA also calculates and provides recommended stability control measures to prevent generator instability.
> Typically, the **control measure is expressed in terms of generator-specific MW adjustment**.
> In some cases, a Mvar adjustment may resolve a stability issue.
>
> TSA is used to monitor and control the generators with known stability concerns as defined in PJM Manual-03B.
> Since TSA uses real-time system conditions to assess stability, the limits tend to be less conservative or less restrictive than the manual operational procedures.
> The operational procedure limits are usually determined using conservative assumptions in order to cover a wider range of operating conditions.
> For scheduled transmission outages, TSA studies are used to determine the stability limits.
> For forced outages, the Manual-03B operational procedure limits are used until a real-time TSA run is completed.
> PJM will also use the Manual-03B operational procedure stability limits in certain cases, such as when TSA is down.
