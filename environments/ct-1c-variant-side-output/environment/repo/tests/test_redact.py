import unittest

from deployctl.redact import mask


class MaskTests(unittest.TestCase):
    def test_masks_token_pair(self):
        self.assertNotIn("abc123", mask("api_token=abc123 region=eu"))

    def test_masks_json_password(self):
        self.assertNotIn("hunter2", mask('{"registry_password": "hunter2"}'))

    def test_leaves_plain_text(self):
        self.assertEqual(mask("region=eu-west-1"), "region=eu-west-1")


    def test_mask_config_masks_token_value_keeps_source(self):
        from deployctl.redact import mask_config
        out = mask_config({"api_token": {"value": "abc123", "source": "env"}, "region": {"value": "eu", "source": "file"}})
        self.assertNotIn("abc123", str(out))
        self.assertEqual(out["api_token"]["source"], "env")
        self.assertEqual(out["region"]["value"], "eu")


if __name__ == "__main__":
    unittest.main()
