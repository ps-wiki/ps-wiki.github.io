---
title: Quasi-Static Simulation
description: A sequence of power flow analysis.
tags:
  - simulation
  - ieee
  - article
  - book
related: []
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.1
date: 2025-11-30
lastmod: 2025-11-30
generated: 2025-12-02
---

### Definition in an IEEE Standard

Source: <d-cite key="ieee2014std1547"></d-cite> p77

> Quasi-static simulation refers to a sequence of steady-state power flow conducted at a time step of no less than 1 second but that can use a time step of up to one hour. Discrete controls, such as capacitor switch controllers, transformer tap changers, automatic switches, and relays may change their state from one step to the next. However, there is no numerical integration of differential equations between time steps. A simple quasi-static simulator can be implemented with existing power flow or short-circuit programs under supervisory control. Open-source quasi-static simulators are also available.

### Definition in a Presentation

Source: <d-cite key="reno2017qsts"></d-cite>

> QSTS (Quasi-Static Time Series) solves a series of sequential steady-state power-flow solutions where the converged state of each iteration is used as the beginning state of the next. This caprtures time-varying parameters such as load, and the time-dependent states in the system such as regulator tap positions.

### Definition in a Book

Source: <d-cite key="milano2010power"></d-cite> p213

> In some applications, the variations of the inputs are relatively slow with respect to transient dynamics. A relevant example is the study of the eﬀect of long term voltage stability phenomena, such as the daily load ramp or voltage collapse. In this case load powers are modelled as time dependent controllable parameters $\eta(t)$. Since load variations take from tens of minutes to some hours, any transient dynamic can be considered steady-state. The resulting system equations are obtained by imposing $\dot{x} = 0$ in (8.12):
>
> $0= f(x, y, \eta(t))$
>
> $0= g(x, y, \eta(t))$
>
> which is generally referred to as quasi-static or quasi-steady-state model.
