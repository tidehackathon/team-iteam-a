import unittest


class TestConfig(unittest.TestCase):

    def setUp(self):
        import os
        os.environ['CRON'] = '* * * * *'
        os.environ['KEYWORDS'] = 'a, b , c'
        os.environ['FEED_ID'] = 'feed_id'

    def test_env_cron_param(self):
        from app.config import Config
        self.assertEqual(Config.CRON, '* * * * *')

    def test_env_keywords_param(self):
        from app.config import Config
        self.assertEqual(Config.KEYWORDS, ['a', 'b', 'c'])

    def test_env_feed_id_param(self):
        from app.config import Config
        self.assertEqual(Config.FEED_ID, 'feed_id')


if __name__ == '__main__':
    unittest.main()
