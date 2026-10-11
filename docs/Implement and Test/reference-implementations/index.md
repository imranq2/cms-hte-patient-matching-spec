---
title: "Reference Implementations Overview"
excerpt: "The public software that implements the specification, and which one to use when."
hidden: false
---

These projects are maintained by b.well Connected Health and are published openly. They are implementations of the specification, not the specification itself. **If an implementation and the specification text disagree, the specification governs.**

## What exists

| Project | What it is | Where |
|---|---|---|
| **Patient matching library** | A Python library that implements the Table 2 rules over FHIR R4 `Patient` resources, with normalization and a candidate cache. Apache-2.0. | [GitHub](https://github.com/icanbwell/cms-hte-patient-matching), [PyPI](https://pypi.org/project/cms-hte-patient-matching/) |
| **Patient matching service** | A FastAPI service that wraps the library as a FHIR `$match` HTTP endpoint. | [GitHub](https://github.com/icanbwell/cms-hte-patient-matching-service) |
| **IAL2 reader** | A package that verifies an IAL2 token and returns a FHIR `Patient`. Published on PyPI; its source repository is not public. | [PyPI](https://pypi.org/project/cms-hte-ial2-reader/) |
| **Probability calculations** | A standalone tool that computes empirical u-probabilities from public data. It is *not* part of the matching library. | [Methodology](/docs/how-the-numbers-are-derived) |

## Which to use

| If you want to | Use |
|---|---|
| Embed matching in a Python application | The library |
| Run an HTTP `$match` endpoint | The service |
| Turn a CSP-issued IAL2 token into a FHIR `Patient` | The IAL2 reader, or implement section III.D of the specification yourself |
| Implement in another language | The specification, checked against the [test set](/docs/test-set). The test set is algorithm-agnostic and needs no Python. |
| Understand how a Table 2 rule maps to code | [Spec-to-Code Map](/docs/spec-to-code-map) |

## Pages in this section

- [Patient Matching Library](/docs/patient-matching-library)
- [Service and IAL2 Reader](/docs/service-and-ial2-reader)
- [Spec-to-Code Map](/docs/spec-to-code-map)
