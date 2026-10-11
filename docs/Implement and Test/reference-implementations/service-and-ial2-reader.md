---
title: "Service and IAL2 Reader"
excerpt: "The FHIR $match service that wraps the library, and the IAL2 token reader."
hidden: false
---

## Patient matching service

*Source of truth: the [README of cms-hte-patient-matching-service](https://github.com/icanbwell/cms-hte-patient-matching-service#readme) and its `docs/TECH_DESIGN.md`. Where this page differs from the repository, the repository is correct.*

A FastAPI service that wraps the [patient matching library](/docs/patient-matching-library) as a FHIR `$match` endpoint.

### Endpoints

| Endpoint | Behavior |
|---|---|
| `POST /Patient/$match` | FHIR `$match`. Requires a bearer JWT. The query `Patient` comes from a `Parameters` resource in the request body, or from a CMS Blue Button `cms_smart` identity in the auth token (verified and converted by the IAL2 reader, with no request body needed). The response is a `searchset` `Bundle` of matched candidates, each with the match outcome and matched rule ID as extensions. |
| `GET /health` | Unauthenticated liveness and readiness probe. |

### Behaviors to know before deploying

- **Authentication fails closed.** If `AUTH_JWK_URLS` is not set, every request to `/Patient/$match` returns 401.
- **No candidates without a FHIR source.** If `FHIR_BASE_URL` is not set, the service starts but its cache is empty and every request returns `no_match`.
- **The default public build does not include the matching engine.** `POST /Patient/$match` returns 503 unless the service is built with `INSTALL_MATCHING_ENGINE=true`.
- **IAL2 support is off by default.** It requires `IAL2_ALLOWED_JWKS_URLS` and `IAL2_AUDIENCE`. Without them, a request carrying a `cms_smart` identity is rejected with 400.
- **The testing UI has no authentication of its own.** The README says never to enable `ENABLE_TESTING_UI` in a production or externally reachable deployment.

### API description

The service is built with FastAPI using its defaults, so a running instance serves an OpenAPI description at `/openapi.json` and interactive documentation at `/docs` unless a deployment disables or blocks them. This site does not republish that description.

## IAL2 reader

The `cms-hte-ial2-reader` package reads a signed IAL2 token from a Credential Service Provider, verifies it, and returns a FHIR R4 `Patient` resource. It is published on [PyPI](https://pypi.org/project/cms-hte-ial2-reader/); its source repository is not public.

The specification's requirements for IAL2 token validation (signature, issuer, audience, expiry, and replay checks) are in [IAL2 Claims Tokens](/docs/ial2-claims-tokens). Those requirements apply whichever implementation you use.
