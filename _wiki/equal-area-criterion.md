---
layout: distill
title: Equal Area Criterion
description: EAC and an extended EAC. A method to determine the stability.
tags: transient-stability
category: wiki
bibliography: papers.bib
---

**Equal Area Criterion** (EAC) <d-cite key="kundur1994Power"></d-cite> (p831-833, first edition)

The equal-area criterion is useful in determining the maximum permissible increase in $P_{m}$ for the system illustrated in Figure 13.14.
Stability is maintained only if an area $A_{2}$ at least equal to $A_{1}$ can be located above $P_{m}$. If $A_{1} > A_{2}$, then the rotor angle $\delta$ will exceed its critical value, and stability will be lost. For $\delta > \delta_{\max}$, $P_{m}$ exceeds $P_{e}$, leading to net acceleration rather than deceleration.

_Jinning's Note: another early reference to the Equal Area Criterion can be found in <d-cite key="dahl1935stability"></d-cite>._

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/response-to-a-step-change-in-mechanical-power-input.png"
        zoomable=false %}
        Fig. 13.14 Response to a step change in mechanical power input (from <d-cite key="kundur1994Power"></d-cite>)
    </div>
</div>
<br>
**Extended Equal Area Criterion** (EEAC) <d-cite key="xue1988eeca"></d-cite>

Compared to EAC, EEAC uses an approximate one-machine-infinite-bus (OMIB) equivalent of the multi-machine system.

_Jinning's Note: OMIB is a.k.a. single machine infinite bus (SIMB). The term "Extended Equal Area Criterion" comes from the authors' response to a discussion on the paper:_

Y. Xue, Th. Van Cutsem, and M. Ribbens-Pavella: We are thankful to the discussers for their valuable and constructive comments.
In order to answer their questions in detail, it is useful to first clarify some aspects of our method to which we henceforth refer to as the **“Extended Equal Area Criterion”** (EEAC).
The EEAC essentially pursues two objectives:
i) Devise an ultrafast technique to assess transient stability (in terms of CCT’s or margins as appropriate); this goal was met in this paper.
ii) Provide analytical means of sensitivity analysis and control; initiated here, this study is developed in Ref. [A].
To reach these objectives, the EEAC method has called upon one conjecture and one simplifying assumption.
It is worth restating them and examining their implications in some detail.
