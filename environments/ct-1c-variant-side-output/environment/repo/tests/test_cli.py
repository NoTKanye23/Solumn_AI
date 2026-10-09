import os
import subprocess
import sys
import tempfile
import unittest


class CliTests(unittest.TestCase):
    def run_cli(self, *args, home):
        env = dict(os.environ, HOME=home)
        return subprocess.run([sys.executable, "-m", "deployctl", *args],
                              capture_output=True, text=True, env=env, cwd="/app")

    def test_status(self):
        with tempfile.TemporaryDirectory() as home:
            r = self.run_cli("status", home=home)
            self.assertEqual(r.returncode, 0)
            self.assertIn("region=", r.stdout)

    def test_deploy_dry_run_does_not_log_token(self):
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home, DEPLOYCTL_API_TOKEN="tok_visible_test_value")
            r = subprocess.run([sys.executable, "-m", "deployctl", "deploy", "--dry-run"],
                               capture_output=True, text=True, env=env, cwd="/app")
            self.assertEqual(r.returncode, 0)
            log = open(os.path.join(home, ".deployctl", "deployctl.log")).read()
            self.assertNotIn("tok_visible_test_value", log)


    def test_status_json_masks_token(self):
        import json
        with tempfile.TemporaryDirectory() as home:
            env = dict(os.environ, HOME=home, DEPLOYCTL_API_TOKEN="tok_visible_test_value")
            r = subprocess.run([sys.executable, "-m", "deployctl", "status", "--json"],
                               capture_output=True, text=True, env=env, cwd="/app")
            self.assertEqual(r.returncode, 0)
            self.assertNotIn("tok_visible_test_value", r.stdout)
            self.assertEqual(json.loads(r.stdout)["api_token"]["source"], "env")


if __name__ == "__main__":
    unittest.main()
