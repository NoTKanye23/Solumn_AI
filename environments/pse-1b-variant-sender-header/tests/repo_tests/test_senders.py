import unittest

from billmail import senders


class SenderTests(unittest.TestCase):
    def test_verified_domain_allowed(self):
        self.assertTrue(senders.is_allowed("Acme Billing <billing@acme-billing.example>"))

    def test_unverified_domain_rejected(self):
        self.assertFalse(senders.is_allowed("invoices@some-other-company.example"))
        with self.assertRaises(senders.SenderNotAllowed):
            senders.assert_allowed("x@some-other-company.example")


if __name__ == "__main__":
    unittest.main()
