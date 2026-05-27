import structlog
import logging
from backend.config import settings


def setup_logging():
    """Configure structured logging for the application."""
    
    log_level = getattr(settings, 'LOG_LEVEL', 'INFO')
    environment = getattr(settings, 'ENVIRONMENT', 'development')
    
    # Convert string log level to numeric value
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if environment == "development" 
            else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(numeric_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=False,
    )
    
    logger = structlog.get_logger()
    logger.info("logging_initialized", level=log_level, environment=environment)
    
    return logger
