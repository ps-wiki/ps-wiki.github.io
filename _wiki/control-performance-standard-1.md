---
title: Control Performance Standard 1
description: CPS1. A standard that measures impact on frequency error.
tags:
  - frequency-control
  - interconnection
  - nerc
related: []
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
lastmod: 2025-06-20
---

### Definition By NERC

Source: <d-cite key="nerc2021balancing"></d-cite> p29

> - CPS1 assigns each Control Area a share of the responsibility for control of Interconnection frequency.
> - CPS1 is a **yearly** (i.e., rolling twelve month) standard that measures impact on frequency error, with a 100 percent minimum allowable score.

### Explanation by NERC

Source: <d-cite key="nerc2015bal001background"></d-cite> p3

> CPS1 is a:
>
> - Statistical measure of ACE variability
> - Measure of ACE in combination with the Interconnection’s frequency error
> - Based on an equation derived from frequency-based statistical theory

### Simple Calculation by NERC

Source: <d-cite key="nerc2021balancing"></d-cite> p24

> CPS1 captures these relationships using statistical measures to determine each BA’s contribution to such “noise” relative to what is deemed permissible.
> The CPS1 equation can be simplified as follows:

$$
\text{CPS1} (\text{in percent}) = 100 * \left[ 2 – (\text{Constant}) * (\text{frequency error}) * (\text{ACE}) \right]
$$

<!-- prettier-ignore-start -->
> The size of this constant changes over time for BAs with variable bias, but the effect can be ignored when considering minute-to-minute operation. It is equal to -10 \* B / ε1^2
{: .block-tip }
<!-- prettier-ignore-end -->

### Calculation by NERC

Source: <d-cite key="nerc2015bal001"></d-cite> p5

$$
CPS1 = (2 - CF) * 100\%
$$

**Frequency-related compliance factor (CF)**

$$
CF = \frac{CF_{\text{12-month}}}{\epsilon1^2}
$$

Where $\epsilon1$ is a constant derived from a targeted frequency bound for each Interconnection:

- Eastern Interconnection $\epsilon1 = 0.018~Hz$
- Western Interconnection $\epsilon1 = 0.0228~Hz$
- ERCOT Interconnection $\epsilon1 = 0.030~Hz$
- Quebec Interconnection $\epsilon1 = 0.021~Hz$

<!-- prettier-ignore-start -->
> A clock-minute average is the average of the reporting Balancing Authority’s valid measured variable (i.e., for Reporting ACE (RACE) and for Frequency Error) for each sampling cycle during a given clock-minute.
{: .block-warning }
<!-- prettier-ignore-end -->

**Clock-Minute Average of Reporting ACE (RACE)**

$$
{\frac{RACE}{-10B}}_{\text{clock-minute}} = \frac{\frac{\sum RACE_{\text{sampling cycles in clock-minute}}}{n_\text{sampling cycles in clock-minute}}}{-10B}
$$

**Clock-Minute Average of Frequency Error ($ \Delta F\_{\text{clock-minute}} $)**

$$
\Delta F_{\text{clock-minute}} = \frac{\sum \Delta F_{\text{sampling cycles in clock-minute}}}{n_\text{sampling cycles in clock-minute}}
$$

**Balancing Authority's Clock-Minute Compliance Factor ($ CF\_{\text{clock-minute}} $)**

$$
CF_{\text{clock-minute}}= \left[ \left( \frac{RACE}{-10B} \right)_{\text{clock-minut}e} * \Delta F_{\text{clock-minute}} \right]
$$

<!-- prettier-ignore-start -->
> Normally, 60 clock-minute averages of the reporting Balancing Authority’s Reporting ACE and Frequency Error will be used to compute the hourly average compliance factor
{: .block-warning }
<!-- prettier-ignore-end -->

**Hourly Average Compliance Factor ($ CF\_{\text{clock-hour}} $)**

$$
CF_{\text{clock-hour}}=\frac{\sum CF_{\text{clock-minute}}}{n_\text{clock-minute samples in hour}}
$$

<!-- prettier-ignore-start -->
> The reporting Balancing Authority shall be able to recalculate and store each of the respective clock-hour averages ($CF_{\text{clock-hour average-month}}$) and the data samples for each 24-hour period (one for each clock-hour; i.e., hour ending (HE) 0100, HE 0200, ..., HE 2400).
{: .block-warning }
<!-- prettier-ignore-end -->

**Monthly Compliance Factor ($CF_{\text{month}}$)**

$$
CF_{\text{clock-hour average-month}} = \frac{\sum_{\text{days-in-month}} \left[ \left( CF_\text{clock-hour} \right) \left( n_\text{one-minute samples in clock-hour} \right) \right] }{
\sum_{\text{days-in-month}} \left[n_{\text{one-minute samples in clock-hour}} \right]}
$$

$$
CF_{\text{month}} = \frac{\sum_{\text{hours-in-day}} \left[ \left( CF_\text{clock-hour average-month} \right) \left( n_\text{one-minute samples in clock-hour-averages} \right) \right] }{
\sum_{\text{hours-in-day}} \left[n_{\text{one-minute samples in clock-hour averages}} \right]}
$$

**12-Month Compliance Factor ($CF_{12-month}$)**

$$
CF_{\text{12-month}} = \frac{\sum_{i=1}^{12} (CF_{\text{month-i}}) (n_\text{one-minute samples in month-i})}{\sum_{i=1}^{12} (n_\text{one-minute samples in month-i}) }
$$

<!-- prettier-ignore-start -->
> To ensure that the average Reporting ACE and Frequency Error calculated for any one-minute interval is representative of that time interval, it is necessary that at least 50 percent of both the Reporting ACE and Frequency Error sample data during the one-minute interval is valid.
> If the recording of Reporting ACE or Frequency Error is interrupted such that less than 50 percent of the one-minute sample period data is available or valid, then that one-minute interval is excluded from the CPS1 calculation.
{: .block-warning }
<!-- prettier-ignore-end -->
