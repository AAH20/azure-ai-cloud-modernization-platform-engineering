from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any


@dataclass(frozen=True)
class Economics:
    baseline_monthly_cost: float
    target_monthly_cost: float
    migration_cost: float
    monthly_revenue_enabled: float
    monthly_capacity_value: float
    monthly_contribution_improvement: float
    annual_net_value: float
    payback_months: float | None
    three_year_roi_percent: float


def _money(value: float) -> float:
    return round(float(value), 2)


def calculate_economics(workload: dict[str, Any]) -> Economics:
    current = workload["current_state"]
    target = workload["target_state"]
    business = workload["business"]
    baseline = float(current["monthly_infrastructure_cost"]) + float(
        current["monthly_operations_labor_cost"]
    )
    target_cost = (
        float(target["estimated_azure_cost"])
        + float(target["estimated_model_cost"])
        + float(target["estimated_operations_labor_cost"])
    )
    capacity_value = max(
        0.0,
        float(current["monthly_operations_labor_cost"])
        - float(target["estimated_operations_labor_cost"]),
    )
    revenue = float(business["monthly_revenue_enabled"])
    improvement = baseline - target_cost + revenue
    migration_cost = float(business["migration_cost"])
    payback = migration_cost / improvement if improvement > 0 else None
    annual = improvement * 12
    roi = ((improvement * 36 - migration_cost) / migration_cost * 100) if migration_cost else 0
    return Economics(
        baseline_monthly_cost=_money(baseline),
        target_monthly_cost=_money(target_cost),
        migration_cost=_money(migration_cost),
        monthly_revenue_enabled=_money(revenue),
        monthly_capacity_value=_money(capacity_value),
        monthly_contribution_improvement=_money(improvement),
        annual_net_value=_money(annual),
        payback_months=round(payback, 2) if payback is not None else None,
        three_year_roi_percent=round(roi, 1),
    )


def recommend_disposition(workload: dict[str, Any]) -> tuple[str, list[str]]:
    app = workload["application"]
    constraints = workload["constraints"]
    reasons: list[str] = []
    if app.get("retire_candidate"):
        return "retire", ["Business owner marked the capability as a retirement candidate."]
    if app.get("saas_replacement_available") and app.get("differentiation") == "low":
        return "replace", ["Low differentiation and an approved SaaS replacement are available."]
    if constraints.get("must_remain_on_premises"):
        return "retain", ["A declared constraint requires the workload to remain on-premises."]
    if app.get("cloud_ready") and app.get("container_ready"):
        reasons.extend(["Application is cloud-ready.", "Container packaging is available."])
        return "replatform", reasons
    if app.get("strategic_value") == "high" and app.get("technical_debt") == "high":
        return "refactor", ["High strategic value justifies remediation of high technical debt."]
    return "rehost", ["No stronger evidence currently justifies a deeper transformation."]


def evaluate_gates(workload: dict[str, Any], economics: Economics) -> list[dict[str, Any]]:
    target = workload["target_state"]
    constraints = workload["constraints"]
    gates = [
        ("nonnegative-value", economics.monthly_contribution_improvement > 0,
         "Target must produce positive monthly contribution improvement."),
        ("recovery-objectives", target["rto_hours"] <= constraints["max_rto_hours"] and
         target["rpo_hours"] <= constraints["max_rpo_hours"],
         "Target RTO and RPO must satisfy business limits."),
        ("data-residency", target["region"] in constraints["allowed_regions"],
         "Deployment region must be explicitly allowed."),
        ("private-data-path", bool(target["private_data_path"]),
         "Production data services require a private path."),
        ("rollback", bool(target["rollback_tested"]),
         "A tested rollback is required before promotion."),
        ("owner-approval", bool(workload["approvals"]["business_owner"]),
         "Business owner approval is required."),
    ]
    return [{"id": key, "passed": passed, "requirement": requirement} for key, passed, requirement in gates]


def analyze(workload: dict[str, Any]) -> dict[str, Any]:
    disposition, reasons = recommend_disposition(workload)
    economics = calculate_economics(workload)
    gates = evaluate_gates(workload, economics)
    result = {
        "schema_version": "1.0",
        "workload_id": workload["workload_id"],
        "disposition": {"recommendation": disposition, "reasons": reasons},
        "economics": asdict(economics),
        "release_gates": gates,
        "decision": "promote" if all(g["passed"] for g in gates) else "hold",
        "evidence_boundary": "Modeled from declared inputs; not evidence of an Azure deployment.",
    }
    canonical = repr(sorted(result.items())).encode()
    result["analysis_digest_sha256"] = sha256(canonical).hexdigest()
    return result
