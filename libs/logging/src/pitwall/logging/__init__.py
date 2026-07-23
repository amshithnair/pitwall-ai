"""PitWall AI Logging Utilities."""
import logging

import structlog


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structlog for the application."""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(level=log_level.upper())
