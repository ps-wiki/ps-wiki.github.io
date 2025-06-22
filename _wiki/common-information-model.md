---
title: Common Information Model
description: CIM. A set of open standards for representing power system components
tags:
  - data-format
bibliography: papers.bib
authors:
  - name: Jinning Wang
    url: https://jinningwang.github.io
date: 2025-03-15
last_update: 2025-06-19
---

### Definition in an EPRI Technical Update

Source: <d-cite key="epri2021cim"></d-cite>

> A set of **open standards** for representing power system components originally developed by the EPRI in North America and now a series of standards under the IEC.

### Definition in an PNNL Technical Report

Source: <d-cite key="anderson2023cim"></d-cite>

> An abstract information model that can be used to model an electrical network and the various equipment used on the network. CIM is widely used for data exchange of bulk transmission power systems and is now beginning to find increasing use for distribution modeling and analysis. By using a common model, utilities, vendors, and researchers from both academia and industry can reduce the effort and cost of data integration, and instead focus on developing increased functionality for managing and optimizing the smart grid of the future.

A brief history of CIM can be found in <d-cite key="wollenberg2015cimhistory"></d-cite>.

A sample CIM file can be found at CIMpy at <https://github.com/sogno-platform/cimpy/tree/master/cimpy/examples/sampledata/CIGRE_MV>

Two answers by Microsoft Copilot about CIM, RDF, UML, and XML, on 01-09-2025:

The **Common Information Model (CIM)** is a **standard** developed by the electric power industry to facilitate the exchange of information about an electrical network. It is maintained as a UML model and defines a common vocabulary and basic ontology for modeling the components and measurements of power systems. The CIM is officially adopted by the International Electrotechnical Commission (IEC) and is used to derive design artifacts like XML or RDF schemas for application integration. It supports various applications, including energy management systems, SCADA, and planning and optimization.

The **Resource Description Framework (RDF)** is a **standard model** for data interchange on the web. Developed by the World Wide Web Consortium (W3C), RDF allows for the representation of information about resources in a graph form. RDF uses triples, which consist of a subject, predicate, and object, to make statements about resources. This model is highly flexible and can represent complex relationships between data. RDF is often used in conjunction with other web standards like SPARQL for querying RDF data, and it supports various serialization formats such as RDF/XML, Turtle, and JSON-LD.

The **Unified Modeling Language (UML)** is a standardized general-purpose **modeling language** in the field of software engineering. UML provides a set of graphical notation techniques to create visual models of software-intensive systems. It includes various types of diagrams, such as class diagrams, sequence diagrams, and use case diagrams, to represent different aspects of a system. UML is widely used for specifying, visualizing, constructing, and documenting the artifacts of software systems. It helps in understanding, designing, and managing complex software projects.

The **Extensible Markup Language (XML)** is a **markup language** designed to store and transport data. XML allows developers to define their own tags and structure data in a platform-independent way. It is widely used for data interchange between different systems and platforms. XML documents are made up of elements defined by starting and ending tags, and they can include attributes to provide additional information about the data. XML is used in various applications, including web services, configuration files, and data exchange formats.

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
