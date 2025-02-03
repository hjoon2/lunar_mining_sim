import logging

logger = logging.getLogger(__name__)

def setup_logging(log_level):
    """Configure logging for the application."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(levelname)s - %(message)s"
    )