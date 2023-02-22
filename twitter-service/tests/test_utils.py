import datetime
import unittest

from app.utils import anonymize_twitter, tweet_to_avro


class TestUtils(unittest.TestCase):

    def test_tweet_to_avro(self):
        tweet = {
            'username': 'JailtonSantana_',
            'title': 'Twitter title',
            'text': 'Twitter text', 'date': 1614643199,
            'url': 'https://twitter.com/283001860', 'language': 'en',
            'quoteCount': 0, 'replyCount': 0, 'retweetCount': 0, 'likeCount': 10
        }
        avro = tweet_to_avro(tweet)
        self.assertEqual(avro['title'], 'Twitter title')
        self.assertEqual(avro['text'], 'Twitter text')
        self.assertEqual(avro['likesCount'], 10)
        self.assertEqual(avro['created'], 1614643199)

    def test_anonymize_twitter(self):
        text = "Hello @user1, how are you? @user2"
        self.assertEqual("Hello @user9f4ce4b497, how are you? @user319eaefe9f", anonymize_twitter(text))

    def test_anonymize_twitter2(self):
        text = "Hello @user1, how are you? @user2 @user"
        self.assertEqual("Hello @user028c1f5ee19f4ce4b497, how are you? @user028c1f5ee1319eaefe9f @user028c1f5ee1",
                         anonymize_twitter(text))

    def test_anonymize_no_users(self):
        text = "Sunny day in Lithuania"
        self.assertEqual("Sunny day in Lithuania", anonymize_twitter(text))

    def test_anonymize_empty(self):
        text = ""
        self.assertEqual("", anonymize_twitter(text))


if __name__ == '__main__':
    unittest.main()
