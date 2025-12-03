---
title: Stability
description: The ability to maintain equilibrium during normal and abnormal conditions.
tags:
  - stability
  - nerc
  - ieee
  - ieee-task-force
  - cigre
  - article
  - book
  - control-theory
related:
  - security
  - reliability
  - transient-stability
  - dynamic-stability
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
version: 1.0.2
date: 2025-03-15
lastmod: 2025-12-02
generated: 2025-12-02
---

### Revised Definition in an Article by a Task Force

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/power-system-time-scales.png"
        zoomable=true %}
        Fig. 1. Power system times scales. (from <d-cite key="hatziargyriou2020stabilityreport"></d-cite>)
    </div>
</div>

<br>

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/classification-of-power-system-stability.png"
        zoomable=true %}
        Fig. 4. Classification of power system stability (from <d-cite key="hatziargyriou2020stabilityreport"></d-cite>)
    </div>
</div>

<br>

Source: <d-cite key="hatziargyriou2021stability"></d-cite>

> Stability is the ability of an electric power system, for a given initial operating condition, to regain a state of operating equilibrium after being subjected to a physical disturbance, with most system variables bounded so that practically the entire system remains intact.

### Definition by NERC

Source: <d-cite key="nerc2024glossary"></d-cite>

> The ability of an electric system to maintain a state of equilibrium during normal and abnormal conditions or disturbances.

### Definition in an Article by a Joint Task Force of IEEE and CIGRE

Source: <d-cite key="kundur2004stability"></d-cite>

> Stability of a power system refers to the continuance of intact operation following a disturbance. It depends on the operating condition and the nature of the physical disturbance.

### Elaboration in an Article by a Joint Task Force of IEEE and CIGRE

Source: <d-cite key="kundur2004stability"></d-cite>

> Relationships between Reliability, Security, and Stability
>
> 1. Reliability is the overall objective in power system design and operation. To be **reliable**, the power system must be **secure** most of the time. To be **secure**, the system must be **stable** but must also be secure against other contingencies that would not be classified as stability problems e.g., damage to equipment such as an explosive failure of a cable, fall of transmission towers due to ice loading or sabotage. As well, a system may be stable following a contingency, yet insecure due to post-fault system conditions resulting in equipment overloads or voltage violations.
> 2. System security may be further distinguished from stability in terms of the **resulting consequences**. For example, two systems may both be stable with equal stability margins, but one may be relatively more secure because the consequences of instability are less severe.
> 3. Security and stability are time-varying attributes which can be judged by studying the performance of the power system under a particular set of conditions. Reliability, on the other hand, is a function of the time-average performance of the power system &nbsp; it can only be judged by consideration of the system’s behavior over an appreciable period of time.

### Definition in a Book

Source: <d-cite key="slotine1990appliednonlinear"></d-cite> p48

> The equilibrium state $x = 0$ is said to be <u>stable</u> if, for any $R>0$, there exists $r>0$, such that if $\|\|x(0)\|\| < r$, then $\|\|x(t)\|\| <R$ for all $t>0$. Otherwise, the equilibrium point is <u>unstable</u>.

> Essentially, stability (also called stability in the sense of Lyapunov, or Lyapunov stability) means that the system trajectory can be kept arbitrarily close to the origin by starting sufficiently close to it. More formally, the definition states that the origin is stable, if, given that we do not want the state trajectory $x(t)$ to get out of a ball of arbitrarily specified radius $\textbf{B}_R$ , a value $r(R)$ can be found such that starting the state from within the ball $\textbf{B}_r$ at time 0 guarantees that the state will stay within the ball $\textbf{B}_r$ thereafter.
