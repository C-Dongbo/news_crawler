import logging
from logging.config import fileConfig


def main(logger_name):

    if logger_name not in ["root", "logstashOnly", "consoleOnly"]:
        raise Exception("logger_name(" + logger_name + ") does not exist")

    fileConfig('logging.conf', disable_existing_loggers=True)
    logger = logging.getLogger(logger_name)
    logger.info("App Start")
    try:
        return 1 / 0 ## generate exception
    except Exception as e:
        logger.error(e)
    logger.info("App End")

if __name__ == '__main__':
    main()