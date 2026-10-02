import unittest
from review import review_text


class SSHTests(unittest.TestCase):
    def test_explicit_risky_settings(self):
        self.assertEqual({x["rule"] for x in review_text("PermitRootLogin yes\nPasswordAuthentication yes\n")}, {"permitrootlogin", "passwordauthentication"})

    def test_first_global_and_match_scope(self):
        self.assertEqual({x["rule"] for x in review_text("PermitRootLogin no\nPermitRootLogin yes\nMatch User guest\nPasswordAuthentication yes\n")}, {"match-scope-review", "passwordauthentication"})

    def test_invalid_directive(self):
        with self.assertRaises(ValueError):
            review_text("PermitRootLogin\n")
