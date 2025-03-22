---
layout: distill
title: Energy Market
description:
tags: PJM
category: wiki
bibliography: papers.bib
---

Relevante items: [Security Constrained Unit Commitment](/wiki/security-constrained-unit-commitment) &nbsp; [Security Constrained Economic Dispatch](/wiki/security-constrained-economic-dispatch) &nbsp; [Locational Marginal Price](/wiki/locational-marginal-price)

**PJM Energy Markets** <d-cite key="pjm2024m11"></d-cite> (p17, Revision 133)

The PJM Energy Markets consists of two markets, a Day-ahead Market and a Real-time Balancing Market.
In general, both markets follow a two-step process to perform dispatch and pricing of the system.
First, security-constrained economic dispatch of the system is performed, referred to as the dispatch run.
Second, the calculation of Locational Marginal Prices is performed separately and subsequent to the dispatch run, referred to as the pricing run.
The objective of both the dispatch run and the pricing run is to serve load and meet reserve requirements at the least cost while evaluating the same transmission constraints.

In the pricing run, however, Integer Relaxation is performed to allow Eligible Fast-Start Resources that are online in the dispatch run, to set price as well as to incorporate their associated commitment costs.
Integer Relaxation allows Eligible Fast-Start Resources that generally do not have wide dispatchable ranges to be fully dispatchable between zero and their Economic Maximum.
Resources cannot be committed in the pricing run if they were not committed in the dispatch run.
This in turn allows the optimization problem in the pricing run to use a fraction of a committed Eligible Fast-Start Resource’s output, including an amount less than the resource’s offered economic minimum output, in the determination of Locational Marginal Prices.
