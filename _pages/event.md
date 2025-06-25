---
layout: timeline
title: event
permalink: /event/
description: Major power grid events
nav: true
nav_order: 3
col1:
- name: Aaa
  to: 2015-03-01
col2:
- name: Bee
  to: 2015-10-01
col3:
- name: Cee
  to: now
col4:
- name: Dee
  to: 2015-01-01
col5:
- name: Eee
  from: 2014-01-01
  to: now
---

{% include jekyll-timeline.html
   startYear=2014
   timelineHeight=400

   col1Title="A"
   col1Events=page.col1

   col2Title="B"
   col2Events=page.col2

   col3Title="C"
   col3Events=page.col3

   col4Title="D"
   col4Events=page.col4

   col5Title="E"
   col5Events=page.col5
%}
