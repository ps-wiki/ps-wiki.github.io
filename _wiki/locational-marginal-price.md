---
layout: distill
title: Localtional Marginal Price
description: LMP. Marginal price for energy at the location delivered or received.
tags: dispatch, economics, operation, PJM, ISO
category: wiki
bibliography: papers.bib
---

**Locational Marginal Price** (LMP) <d-cite key="pjm2024m11"></d-cite> (p20, Revision 133)

Locational Marginal Price (LMP) is defined as the marginal price for energy at the location where the energy is delivered or received and is based on forecasted system conditions and the latest approved Real-time security constrained economic dispatch program solution.
LMP is expressed in dollars per megawatt-hour ($/MWh).
LMP is a pricing approach that addresses Transmission System congestion and loss costs, as well as energy costs.
Therefore, each spot market energy customer pays an energy price that includes the full marginal cost of delivering
an increment of energy to the purchaser’s location.

- When there is transmission congestion in PJM, the PJM dispatcher dispatches one or more of the generating units out of economic merit order to keep transmission flows within limits. There may be many resources that are dispatched to relieve the congestion. The LMP reflects the cost of re-dispatch for out-of-merit resources and cost of delivering energy to that location.
- LMPs are calculated at all injections, withdrawals, EHVs (nominal voltage of 500 KV and above), Interfaces, and various aggregations of these points.
- LMPs are calculated in both the Real-time Energy Market and Day-ahead Energy Market.
  - The Day-ahead LMP is calculated based on the security-constrained economic dispatch for the Day-ahead Market as described in Section 5.2.6 of this Manual.
  - The Real-time LMP is calculated based on the approved security constrained economic dispatch solution for the target dispatch interval as described in Section 2.7 of this Manual.
- The LMP calculation determines the full marginal cost of serving an increment of load at each bus from each resource associated with an eligible energy offer as the sum of three (3) separate components of LMP.
  In performing this LMP calculation, the cost of serving an increment of load at each bus from each resource associated with an eligible energy offer is calculated as the sum of the following three components of Locational Marginal Price: - System Energy Price – This is the price at which the Market Seller has offered to supply an additional increment of energy from a generation resource or decrease an increment of energy being consumed by a Demand Resource. The System Energy Price may include a portion of the defined reserve penalty factors should a reserve shortage exist. - Congestion Price – This is the effect on transmission congestion costs (whether positive or negative) associated with increasing the output of a generation resource or decreasing the consumption by a Demand Resource, based on the effect of increased generation from or consumption by the resource on transmission line loadings. As further described in Section 2.17 of this Manual, the Congestion Price is set to the specified transmission constraint penalty factor in the event a transmission constraint cannot be controlled below the penalty factor value. The Congestion Price may include a portion of the defined reserve penalty factors should a reserve shortage exist. - Loss Price – This is the effect on transmission loss costs (whether positive or negative) associated with increasing the output of a generation resource or decreasing the consumption by a Demand Resource, based on the effect of increased generation from or consumption by the resource on transmission losses.
- The energy offer or offers that can serve an additional increment of load at a bus at the lowest cost, calculated in this manner, shall determine the Locational Marginal Price at that bus.
