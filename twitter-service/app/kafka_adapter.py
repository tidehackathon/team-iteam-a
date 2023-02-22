import logging
import threading
import time

from test_bed_adapter import TestBedOptions, TestBedAdapter
from test_bed_adapter.kafka.consumer_manager import ConsumerManager
from test_bed_adapter.kafka.producer_manager import ProducerManager

from app import utils
from app.config import Config

_logger = logging.getLogger()


class KafkaAdapter(threading.Thread):
    daemon = True
    running = True
    manager = None
    _producers = {}

    def handle_message(self, message):
        _logger.info(f"Received message {message}")
        try:
            self._parse_config(message)
        except Exception as e:
            _logger.error(e)

    def _parse_config(self, message):
        keywords = []
        for source in message['sources']:
            for feed in source['feeds']:
                if feed["type"] == "Twitter":
                    _logger.info(f"Found telegram config")
                    Config.update('FEED_ID', feed['id'])
                    Config.update('SOURCE_ID', feed['sourceId'])
                    Config.update('CRON', feed['refresh'])
                    Config.update('KEYWORDS', self.parse_keywords(feed['options']))
                    _logger.info(
                        f"Found twitter config: {Config.FEED_ID}, {Config.SOURCE_ID}, {Config.CRON}, {Config.KEYWORDS}")
        return keywords

    def send_tweets(self, tweets):
        """Send tweets to kafka"""
        _logger.info(f"Sending {len(tweets)} tweets to kafka")
        # batch tweets to 20
        for i in range(0, len(tweets), 20):
            batch = tweets[i:i + 20]
            kafka_messages = [utils.tweet_to_avro(tweet) for tweet in batch]
            self.send_messages(kafka_messages)

    def run(self):
        _logger.info("Connecting to kafka")
        self._init_starter_params()

        self._test_bed_adapter.initialize()
        listener_threads = []

        # Create threads for each consume topic
        for topic in Config.CONSUME.split(','):
            topic = topic.strip()
            _logger.info(f"Creating consumer for topic {topic}")
            listener_threads.append(threading.Thread(
                target=ConsumerManager(
                    options=self._test_bed_options,
                    kafka_topic=topic,
                    handle_message=self.handle_message,
                    run=lambda: self.running
                ).listen)
            )

        # start all threads
        for thread in listener_threads:
            _logger.info(f"Starting thread {thread}")
            thread.daemon = True
            thread.start()

        # make sure we keep running until keyboardinterrupt
        while self.running:
            # make sure we check thread health every 10 sec
            time.sleep(10)

            for thread in listener_threads:
                if not thread.is_alive():
                    self.running = False
                    _logger.error("Thread died, shutting down")

        # Stop test bed
        self._test_bed_adapter.stop()
        for producer in self._producers.values():
            producer.stop()

        # Clean after ourselves
        for thread in listener_threads:
            thread.join()

        raise Exception

    def send_messages(self, messages):
        """Send message to kafka topic"""
        for topic, producer in self._producers.items():
            try:
                producer.send_messages(messages=messages)
            except Exception as e:
                _logger.error(f"Error sending message to topic {topic}: {e}")

    def _init_starter_params(self):
        """Initialize all producers"""
        options = {
            "kafka_host": Config.KAFKA_HOST,
            "schema_registry": Config.SCHEMA_REGISTRY,
            "partitioner": Config.PARTITIONER,
            "consumer_group": Config.CLIENT_ID,
            "message_max_bytes": Config.MESSAGE_MAX_BYTES,
            "offset_type": Config.OFFSET_TYPE,
            "heartbeat_interval": Config.HEARTBEAT_INTERVAL
        }
        self._test_bed_options = TestBedOptions(options)
        self._test_bed_adapter = TestBedAdapter(TestBedOptions(options))

        self._producers = {
            topic: ProducerManager(
                options=self._test_bed_options,
                kafka_topic=topic
            ) for topic in Config.PRODUCE.split(',')
        }
        _logger.info(f"Initialized producers {self._producers.keys()}")

    @staticmethod
    def parse_keywords(options):
        try:
            keywords = options['keywords']
            if keywords:
                return [keyword.strip() for keyword in keywords.split(',')]
        except Exception as e:
            _logger.error(f'Error parsing keywords: {options} {e}')
            return []
