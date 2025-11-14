"""src/logger_config.py
Configure stdlib logging and structlog and expose a `logger` instance.
"""
import logging
import structlog

def configure_logging():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )
    return structlog.get_logger()

logger = configure_logging()
