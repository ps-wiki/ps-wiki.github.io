---
layout: distill
title: Resource Scheduling & Commitment
description: RSC
tags: PJM
category: wiki
bibliography: papers.bib
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
last_update: 2025-06-19
---

### Definition by PJM

Source: <d-cite key="pjm2024m11"></d-cite> p143, Revision 134

> The PJM Energy Market Technical Software is a set of computer programs, which performs a security-constrained resource commitment and economic dispatch for the Day-ahead Market. The individual programs are:
>
> - Resource Scheduling & Commitment (RSC) – RSC performs **security-constrained resource commitment** based on generation offers, Demand Resource offers, demand bids, Day-ahead Reserve offers, increment offers, decrement bids and transaction schedules submitted by participants and based on PJM RTO reliability requirements. RSC enforces physical resource specific constraints that are specified in the generation offer data and generic transmission constraints that are entered by the Market Operator. RSC provides an optimized economic resource **commitment schedule** for the next forty-eight (48) hours and it utilizes a mixed integer linear programming solver to create an initial resource dispatch for the next Operating Day.
> - Scheduling, Pricing and Dispatch (SPD) — Performs security-constrained economic dispatch using the commitment profile produced by RSC. SPD calculates hourly unit generation MW levels and LMPs for all load and generation buses for each hour of the next operating day.
> - Study Network Analysis (STNET) — Creates a powerflow model for each hour of the next operating day based on the scheduled network topology, the generation and demand MW profile produced by SPD and the scheduled Tie Flow with adjacent Balancing Authorities. STNET performs AC contingency analysis using the contingency list from PJM EMS and creates generic constraints based on any violations that are detected.
