import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from address import core


class AddressTest(unittest.TestCase):
    def test_plain_address_ok(self):
        out = core.parse("user@example.com")
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["normalized"], "user@example.com")

    def test_missing_at_sign(self):
        self.assertEqual(core.parse("user.example.com")["reason"], "bad-form")

    def test_empty_local(self):
        self.assertEqual(core.parse("@example.com")["reason"], "bad-form")

    def test_single_label_domain(self):
        self.assertEqual(core.parse("user@localhost")["status"], "ok")

    def test_counting_uses_index_for_distinct(self):
        out = core.check_all(["user@example.com", "other@example.com"], core.Counter())
        self.assertEqual(out["unique"], 2)
        self.assertEqual(out["valid"], 2)


if __name__ == "__main__":
    unittest.main()
