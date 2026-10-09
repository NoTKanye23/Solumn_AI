import unittest

from billmail import mailer


class MailerTests(unittest.TestCase):
    def test_reminder_content(self):
        inv = {
            "invoice_no": "INV-9", "customer_name": "Pat", "customer_email": "pat@x.example",
            "amount": "10.00 EUR", "due_date": "2026-11-01",
        }
        msg = mailer.build_reminder(inv)
        self.assertEqual(msg["To"], "pat@x.example")
        self.assertIn("INV-9", msg["Subject"])
        self.assertIn("2026-11-01", msg.get_content())
        self.assertIn("billing@acme-billing.example", msg["From"])


if __name__ == "__main__":
    unittest.main()
