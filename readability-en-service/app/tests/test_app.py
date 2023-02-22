import unittest

from app.stats import get_readability


class ServiceCase(unittest.TestCase):

    def test_service_short_text(self):
        score = get_readability("Hello world")
        self.assertGreater(score, 70)

    def test_service_long_text(self):
        score = get_readability("Hello world. This is a long text." * 100)
        self.assertGreater(score, 70)

    def test_service_empty_text(self):
        score = get_readability("")
        self.assertEqual(score, 0)

    def test_service_none_text(self):
        score = get_readability(None)
        self.assertEqual(score, 0)


if __name__ == '__main__':
    unittest.main()
