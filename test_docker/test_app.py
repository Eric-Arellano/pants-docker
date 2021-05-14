import test_docker.app
from unittest import TestCase

class TestApplication(TestCase):
    def test_xzy(self):
        self.assertEqual(1, 2)

    def test_abc(self):
        self.assertEqual('abc', 123)
