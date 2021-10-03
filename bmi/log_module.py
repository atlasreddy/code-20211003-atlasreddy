import os
import logging
from bmi.config import Configuration as conf

os.makedirs(conf.LOG_DIR, exist_ok=True)


class LogModule:
    @staticmethod
    def get_logger(name):
        logging.basicConfig()
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(os.path.join(conf.LOG_DIR, conf.LOG_FILE))
        file_log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        file_handler.setFormatter(file_log_formatter)
        logger.addHandler(file_handler)
        return logger
