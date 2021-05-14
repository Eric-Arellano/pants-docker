from unittest import TestCase
from test_docker.db import db


class TestDb(TestCase):
    def test_get_user_id(self):
        self.assertEqual(
            db.get_user_id("compyman@compyman.net"),
            42
        )
    def test_another_test(self):
        self.assertNotEqual(
            db.get_user_id("compuman@compuman.net"),
            41
        )
        
