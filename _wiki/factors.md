---
layout: distill
title: Factors
description: System sensitivity matrices, such as GSF, PTDF, LODF, BODF, OTDF, etc.
tags: sensitivity
category: wiki
bibliography: papers.bib
---

**Participation Factors** <d-cite key="nerc2024glossary"></d-cite>

A set of dispatch rules such that given a specific amount of load to serve, an **approximate generation** dispatch can be determined.
To accomplish this, generators are assigned a percentage that they will contribute to serve load.

**Generator Shift Factor** (GSF) <d-cite key="nerc2024glossary"></d-cite>

A factor to be applied to a generator’s expected change in output to determine the amount of flow contribution that change in output will impose on an identified transmission facility or [Flowgate](/wiki/flowgate).

**Power Transfer Distribution Factor** (PTDF) by NERC <d-cite key="nerc2024glossary"></d-cite>

In the pre-contingency configuration of a system under study, a measure of the responsiveness or change in electrical loadings on transmission system Facilities due to a change in electric power transfer from one area to another, expressed in percent (up to 100%) of the change in power transfer.

**Power Transfer Distribution Factors** (PTDF) by PowerWorld <d-cite key="powerworld2025manual"></d-cite> (Sensitivities -> Power Transfer Distribution Factors -> Power Transfer Distribution Factors)

Power Transfer Distribution Factors indicate the **incremental change** in real power that occurs on transmission lines due to real power transfers between two regions.
These regions can be defined by areas, zones, super areas, single buses, injection groups or the system slack.
These values provide a **linearized approximation** of how the flow on the transmission lines and interfaces change in response to a transaction between the Seller (source) and the Buyer (sink).
These values can then be visualized on the onelines using animated flows.

**Line Outage Distribution Factors** (LODFs) by PowerWorld <d-cite key="powerworld2025manual"></d-cite> by PowerWorld Sensitivities > Line Outage Distribution Factors > Line Outage Distribution Factors (LODFs)

Line Outage Distribution Factors (LODFs) are a sensitivity measure of how a change in a line’s status affects the flows on other lines in the system.
On an energized line, the LODF calculation determines the percentage of the present line flow that will show up on other transmission lines after the outage of the line. For example, consider an energized line, called LineX, whose present MW flow is 100 MW.
If the LODFs are found to be

LODFs for LineX outage

LineX -100%

LineY + 10%

LineZ - 30%

This means that after the outage of LineX, the flow on LineX will decrease by 100 MW (of course), LineY will increase by 10 MW, and LineZ will decrease by 30 MW.
The "flow on Line X" here means the flow at the from bus going toward the to bus.

Similarly, sensitivities can be calculated for the insertion of a presently open line.
In this case, the LODF determines the percentage of the post-insertion line flow that will come from the other transmission line after the insertion.
The "LODF" is better named a Line Closure Distribution Factor (LCDF) in this case.

_Jinning's Note: LODF is a.k.a. Branch Outage Distribution Factor (BODF) in some references._

**Outage Transfer Distribution Factor** (OTDF) by NERC <d-cite key="nerc2024glossary"></d-cite>

In the post-contingency configuration of a system under study, the electric Power Transfer Distribution Factor (PTDF) with one or more system Facilities removed from service (outaged).

**Outage Transfer Distribution Factors** (OTDF) by PowerWorld <d-cite key="powerworld2025manual"></d-cite> (Sensitivities > Line Outage Distribution Factors > Line Outage Distribution Factors (LODFs))

An OTDF is similar to PTDF, except an OTDF provides a linearized approximation of the **post-outage change** in flow on a transmission line in response to a transaction between the Seller and the Buyer.
The OTDF value is a function of PTDF values and LODF values.
For a single line outage, the OTDF value for line x during the outage of line y is

OTDFx = PTDFx + LODFx,y \* PTDFy

where PTDFx and PTDFy are the PTDFs for line x and y respectively, and LODFx,y is the LODF for line x during the outage of line y.

**Participation factor** regarding small-signal stability <d-cite key="kundur1994Power"></d-cite> (p716-717, first edition)

One problem in using right and left eigenvectors individually for identifying the relationship between the states and the modes is that the elements of the eigenvectors are dependent on units and scaling associated with the state variables.
As a solution to this problem, a matrix called the **participation matrix** ($P$), which combines the right and left eigenvectors as follows is proposed in reference 2 as a measure of the association between the state variables and the modes.

$$ P = [ P_1 \quad P_2 \quad \dots \quad P_n ] $$ (12.49A)

with

$$
P_i =
\begin{bmatrix}
p_{1i} \\
p_{2i} \\
\vdots \\
p_{ni}
\end{bmatrix}
=
\begin{bmatrix}
\phi_{1i} \psi_{i1} \\
\phi_{2i} \psi_{i2} \\
\vdots \\
\phi_{ni} \psi_{in}
\end{bmatrix}
$$ (12.49B)

where

$\phi_{ki}$ = the element on the $k$th row and $i$th column of the modal matrix $\Phi$
<br>= $k$th entry of the right eigenvector $\Phi_i$

$\psi_{ik}$ = the element on the $i$th row and $k$th column of the modal matrix $\Psi$
<br>= $k$th entry of the left eigenvector $\Psi_i$

The element $p_{ki} = \phi_{ki} \psi_{ik}$ is termed the **participation factor**.
It is a measure of the relative participation of the $k$th state variable in the $i$th mode, and vice versa.

Since $\phi_{ki}$ measures the **activity** of $x_k$ in the $i$th mode and $\psi_{ik}$ weighs the contribution of this activity to the mode, the product $p_{ki}$ measures the **net participation**.
The effect of multiplying the elements of the left and right eigenvectors is also to make $p_{ki}$ dimensionless (i.e., independent of the choice of units).

In view of the eigenvector normalization, the sum of the participation factors associated with any mode $\sum_{i=1}^{n} p_{ki}$ or with any state variable $\sum_{k=1}^{n} p_{ki}$ is equal to 1.

From Equation 12.48, we see that the participation factor $p_{ki}$ is actually equal to the sensitivity of the eigenvalue $\lambda_i$ to the diagonal element $a_{kk}$ of the state matrix $A$:

$$ p_{ki} = \frac{\partial \lambda_i}{\partial a_{kk}} $$ (12.50)

As we will see in a number of examples in this chapter, the **participation factors are generally indicative of the relative participations** of the respective states in the corresponding modes.
$$
