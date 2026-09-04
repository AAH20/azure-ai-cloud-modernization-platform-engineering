# Evidence register

Evidence in this directory is classified explicitly:

| Artifact | Status | Meaning |
|---|---|---|
| `order-api-analysis.json` | Locally generated | Reproducible output from synthetic inputs |
| GitHub Actions run | CI evidence after publication | Independent execution of tests and static validation |
| Azure deployment outputs | Not yet collected | Requires restored Azure subscription access |
| Portal screenshots | Not yet collected | Must show a real deployed resource and matching identifiers |

Synthetic analysis is not evidence that Azure resources were deployed. Screenshots must never be added merely as decoration: each must be paired with the command, time, resource ID and assertion it proves.
