---
layout: distill
title: Economic Dispatch
description: ED. Allocation of generating units for economical production.
tags: dispatch, economics, operation, PJM, ISO
importance: 2
category: wiki
bibliography: papers.bib
---

**Economic Dispatch** <d-cite key="nerc2024glossary"></d-cite>

The allocation of demand to individual generating units on line to effect the most economical production of electricity.

**Security Constraint Economic Dispatch** (SCED) by PJM <d-cite key="pjm2022cooptimization"></d-cite> (p1)

SCED is a mathematical model that generates the most economic resource dispatch during Real-time operations while considering key system operating constraints, such as power balance, reserve requirements, transmission congestion, as well as resource parameters, such as ramp rates, minimum and maximum output capability.
The overall objective function of the SCED algorithm is to minimize the total system product cost over the study interval(s).

The Objective Function include:

1. Resource Energy Costs
2. Price Responsive Demand Value
3. Import Transaction Costs
4. Export Transaction Value
5. Regulation Reserve Costs
6. Synchronized Reserve Costs
7. Non-Synchronized Reserve Costs
8. Secondary Reserve Costs

The Constraints include:

1. Power Balance Constraint
2. Transmission Constraints
3. Resource Capacity Constraints
4. Resource’s Ramp Rate Constraints
5. Reserve Requirement Constraints
