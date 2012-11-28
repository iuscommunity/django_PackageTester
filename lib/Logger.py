import logging

def get_logger():
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('PackageTester')
    logger.setLevel(getattr(logging, 'INFO'))
    return logger