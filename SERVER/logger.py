import logging
import os
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Configure the root logger
def setup_logger(name=None):
    """
    Set up and return a logger with standardized configuration

    Args:
        name: Logger name (typically __name__ of the calling module)

    Returns:
        A configured logger instance
    """
    logger_name = name if name else "ai_tvts"
    logger = logging.getLogger(logger_name)

    # Only configure if it hasn't been configured yet
    if not logger.handlers:
        # Set the log level
        logger.setLevel(logging.INFO)
        logger.propagate = False

        # Console handler with UTF-8 encoding
        console_handler = logging.StreamHandler()  # Use sys.stderr instead of sys.stdout for better UTF-8 support
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(console_handler)

        # File handler - rotating log files with UTF-8 encoding
        file_handler = RotatingFileHandler(
            os.path.join(logs_dir, f"{logger_name.replace('.', '_')}.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'  # Explicitly set UTF-8 encoding
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)

    return logger
