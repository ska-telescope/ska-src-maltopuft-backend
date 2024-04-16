"""MALTOPUFT API source code"""

import logging

from ska_ser_logging import configure_logging

configure_logging(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.info(f"Initialised logger for {__name__}")
