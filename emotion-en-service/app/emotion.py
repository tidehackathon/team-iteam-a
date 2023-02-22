import json
import logging

from transformers import pipeline

_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

_logger = logging.getLogger(__name__)


def predict_emotion(text: str):
    """
    Predict emotion of text
    :param text: text to predict
    :return: dict of emotions and scores
    """
    try:
        if not text:
            return {}
        if len(text) > 512:
            text = text[:512]
        result = _classifier(text)[0]
        result_dict = {}
        for item in result:
            score = item['score']
            score = round(score, 3)
            result_dict[item['label']] = score
        _logger.info(f'Predicted {text[:50]} emotion: {result_dict}')
        return result_dict
    except Exception as e:
        _logger.error(f'Error predicting emotion: {e}')
        return {}


if __name__ == '__main__':
    text = 'I am happy'
    print(predict_emotion(text))
