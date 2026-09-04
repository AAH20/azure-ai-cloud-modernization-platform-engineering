# Architecture

## Decision plane

The current executable plane consumes a versioned workload record. It produces disposition, economics, release gates and a content digest. The contract is intentionally provider-neutral so future model and graph adapters cannot bypass the deterministic controls.

## Azure platform plane

The enterprise target uses Azure landing-zone separation:

- Identity: Microsoft Entra ID, workload identities, PIM and break-glass procedures.
- Connectivity: hub-spoke or Virtual WAN, centralized egress, DNS and private endpoints.
- Management: Azure Monitor, Log Analytics, action groups and cost exports.
- Application landing zones: independently owned workload subscriptions and environments.
- Data and AI: Azure Database for PostgreSQL, Storage, Azure AI Search, model endpoints and optional Microsoft Fabric analytics.

The checked-in low-cost Bicep profile deploys only a resource group, Log Analytics workspace and hardened storage account. Expensive components are intentionally excluded from the default profile.

## Agentic plane

Planned agents are advisory roles: discovery, modernization, network, platform, data, model-routing, FinOps and reliability. A durable orchestrator owns state transitions. Model routing uses declared policies for capability, cost, latency and residency. Retrieval may combine PostgreSQL/pgvector, Azure AI Search and a graph adapter.

## Trust boundaries

1. Imported estate metadata is untrusted input.
2. Retrieved text cannot create authority.
3. Generated IaC must pass static validation, what-if and policy checks.
4. Secrets remain in an external secret store and never enter prompts.
5. Production release requires an identity distinct from the recommending agent.
6. Rollback is tested before promotion.

## Reliability

Production profiles must define SLOs, dependency failure modes, retry budgets, bulkheads, region-failure behavior, RTO/RPO and restoration evidence. Multi-region deployment is a workload decision—not a portfolio checkbox.
