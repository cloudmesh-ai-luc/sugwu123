import unittest

from sports.cloud import plan, smoke_payload


class CloudContractTests(unittest.TestCase):
    def test_three_plans_use_current_named_start_syntax_and_correct_providers(self):
        for cloud in ["multipass", "chameleon", "google"]:
            result = plan(cloud, f"sports-{cloud}")
            self.assertEqual(result["create"], ["cmx", "vm", "--cloud", cloud, "start", f"sports-{cloud}"])

    def test_plan_rejects_coursework_vm_names(self):
        with self.assertRaises(ValueError):
            plan("multipass", "week2-vm")

    def test_provider_error_text_cannot_be_counted_as_a_success(self):
        with self.assertRaises(ValueError):
            smoke_payload("Unexpected error executing command on google: authentication failed")
        with self.assertRaises(ValueError):
            smoke_payload('{"sports_smoke":"ok","rows":0,"evaluated_games":0}')

    def test_smoke_accepts_actual_analysis_with_a_provider_banner(self):
        result = smoke_payload('Running on cloud: google\n{\n"sports_smoke":"ok",\n"rows":2460,\n"evaluated_games":72\n}')
        self.assertEqual(result["evaluated_games"], 72)
