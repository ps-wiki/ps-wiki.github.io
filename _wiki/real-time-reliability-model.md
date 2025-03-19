---
layout: distill
title: Real-Time Reliability Model
description: EMS. A computer representation of the power system facilities.
tags: reliability, transmission-operation, PJM, ISO
category: wiki
bibliography: papers.bib
---

**Real-Time Reliability Model** by PJM <d-cite key="pjm2024m3"></d-cite> (p17, Revision 67)

PJM's Real-Time Reliability Model is a computer representation of the power system facilities in the PJM RTO and other Balancing Authorities that may impact the reliable operation of the PJM system.
The model resides and is maintained by the PJM staff on the PJM Energy Management System (EMS).
The PJM EMS Network Application programs utilize the model to continuously calculate the **real-time state** and determine the **security** of the PJM system.
The **Security Constrained Economic Dispatch (SCED)** dispatches every generator in the model.
The model is also used to calculate real-time Locational Marginal Prices.
The model is created and maintained from input data received by PJM from various sources including Transmission Owners, Generation Owners, Load Serving Entities, and other Balancing Authorities.
The model is only as accurate as the input data used to derive it; therefore, timely and accurate data updates are critical.

**Real-Time Reliability Model** by PJM <d-cite key="pjm2024m3a"></d-cite> (p12, Revision 25)
PJM’s Real-Time Reliability Model, also known as the EMS model, is a computer representation of the power system facilities in the PJM RTO and other Control Areas that may impact the reliable operation of the PJM system.
The model, maintained by designated PJM support staff, resides on the PJM EMS.
The PJM EMS Transmission Network Application (TNA) programs utilize the model to:
- Calculate the real-time state of the electric system (using a State Estimator (SE)) and
- Assess if the PJM system is operating within relevant, established limits.

The EMS model is adapted for use in the real-time Locational Marginal Price calculator (LMP - see Section 5 of this manual, Data Interfaces). The LMP calculator is interfaced to another program, the Security Constrained Economic Dispatch (SCED) program which models PJM generators. The LMP and SCED programs work together to develop secure, economic operating points for the electric system and to provide Automatic Generation Control (AGC).
These systems use data from various sources including, but not limited to, the EMS.
All the models are created and maintained from input data received by PJM from various sources including TOs, GOs, Load Serving Entities, and other Reliability Coordinators.
