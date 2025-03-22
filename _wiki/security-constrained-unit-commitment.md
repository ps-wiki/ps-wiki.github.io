---
layout: distill
title: Security Constrained Unit Commitment
description: SCUC. Resource Scheduling and Commitment
tags: PJM
category: wiki
bibliography: papers.bib
---

Relevante items: [Security Constrained Economic Dispatch](/wiki/security-constrained-economic-dispatch) &nbsp; [Locational Marginal Price](/wiki/locational-marginal-price)

**Unit Commitment** <d-cite key="pjm2024m14d"></d-cite>

The resource commitment process includes the Markets Database (formerly the Unit Commitment Database or UCDB) and the functions of Hydro Scheduler and the Dispatch Management Tool (DMT).
The Markets Database is a large database containing information on each resource that operates as part of the PJM Interchange Energy Market.
The Resource Scheduling and Commitment (RSC) programs provide an optimized economic commitment schedule for thermal generating units and are the primary tool used to determine commitment of resources that have operating constraints requiring multiple-day operation.
The Hydro Calculator computes hourly reservoir elevations and hydro plant generation from input river flows and hydro plant discharges.

**Resource Scheduling & Commitment** <d-cite key="pjm2024m11"></d-cite> (p143, Revision 133)

The PJM Two-Settlement Technical Software is a set of computer programs performing security-constrained resource commitment and economic dispatch for the Day-Ahead Market.
The individual programs are:

1. Resource Scheduling & Commitment (RSC) – RSC performs **security-constrained resource commitment** based on generation offers, Demand Resource offers, demand bids, Day-ahead Reserve offers, increment offers, decrement bids and transaction schedules submitted by participants and based on PJM RTO reliability requirements.
   RSC enforces physical resource specific constraints that are specified in the generation offer data and generic transmission constraints that are entered by the Market Operator.
   RSC provides an optimized economic resource **commitment schedule** for the next forty-eight (48) hours and it utilizes a mixed integer linear programming solver to create an initial resource dispatch for the next Operating Day.
1. Scheduling, Pricing and Dispatch (SPD) — Performs security-constrained economic dispatch using the commitment profile produced by RSC. SPD calculates hourly unit generation MW levels and LMPs for all load and generation buses for each hour of the next operating day.
1. Study Network Analysis (STNET) — Creates a powerflow model for each hour of the next operating day based on the scheduled network topology, the generation and demand MW profile produced by SPD and the scheduled Tie Flow with adjacent Balancing Authorities.
   STNET performs AC contingency analysis using the contingency list from PJM EMS and creates generic constraints based on any violations that are detected.

**Security Constrained Unit Commitment (SCUC)** by NYISO <d-cite key="nyiso2024dayahead"></d-cite> (p8, Version 8.0)

The SCUC produces the generating unit commitment schedule and Firm Transaction schedules for the next day’s operation.
Factors considered by SCUC are:

- Current generating unit operating status
- Constraints on the minimum up and down time of the generators
- Generation and start up bid prices
- Plant-related startup and shutdown constraints
- Minimum and maximum generation constraints
- Generation and reserve requirements
- Transmission facility maintenance schedules
- Transmission constraints
- Phase angle regulator settings
- Transaction bids
- Minimum and Maximum Energy Level constraints (for Energy Storage Resources (ESR) only)
- Bid Beginning Energy Level for ESR (for ISO Managed ESR only)
- Co-located Storage Resources (CSR) Scheduling Limits (Only for solar/wind Intermittent Power Resource (IPR) and ESR Generators that participate in a CSR). Aggregations comprised of ESR, Wind, or Solar only are not eligible to participate in a CSR.
