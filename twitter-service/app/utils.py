import hashlib
import json
import multiprocessing
import re
import uuid
from datetime import datetime
import binascii, struct


def tweet_to_avro(tweet) -> dict:
    from app.config import Config
    return {
        "id": get_uuid(),
        "feedId": Config.FEED_ID,
        "sourceId": Config.SOURCE_ID,
        "type": "social_media",
        "url": tweet['url'],
        "title": '',
        "text": anonymize_twitter(tweet['text']),
        "language": tweet['language'],
        "summary": "",
        "version": 1,
        "originalLanguage": None,
        "original": None,
        "images": [],
        "metadata": [],
        "created": tweet['date'],
        "updated": tweet['date'],
        'viewsCount': 0,
        'sharesCount': tweet['retweetCount'],
        'likesCount': tweet['likeCount'],
        'dislikesCount': 0,
        'commentsCount': tweet['replyCount']
    }


def anonymize_twitter(text):
    """
    Anonymize twitter text
    :param text: text to anonymize
    :return: anonymized text
    :rtype: str
    :example:
    >>> anonymize_twitter("Hello @user")
    'Hello user'
    """

    usernames = re.findall(r'@([a-zA-Z0-9_]+)', text)
    for username in usernames:
        text = text.replace(username, "user" + str_to_hash(username))
    return text


def str_to_hash(text):
    return hashlib.shake_256(text.encode()).hexdigest(5)


def jsonify(obj):
    return json.loads(obj)


def timestamp():
    return int(datetime.now().timestamp())


def get_uuid():
    return str(uuid.uuid4())
