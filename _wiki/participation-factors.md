---
layout: distill
title: Participation Factors
description: One definition is about dispath and another is about small-signal stability.
tags: sensitivity
category: wiki
bibliography: papers.bib
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
last_update: 2025-06-18
---

### Definition by NERC

Source: <d-cite key="nerc2024glossary"></d-cite>

> A set of dispatch rules such that given a specific amount of load to serve, an **approximate generation** dispatch can be determined. To accomplish this, generators are assigned a percentage that they will contribute to serve load.

### Definition in a Book Regarding Small-Signal Stability

Source: <d-cite key="kundur1994Power"></d-cite> p716-717, first edition

> One problem in using right and left eigenvectors individually for identifying the relationship between the states and the modes is that the elements of the eigenvectors are dependent on units and scaling associated with the state variables. As a solution to this problem, a matrix called the **participation matrix** ($P$), which combines the right and left eigenvectors as follows is proposed in reference 2 as a measure of the association between the state variables and the modes.

More details from the book are excerpted below for reference:

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
