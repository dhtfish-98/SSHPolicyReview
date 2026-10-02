import json
import plistlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from review import review_text


class RegressionTests(unittest.TestCase):

    def test_quoted_and_equal_settings(self):
        self.assertEqual([x["rule"] for x in review_text('PermitRootLogin "yes"\n')],["permitrootlogin"])
        self.assertEqual([x["rule"] for x in review_text('PasswordAuthentication=yes\n')],["passwordauthentication"])
    def test_includes_are_explicitly_unresolved(self):
        rules={x["rule"] for x in review_text('Include "local#owned.conf"\nMatch User synthetic\nPermitRootLogin yes\n')}
        self.assertEqual(rules,{"unresolved-include","match-scope-review","permitrootlogin"})
