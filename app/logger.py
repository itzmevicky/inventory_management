import structlog



def get_logger(name: str | None = None):
    """
    Usage:
        logger = get_logger(__name__)
        logger.info("user created", user_id=123, email="a@b.com")
    """
    return structlog.get_logger(name)