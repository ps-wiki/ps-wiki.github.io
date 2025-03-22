---
layout: distill
title: Security Constraiend Economic Dispatch
description: SCED. Allocation of generating units for economical production.
tags: dispatch, economics, operation, PJM, ISO
category: wiki
bibliography: papers.bib
---

Relevante items: [Security Constrained Unit Commitment](/wiki/security-constrained-unit-commitment) &nbsp; [Locational Marginal Price](/wiki/locational-marginal-price)

**Economic Dispatch** <d-cite key="nerc2024glossary"></d-cite>

The allocation of demand to individual generating units on line to effect the most economical production of electricity.

**Security Constrained Economic Dispatch** (SCED) by PJM <d-cite key="pjm2024m3"></d-cite> (p17, Revision 67)

PJM's Real-Time Reliability Model is a computer representation of the power system facilities in the PJM RTO and other Balancing Authorities that may impact the reliable operation of the PJM system.
The model resides and is maintained by the PJM staff on the PJM Energy Management System (EMS).
The PJM EMS Network Application programs utilize the model to continuously calculate the real-time state and determine the security of the PJM system.
The <u>Security Constrained Economic Dispatch</u> (SCED) dispatches every generator in the model.
The model is also used to calculate real-time Locational Marginal Prices.
The model is created and maintained from input data received by PJM from various sources including Transmission Owners, Generation Owners, Load Serving Entities, and other Balancing Authorities.
The model is only as accurate as the input data used to derive it; therefore, timely and accurate data updates are critical.

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
