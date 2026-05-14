import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Create file handler
file_handler = logging.FileHandler("logs/linkedin.log")

# Optional formatting
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)

# Attach handler to logger
logger.addHandler(file_handler)