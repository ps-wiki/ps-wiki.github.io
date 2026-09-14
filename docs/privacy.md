---
title: Privacy Policy
description: How PS-Wiki handles website, REST API, and MCP request data
---

# Privacy Policy

**Last updated: 2026-09-14.**

This policy describes the request data handled by the Power Systems Wiki
(“PS-Wiki”) website, REST API, and remote MCP server. The service is operated
as an open, read-only reference project.

## Data handled

When you visit the site or call an API, Cloudflare may process ordinary network
and security data needed to deliver the service. PS-Wiki's application-level
telemetry is limited as follows:

- The REST and MCP Workers write a durable R2 traffic record containing the
  timestamp, worker name, HTTP method, origin and path, response status,
  duration, request ID, and selected Cloudflare location metadata (colo,
  country, and ASN when available).
- Query strings are omitted from durable R2 traffic records. This prevents
  REST search text and similar parameters from being retained in those logs.
- MCP tool telemetry records the tool name, upstream REST status information,
  bounded error classes, and elapsed time. It does not record tool arguments,
  prompts, or response bodies.
- The REST Worker may emit short-lived diagnostic logs containing method, path,
  country, colo, User-Agent, Referer, and Accept headers. These logs are
  controlled by Cloudflare's Workers Logs retention and access controls.

PS-Wiki does not require an account, does not ask for passwords, and does not
intentionally collect the contents of conversations sent by an AI client.
Please do not include confidential or sensitive information in search terms or
other requests.

## Purpose and retention

Telemetry is used to operate the service, diagnose failures, understand broad
usage, and plan capacity. R2 traffic records are retained until the project
owner deletes them or adds a Cloudflare R2 lifecycle rule; the current Worker
configuration does not set an automatic expiration. Cloudflare diagnostic-log
retention may be shorter and depends on the account plan.

The PS-Wiki application does not use these logs to train an AI model. MCP
clients and model providers may handle prompts and tool results under their
own policies; review the policy of the client you choose.

## Sharing and service providers

The Workers, R2 bucket, and diagnostic logging are provided through Cloudflare.
The remote MCP Worker retrieves public wiki data from the PS-Wiki REST API.
PS-Wiki does not sell application telemetry. Data may be processed by these
service providers as necessary to deliver, secure, and operate the service.

## Your choices and requests

You can stop sending requests at any time. To ask about a traffic record or
report a privacy concern, open a [GitHub issue](https://github.com/ps-wiki/ps-wiki.github.io/issues)
with the approximate date, worker, and route; do not include private content.
Because traffic records use generated request IDs and do not contain account
identifiers, a request may not be identifiable without sufficient timing and
route information.

## Changes

This policy may be updated when the service or its telemetry changes. The
effective date appears at the top of this page.
