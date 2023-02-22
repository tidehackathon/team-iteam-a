import unittest

from app.twitter_api import TwitterApi


@unittest.skip("skipping")
class TestTwitterAPI(unittest.TestCase):
    def test_search_by_keyword(self):
        tweets = TwitterApi.get_tweets_by_search('covid', 1614556800, 1614643200, 1)
        print(tweets)
        self.assertEqual(len(tweets), 1)


if __name__ == '__main__':
    unittest.main()
