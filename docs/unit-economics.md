# Unit economics

## Equations

```text
baseline monthly cost = current infrastructure + current operations labour
target monthly cost = Azure + model inference + target operations labour
monthly contribution improvement = baseline - target + revenue enabled
payback months = migration cost / monthly contribution improvement
three-year ROI = ((36 × monthly improvement) - migration cost) / migration cost
```

The calculations are intentionally simple, inspectable and tested. A production assessment should also model taxes, discount rate, licence termination, egress, parallel-run cost, risk-adjusted downtime and uncertainty ranges.

## Synthetic worked case

| Measure | Value |
|---|---:|
| Baseline infrastructure | $18,500/month |
| Baseline operations labour | $12,000/month |
| Azure estimate | $11,200/month |
| Model estimate | $850/month |
| Target operations labour | $4,800/month |
| Revenue enabled | $22,000/month |
| Migration investment | $95,000 |

This is a synthetic scenario for testing the model. It is neither a quote nor a guaranteed customer outcome.

## Required sensitivity cases

Every customer decision should include expected, downside and severe-downside cases. At minimum vary cloud consumption, implementation duration, inference volume, labour realization, revenue delay and outage impact.
