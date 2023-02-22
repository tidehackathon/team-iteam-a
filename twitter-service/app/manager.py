import logging
from time import sleep

import pycron as pycron

from app import utils
from app.twitter_api import TwitterApi
from app.config import *

from app.kafka_adapter import KafkaAdapter

_logger = logging.getLogger(__name__)


class Manager:
    def __init__(self):
        self.now_date = utils.timestamp()
        self.last_date = None
        self.running = True

        self.kafka_adapter = KafkaAdapter()

    def start(self):
        self.kafka_adapter.start()
        _logger.info(f'Starting manager with keywords {Config.KEYWORDS} and cron {Config.CRON}')
        self._process()

    def stop(self):
        self.running = False

    def _process(self):
        sleep(60)
        _logger.info('Running')
        if self._check():
            self._get_tweets()
        if self.running:
            self._process()

    def _check(self):
        """Check if it's time to get new tweets"""
        if Config.KEYWORDS and Config.CRON and Config.FEED_ID and Config.SOURCE_ID:
            return pycron.is_now(Config.CRON)
        return False

    def _get_tweets(self):
        """Get tweets from Twitter API"""
        _logger.info('Getting tweets')
        self.last_date = self.now_date
        self.now_date = utils.timestamp()
        _logger.info(f'Getting tweets from {self.last_date} to {self.now_date} with keywords {Config.KEYWORDS}')
        for keyword in Config.KEYWORDS:
            tweets = self._get_tweets_by_keyword(keyword)
            if tweets:
                self.kafka_adapter.send_tweets(tweets)
                _logger.info(f'Done sending tweets for keyword {keyword}')

    def _get_tweets_by_keyword(self, keyword):
        """Get tweets by keyword"""
        try:
            tweets = TwitterApi.get_tweets_by_search(keyword, self.last_date, self.now_date, 100)
            return tweets
        except Exception as e:
            _logger.error(f'Error getting tweets by keyword {keyword}: {e}')
            return []
