import logging


def setup_logger():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')