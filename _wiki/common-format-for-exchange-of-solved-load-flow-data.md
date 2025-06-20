---
layout: distill
title: Common Format for Exchange of Solved Load Flow Data
description: A.k.a. common data format (CDF)
tags: data-format
bibliography: papers.bib
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-06-17
last_update: 2025-06-19
---

### Definition in an IEEE Standard

Source: <d-cite key="ieee1973loadflow"></d-cite>

> Also referred as common data format (CDF). This format is presently being used throughout most of the eastern and north central United States and parts of Canada. By publishing through the national organization, it is intended that a common reference be established and maintained for those who wish to use the format. The paper presents a detailed description of the format as well as procedures for making revisions and additions.

<!-- prettier-ignore-start -->

> A clarification on the word "presently": this format was used around the 1970s rather than today.
{: .block-warning }

<!-- prettier-ignore-end -->

A matpower function to convert an IEEE CDF data file into a MATPOWER case struct is available at <https://matpower.org/doc/ref-manual/legacy/functions/cdf2mpc.html#cdf2mpc>
