---
layout: distill
title: Real-Time Reliability Model
description: A computer representation of the power system facilities.
tags: reliability, transmission-operation, PJM, ISO
category: wiki
bibliography: papers.bib
---

**Real-Time Reliability Model** <d-cite key="pjm2024m3"></d-cite> (p17, Revision 67)

PJM's Real-Time Reliability Model is a computer representation of the power system facilities in the PJM RTO and other Balancing Authorities that may impact the reliable operation of the PJM system.
The model resides and is maintained by the PJM staff on the PJM Energy Management System (EMS).
The PJM EMS Network Application programs utilize the model to continuously calculate the **real-time state** and determine the **security** of the PJM system.
The **Security Constrained Economic Dispatch (SCED)** dispatches every generator in the model.
The model is also used to calculate real-time Locational Marginal Prices.
The model is created and maintained from input data received by PJM from various sources including Transmission Owners, Generation Owners, Load Serving Entities, and other Balancing Authorities.
The model is only as accurate as the input data used to derive it; therefore, timely and accurate data updates are critical.
