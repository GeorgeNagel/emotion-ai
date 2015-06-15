from unittest import TestCase


class TestRun(TestCase):
    def test_run(self):
        # Run should complete without error
        from ai.example import run  # noqa
