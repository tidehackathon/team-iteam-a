from datetime import datetime

from starter_service.base_service import StarterService

from app.stats import get_readability


class ReadabilityService(StarterService):

    def handle_article(self, article: dict):
        try:
            text = article['text']
            score = get_readability(text)
            message = {
                'origin': self._CLIENT_ID,
                'refId': article['id'],
                'schema': 'ARTICLE',
                'timestamp': int(datetime.now().timestamp()),
                'keyValuePairs': [{"key": 'readability', "value": score}]
            }
            self.send_message(message)
        except Exception as e:
            self.logger.error(f"Error: bad article:\n{article} \n{e}")


if __name__ == '__main__':
    ReadabilityService(
        PRODUCE="key_value_xx",
        CONSUME="article_raw_en",
        CLIENT_ID="readability_en_service"
    ).start()
