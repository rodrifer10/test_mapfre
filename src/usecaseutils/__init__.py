import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s',
                    datefmt='%d-%m-%y %H:%M:%S')

__all__ = [
    'data',
    'utils',
]
