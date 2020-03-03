import logging


basic_logger = logging.getLogger("basic_logger")
basic_logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] %(message)s', datefmt="%a, %d %b %Y %H:%M:%S")
handler.setFormatter(formatter)

basic_logger.addHandler(handler)