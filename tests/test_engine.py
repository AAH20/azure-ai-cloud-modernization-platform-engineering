import unittest

from modernization_factory.engine import analyze, calculate_economics


def workload():
    return {
        "workload_id": "test-1",
        "application": {"strategic_value": "high", "technical_debt": "high",
                        "differentiation": "high", "cloud_ready": True,
                        "container_ready": True, "retire_candidate": False,
                        "saas_replacement_available": False},
        "current_state": {"monthly_infrastructure_cost": 10000,
                          "monthly_operations_labor_cost": 5000},
        "target_state": {"region": "westeurope", "estimated_azure_cost": 7000,
                         "estimated_model_cost": 500,
                         "estimated_operations_labor_cost": 2500,
                         "rto_hours": 2, "rpo_hours": 0.5,
                         "private_data_path": True, "rollback_tested": True},
        "business": {"migration_cost": 60000, "monthly_revenue_enabled": 5000},
        "constraints": {"must_remain_on_premises": False,
                        "allowed_regions": ["westeurope"], "max_rto_hours": 4,
                        "max_rpo_hours": 1},
        "approvals": {"business_owner": True},
    }


class EngineTests(unittest.TestCase):
    def test_replatform_and_promote(self):
        result = analyze(workload())
        self.assertEqual(result["disposition"]["recommendation"], "replatform")
        self.assertEqual(result["decision"], "promote")

    def test_economics_are_auditable(self):
        result = calculate_economics(workload())
        self.assertEqual(result.baseline_monthly_cost, 15000)
        self.assertEqual(result.target_monthly_cost, 10000)
        self.assertEqual(result.monthly_contribution_improvement, 10000)
        self.assertEqual(result.payback_months, 6)

    def test_failed_rollback_holds_release(self):
        case = workload()
        case["target_state"]["rollback_tested"] = False
        result = analyze(case)
        self.assertEqual(result["decision"], "hold")
        self.assertFalse(next(g for g in result["release_gates"] if g["id"] == "rollback")["passed"])

    def test_disallowed_region_holds_release(self):
        case = workload()
        case["target_state"]["region"] = "eastus"
        self.assertEqual(analyze(case)["decision"], "hold")

    def test_negative_value_holds_release(self):
        case = workload()
        case["business"]["monthly_revenue_enabled"] = 0
        case["target_state"]["estimated_azure_cost"] = 20000
        self.assertEqual(analyze(case)["decision"], "hold")


if __name__ == "__main__":
    unittest.main()
