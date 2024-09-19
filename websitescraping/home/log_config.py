import os
import logging

LOG_DIR = 'logs'

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def configure_logger(name):
    # Configure logging
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Capture all levels of logs

    # Check if running in a test environment
    if os.getenv('PYTHON_ENV') == 'test':
        # Disable logging
        logger.disabled = True
        return logger

    # General log file handler
    general_handler = logging.FileHandler(os.path.join(LOG_DIR, f"general.log"))
    general_handler.setLevel(logging.DEBUG)

    # Error log file handler
    error_handler = logging.FileHandler(os.path.join(LOG_DIR, f"error.log"))
    error_handler.setLevel(logging.ERROR)

    # Info log file handler
    info_handler = logging.FileHandler(os.path.join(LOG_DIR, f"general.log"))
    info_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    general_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(general_handler)
    logger.addHandler(error_handler)
    logger.addHandler(info_handler)

    return logger