import logging
import argparse
from logging.config import fileConfig

parser = argparse.ArgumentParser(description='Logging')
parser.add_argument('--logger_name', type=str, default='root')

def main(logger_name):

    if logger_name not in ["root", "logstash_only", "console_only"]:
        raise Exception("logger_name(" + logger_name + ") does not exist")

    fileConfig('logging.conf', disable_existing_loggers=True)
    logger = logging.getLogger(logger_name)
    logger.info("Start")
    try:
        return 1 / 0 ## generate exception
    except Exception as e:
        logger.error(e)
    logger.info("End")

if __name__ == '__main__':
    args = parser.parse_args()
    main(args.logger_name)