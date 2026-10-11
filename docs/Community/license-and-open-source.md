---
title: "License and Open Source"
excerpt: "The licenses that cover the site, the specification text, the code, and the data."
hidden: true
---

The documentation site, the reference implementations, the probability calculations, and the test set are open source.

## Licenses

| Component | License |
|---|---|
| This site and the specification text | Apache-2.0 |
| Patient matching library (`cms-hte-patient-matching`), including the probability calculations in `calculations/` | Apache-2.0 (the repository's LICENSE file, and the package metadata on PyPI) |
| Test set (`cms-hte-patient-matching-test-set`) | Apache-2.0 (the repository's LICENSE file) |
| Patient matching service | Apache-2.0 (the repository's LICENSE file) |

Copyright in the library and test set is held by b.well Connected Health, Inc., according to their LICENSE files.

## Data

The code is licensed as above, but the data these projects use comes from public sources that have their own terms:

- **ONC 2017 Patient Matching Algorithm Challenge dataset**, used to build the test set. The test set's README advises independently confirming the terms ONC published it under before redistributing it further.
- **U.S. Census Bureau, CMS, CDC/NCHS, and SSA public data**, used by the probability calculations. See [Data Sources](/docs/data-sources).

## Contributing

Contributions are accepted under the license of the repository they go to. See [Contribute](/docs/contribute).
