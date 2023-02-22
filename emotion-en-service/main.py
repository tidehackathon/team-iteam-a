from datetime import datetime
from time import sleep

from starter_service.base_service import StarterService

from app.emotion import predict_emotion


class EmotionENService(StarterService):

    def handle_article(self, article: dict):
        try:
            text = article['text']
            result_dict = predict_emotion(text)
            if not result_dict:
                return
            result_list = [{"key": k, "value": v} for k, v in result_dict.items()]
            message = {
                'origin': self._CLIENT_ID,
                'refId': article['id'],
                'schema': 'ARTICLE',
                'timestamp': int(datetime.now().timestamp()),
                'keyValuePairs': result_list
            }
            self.send_message(message)
        except Exception as e:
            self.logger.error(f"Error: bad article:\n{article} \n{e}")


if __name__ == '__main__':
    print("Starting emotion detection service in 30 seconds...")
    sleep(30)
    EmotionENService(
        PRODUCE="key_value_xx",
        CONSUME="article_raw_en",
        CLIENT_ID="emotion_en_service"
    ).start()
