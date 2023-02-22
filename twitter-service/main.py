import logging
from time import sleep

from app.config import Config
from app.manager import Manager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message).300s')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logger.info(f'Wainting {Config.SLEEP} seconds')
    sleep(Config.SLEEP)
    # Config.update('CRON', '*/2 * * * *')
    # Config.update('KEYWORDS', ['test', 'test2'])
    # Config.update('FEED_ID', 'feed_id')
    # Config.update('SOURCE_ID', 'source_id')
    manager = Manager()
    manager.start()
