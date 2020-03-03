import logging

logging.basicConfig(
    level=logging.INFO, 
    format='[%(asctime)s] [%(levelname)s] %(message)s', 
    datefmt="%a, %d %b %Y %H:%M:%S")

basic_logger = logging.getLogger(__name__)