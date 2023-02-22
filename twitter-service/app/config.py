from environs import Env

env = Env()


class Config:
    CRON = env.str('CRON', None)
    KEYWORDS = [keyword.strip() for keyword in env.str('KEYWORDS', '').split(',')]
    FEED_ID = env.str('FEED_ID', None)
    SOURCE_ID = env.str('SOURCE_ID', None)

    CONSUME = env('CONSUME', 'config')
    PRODUCE = env('PRODUCE', 'article_raw_xx')
    CLIENT_ID = env('CLIENT_ID', 'twitter_service')

    KAFKA_HOST = env('KAFKA_HOST', '127.0.0.1:3501')
    SCHEMA_REGISTRY = env('SCHEMA_REGISTRY', 'http://localhost:8081')  # 3502')
    PARTITIONER = env("PARTITIONER", "random")
    MESSAGE_MAX_BYTES = env.int('MESSAGE_MAX_BYTES', 1000000)
    HEARTBEAT_INTERVAL = env.int('HEARTBEAT_INTERVAL', 10)
    OFFSET_TYPE = env('OFFSET_TYPE', 'earliest')

    SLEEP = env.int('SLEEP', 20)

    @staticmethod
    def update(name, value):
        setattr(Config, name, value)
