---
layout: distill
title: Area, Zone, Region
description: Some geographical concepts in power systems
permalink: /wiki/area-zone-region/
tags: balancing-authority, area, zone, region
category: wiki
bibliography: papers.bib
---

**Balancing Authority Area** <d-cite key="nerc2024glossary"></d-cite>

The collection of generation, transmission, and loads within the metered boundaries of the [Balancing Authority](/wiki/balancing-authority).
The Balancing Authority maintains load-resource balance within this area.

**Reliability Coordinator Area** <d-cite key="nerc2024glossary"></d-cite>

The collection of generation, transmission, and loads within the boundaries of the Reliability Coordinator.
Its boundary coincides with one or more Balancing Authority Areas.

**Control Area** <d-cite key="ferc2020glossary"></d-cite>

An electric power system or combination of electric power systems to which a common automatic control scheme is applied in order to:
- Match, at all times, the power output of the generators within the electric power system(s) and capacity and energy purchased from entities outside the electric power system(s), with the load in the electric power system(s).
- Maintain, within the limits of Good Utility Practice, scheduled interchange with other Control Areas.
- Maintain the frequency of the electric power system(s) within reasonable limits in accordance with Good Utility Practice.
- Provide sufficient generating capacity to maintain operating reserves in accordance with Good Utility Practice.

Another definition from HIFLD:

Control Areas, also known as Balancing Authority Areas, are controlled by Balancing Authorities, who are responsible for monitoring and balancing the generation, load, and transmission of electric power within their region, often comprised of the retail service territories of numerous electric power utilities.

URL: <https://hifld-geoplatform.hub.arcgis.com/datasets/geoplatform::control-areas/about>

Map of [Control Areas](https://hifld-geoplatform.hub.arcgis.com/maps/db7622e5ebdd40428fcafbd1615d621a)

**Loss Zone** <d-cite key="matpower"></d-cite>

In MATPOWER, there is a bus parameter named "ZONE", and it means loss zone.

**Zone**

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/PJM_zone_map.png"
        zoomable=true %}
        PJM Transmission Zones Map (from <d-cite key="pjm2023transmission"></d-cite>)
    </div>
</div>

**Region** <d-cite key="nerc2024tpl"></d-cite>

NERC divides North America into several regions for the purpose of reliability and coordination.
Each region is responsible for ensuring the reliability of the bulk power system within its boundaries.
The six regions are:

- MRO: Midwest Reliability Organization
- NPCC: Northeast Power Coordinating Council
- RF: ReliabilityFirst
- SERC: SERC Reliability Corporation
- Texas RE: Texas Reliability Entity
- WECC: Western Electricity Coordinating Council

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid
        path="/assets/img/pswiki/six_region.png"
        zoomable=true %}
        Regional Maps (from <d-cite key="nerc2024tpl"></d-cite>)
    </div>
</div>

<br>
<br>
<br>
