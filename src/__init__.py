"""Package initialisation routine."""

import logging

from ska_ser_logging import configure_logging

PACKAGE_NAME = "ska.ska-src-maltopuft-backend"

configure_logging(logging.DEBUG)

logger = logging.getLogger(PACKAGE_NAME)
logger.info(f"Initalised logger for {PACKAGE_NAME}")
