---
layout: distill
title: Control Performance Standard 1
description: CPS1. A standard that measures impact on frequency error
tags: frequency, interconnection
category: wiki
bibliography: papers.bib
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
last_update: 2025-06-17
---

### Definition By NERC <d-cite key="nerc2021balancing"></d-cite> (p29)

- CPS1 assigns each Control Area a share of the responsibility for control of Interconnection frequency.
- CPS1 is a **yearly** (i.e., rolling twelve month) standard that measures impact on frequency error, with a 100 percent minimum allowable score.

### Explanation by NERC <d-cite key="nerc2015bal001background"></d-cite> (p3)

CPS1 is a:

- Statistical measure of ACE variability
- Measure of ACE in combination with the Interconnection’s frequency error
- Based on an equation derived from frequency-based statistical theory

### Calculation by NERC <d-cite key="nerc2015bal001"></d-cite> p5

$$
CPS1 = (2 - CF) * 100\%
$$

**frequency-related compliance factor (CF)**

$$
CF = \frac{CF_{12-month}}{\epsilon1^2}
$$

Where $\epsilon1$ is a constant derived from a targeted frequency bound for each Interconnection:
- *Eastern Interconnection* $\epsilon1 = 0.018~Hz$ 
- *Western Interconnection* $\epsilon1 = 0.0228~Hz$ 
- *ERCOT Interconnection* $\epsilon1 = 0.030~Hz$ 
- *Quebec Interconnection* $\epsilon1 = 0.021~Hz$ 

**Clock-Minute Average of Reporting ACE (RACE)**

$$
RACE_{clock-minute} = \frac{\sum RACE_{sampling~cycles~in~clock-minute}}{n_{sampling~cycles~in~clock-minute}}
$$

**Clock-Minute Average of Frequency Error ($\Delta F$)**

$$
\Delta F_{clock-minute} = \frac{\sum \Delta F_{sampling~cycles~in~clock-minute}}{n_{sampling~cycles~in~clock-minute}}
$$

**Balancing Authority's Clock-Minute Compliance Factor ($CF_{clock-minute}$)**

$$
CF_{clock-minute}=[ (\frac{RACE}{-10B})_{clock-minute} * \Delta F_{clock-minute} ]
$$

**Hourly Average Compliance Factor ($CF_{clock-hour}$)**

$$
CF_{clock-hour}=\frac{\sum CF_{clock-minute}}{n_{clock-minute~samples~in~hour}}
$$

**Monthly Compliance Factor ($CF_{month}$)**

$$
\begin{split}
CF_{month} = \frac{\sum_{days-in-month} \sum_{hours-in-day} [(CF_{clock-hour~average-month}) (n_{one-minute~samples~in~clock-hour~averages})]}{
\sum_{days-in-month} \sum_{hours-in-day} [n_{one-minute~samples~in~clock-hour~averages}]}
\end{split}
$$

**12-Month Compliance Factor ($CF_{12-month}$)**

$$
CF_{12-month} = \frac{\sum_{i=1}^{12} [(CF_{month})_i (n_{one-minute~samples~in~month})_i]}{\sum_{i=1}^{12} (n_{one-minute~samples~in~month})_i}
$$

> To ensure that the average Reporting ACE and Frequency Error calculated for any one-minute interval is representative of that time interval, it is necessary that at least 50 percent of both the Reporting ACE and Frequency Error sample data during the one-minute interval is valid.
> If the recording of Reporting ACE or Frequency Error is interrupted such that less than 50 percent of the one-minute sample period data is available or valid, then that one-minute interval is excluded from the CPS1 calculation. 
{: .block-warning }
