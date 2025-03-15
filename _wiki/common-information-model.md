---
layout: distill
title: Common Information Model
description: CIM. A set of open standards for representing power system components
permlink: /projects/common-information-model/
tags: data-format
category: wiki
bibliography: papers.bib
---

**Common Information Model (CIM)** <d-cite key="epri2021cim"></d-cite>

A set of **open standards** for representing power system components originally developed by the EPRI in North America and now a series of standards under the IEC.

**CIM** <d-cite key="anderson2023cim"></d-cite>

An abstract information model that can be used to model an electrical network and the various equipment used on the network. CIM is widely used for data exchange of bulk transmission power systems and is now beginning to find increasing use for distribution modeling and analysis. By using a common model, utilities, vendors, and researchers from both academia and industry can reduce the effort and cost of data integration, and instead focus on developing increased functionality for managing and optimizing the smart grid of the future.

A brief history of CIM can be found in <d-cite key="wollenberg2015cimhistory"></d-cite>.

A sample CIM file can be found at CIMpy at <https://github.com/sogno-platform/cimpy/tree/master/cimpy/examples/sampledata/CIGRE_MV>

Two answers by Microsoft Copilot about CIM, RDF, UML, and XML, on 01-09-2025:

The **Common Information Model (CIM)** is a **standard** developed by the electric power industry to facilitate the exchange of information about an electrical network. It is maintained as a UML model and defines a common vocabulary and basic ontology for modeling the components and measurements of power systems. The CIM is officially adopted by the International Electrotechnical Commission (IEC) and is used to derive design artifacts like XML or RDF schemas for application integration. It supports various applications, including energy management systems, SCADA, and planning and optimization1.

The **Resource Description Framework (RDF)** is a **standard model** for data interchange on the web. Developed by the World Wide Web Consortium (W3C), RDF allows for the representation of information about resources in a graph form. RDF uses triples, which consist of a subject, predicate, and object, to make statements about resources. This model is highly flexible and can represent complex relationships between data. RDF is often used in conjunction with other web standards like SPARQL for querying RDF data, and it supports various serialization formats such as RDF/XML, Turtle, and JSON-LD23.

The **Unified Modeling Language (UML)** is a standardized general-purpose **modeling language** in the field of software engineering. UML provides a set of graphical notation techniques to create visual models of software-intensive systems. It includes various types of diagrams, such as class diagrams, sequence diagrams, and use case diagrams, to represent different aspects of a system. UML is widely used for specifying, visualizing, constructing, and documenting the artifacts of software systems. It helps in understanding, designing, and managing complex software projects45.

The **Extensible Markup Language (XML)** is a **markup language** designed to store and transport data. XML allows developers to define their own tags and structure data in a platform-independent way. It is widely used for data interchange between different systems and platforms. XML documents are made up of elements defined by starting and ending tags, and they can include attributes to provide additional information about the data. XML is used in various applications, including web services, configuration files, and data exchange formats67.

Summary:

- CIM: Standard for modeling power system components and measurements, used for data exchange in the electric power industry.
- RDF: Framework for representing information about resources in a graph form, used for data interchange on the web.
- UML: General-purpose modeling language for visualizing and documenting software systems.
- XML: Markup language for storing and transporting data, allowing for custom tag definitions and platform-independent data exchange.

Summary of what CIM is not:

- CIM is not a programming language: It is a standard for modeling power system components and measurements.
- CIM is not a software application: It provides a common data model for information exchange but is not an executable program.
- CIM is not a database: While it can be used to define data structures, it is not a database management system.
- CIM is not a communication protocol: It defines data models and schemas but does not specify how data is transmitted between systems.

**Common Format for Event Data Exchange (COMFEDE) for Power Systems** <d-cite key="ieee2010comfede"></d-cite> **INACTIVE NOW**

This standard defines a common format for the data files needed for the exchange of various types of power network events in order to facilitate event data integration and analysis from multiple data sources and from different vendor devices.
The flexibility provided by digital devices in recording network fault event data in the electric utility industry has generated the need for a standard format for the exchange of data.
These data are being used with various devices to enhance and automate the analysis, testing, evaluation, and simulation of power systems and related protection schemes during fault and disturbance conditions.
Since each source of data may use a different proprietary format, a common data format is necessary to facilitate the exchange of such data between applications.
This will facilitate the use of proprietary data in diverse applications and allow users of one proprietary system to use digital data from other systems.
**A sample file is given in the source file.**

Versions:
Inactive

- Draft: PC37.239/D04, Mar 2010 - Dec 31, 2010
- Reserved: C37.239-2010 - Nov 11, 2010
- Draft: C37.239 - Jan 01, 2010

**Common Format for Transient Data Exchange (COMTRADE) for Power Systems** <d-cite key="ieee1999comtrade"></d-cite> **INACTIVE NOW**

A common format for data files and exchange medium used for the interchange of various types of fault, test, or simulation data for electrical power systems is defined. Sources of transient data are described, and the case of disketts as an exchange medium is recommended. issues of sampling rates, filters, and sample rate conversions for transient data being exchanged are discussed. Files for data exchange are specified, as is the organization of the data. **A sample file is given in the source file.**

Versions:
Superseded

- C37.111-1999 - Oct 15, 1999
- C37.111-1991 - Oct 21, 1991

Inactive

- Reserved: C37.111-2013 - Apr 30, 2013
- Redline: C37.111-2013 - Apr 30, 2013
- Draft: PC37.111/D4, Jan 2012 - Jul 24, 2012

**Common Format for Exchange of Solved Load Flow Data** <d-cite key="ieee1973loadflow"></d-cite>

Also referred as common data format (CDF).
This format is presently (_Jinning's Note: this format was used around the 1970s rather than 2020s_) being used throughout most of the eastern and north central United States and parts of Canada.
By publishing through the national organization, it is intended that a common reference be established and maintained for those who wish to use the format.
The paper presents a detailed description of the format as well as procedures for making revisions and additions.

A matpower function to convert an IEEE CDF data file into a MATPOWER case struct at <https://matpower.org/doc/ref-manual/legacy/functions/cdf2mpc.html#cdf2mpc>
