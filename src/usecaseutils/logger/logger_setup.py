import logging

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s',
    datefmt='%d-%m-%y %H:%M:%S')

preprocess_logger = logging.getLogger('preprocess')
training_logger = logging.getLogger('training')
predict_logger = logging.getLogger('predict')
