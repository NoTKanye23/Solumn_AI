import unittest

from syncer.transform import transform


class TransformTests(unittest.TestCase):
    def test_normalises_fields(self):
        row = {"id": "7", "name": "  Ada   Lovelace ", "email": " Ada@Example.COM ", "phone": "(555) 010-9999"}
        self.assertEqual(transform(row), {"id": "7", "name": "Ada Lovelace", "email": "ada@example.com", "phone": "+5550109999"})

    def test_empty_phone(self):
        row = {"id": "1", "name": "A", "email": "a@x.io", "phone": ""}
        self.assertEqual(transform(row)["phone"], "")


if __name__ == "__main__":
    unittest.main()
