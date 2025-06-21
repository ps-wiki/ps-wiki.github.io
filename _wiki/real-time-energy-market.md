---
layout: distill
title: Real Time Energy Market
description: Use dispatch run to determine the least cost solution to balance supply and demand.
tags:
  - system-operator
  - market
bibliography: papers.bib
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
last_update: 2025-06-20
---

Relevante items: [Security Constrained Unit Commitment](/wiki/security-constrained-unit-commitment) &nbsp; [Security Constrained Economic Dispatch](/wiki/security-constrained-economic-dispatch) &nbsp; [Locational Marginal Price](/wiki/locational-marginal-price) &nbsp; [Energy Market](/wiki/energy-market)

### Definition by PJM

Source: <d-cite key="pjm2024m11"></d-cite> p19, Revision 133

> The Real-time Energy Market uses the Real-time Security Constrained Economic Dispatch (RT SCED) program, known as the dispatch run, to determine the least cost solution to balance supply and demand.
> The dispatch run considers resource offers, forecasted system conditions, and other inputs in its calculations.
> For more information regarding the RT SCED program, please refer to Section 2.5 of this Manual.
> Generators and Demand Resources may alter their bids for use in the Real-time Energy Market as defined in Section 9.1 of this Manual during the following periods:
>
> - During the Generation Rebidding Period which is defined from the time PJM posts the results of the Day-ahead Energy Market until 14:15.
> - Starting at 18:30 (typically after the Reliability Assessment and Commitment (RAC) Run is completed) and up to sixty-five (65) minutes prior to the start of the operating hour.
>
> Real-time LMPs and Regulation and Reserve Clearing Prices are calculated every five (5) minutes by the Locational Price Calculator (LPC) program, in a process referred to as the pricing run, and are based on forecasted system conditions and the latest approved RT SCED program solution.
> For more information regarding LPC, Real-time LMPs and Regulation and Reserve Clearing Prices, refer to Section 2.7 of this Manual.
> The balancing settlement is calculated for each Real-time Settlement Interval (five (5) minute interval) based on actual five (5) minute Revenue Data for Settlement MW quantity deviations from Day-ahead scheduled quantities resulting from the dispatch run and on the applicable Real-time prices resulting from the pricing run.
