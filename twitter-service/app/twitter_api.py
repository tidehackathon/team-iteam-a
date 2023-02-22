import logging
from pprint import pprint
from typing import List

import snscrape.modules.twitter as sntwitter

_logger = logging.getLogger(__name__)


class TwitterApi:
    """Twitter API uses snscrape library to get tweets by search query"""

    @staticmethod
    def get_tweets_by_search(search: str, date_from: int, date_to: int, limit: int = 1000) -> List[dict]:
        """
        Get tweets by search query
        :param search: query
        :param date_from: date from (unix timestamp)
        :param date_to: date to (unix timestamp)
        :param limit: limit of tweets
        :return: list of tweets (dict)
        :rtype: List[dict]
        :example:
            >>> TwitterApi.get_tweets_by_search('covid', 1614556800, 1614643200, 10)
        """
        tweets = []
        cursor = sntwitter.TwitterSearchScraper(f'{search} since:{date_from} until:{date_to}').get_items()
        for i, tweet in enumerate(cursor):
            if i >= limit:
                break
            title = ''
            tweets.append(
                {
                    'username': tweet.user.username,
                    'title': title,
                    'text': tweet.content,
                    'date': int(tweet.date.timestamp()),
                    'url': tweet.url,
                    'language': tweet.lang,
                    'quoteCount': tweet.quoteCount if hasattr(tweet, 'quoteCount') else 0,
                    'replyCount': tweet.replyCount if hasattr(tweet, 'replyCount') else 0,
                    'retweetCount': tweet.retweetCount if hasattr(tweet, 'retweetCount') else 0,
                    'likeCount': tweet.likeCount if hasattr(tweet, 'likeCount') else 0
                }
            )
        _logger.info(f'Found {len(tweets)} tweets by search query: {search}')
        return tweets
