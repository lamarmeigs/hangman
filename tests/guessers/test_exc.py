from unittest import TestCase

from guessers.exc import TableFlipError


class TableFlipErrorTestCase(TestCase):
    def test_inheritance(self):
        self.assertIsInstance(TableFlipError(), Exception)
