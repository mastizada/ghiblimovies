"""Settings related utilities."""
import logging


class ErrorOnlyLogFilter(logging.Filter):
    """Log only error and critical messages."""

    def filter(self, record) -> int:
        if record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            return 1
        return 0  # do not log
