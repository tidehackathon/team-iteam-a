import logging
import unittest

from app.kafka_adapter import KafkaAdapter
from app.config import Config

_config = {
    "sources": [
        {
            "feeds": [
                {
                    "id": "feed-id",
                    "sourceId": "sourceId-id",
                    "type": "Twitter",
                    "refresh": "0 * * * *",
                    "options": {
                        "keywords": "test, test2"
                    }
                }
            ]
        }
    ]
}


class TestKafkaAdapter(unittest.TestCase):
    def test_config_feed_id(self):
        kafka = KafkaAdapter()
        kafka.handle_message(_config)
        self.assertEqual(Config.FEED_ID, "feed-id")

    def test_config_source_id(self):
        kafka = KafkaAdapter()
        kafka.handle_message(_config)
        self.assertEqual(Config.SOURCE_ID, "sourceId-id")

    def test_config_cron(self):
        kafka = KafkaAdapter()
        kafka.handle_message(_config)
        self.assertEqual(Config.CRON, "0 * * * *")

    def test_config_keywords(self):
        kafka = KafkaAdapter()
        kafka.handle_message(_config)
        self.assertEqual(Config.KEYWORDS, ["test", "test2"])


if __name__ == '__main__':
    unittest.main()
