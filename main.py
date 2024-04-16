"""Entrypoint to the ska-src-maltopuft-backend application."""

import logging

import uvicorn
from ska_ser_logging import configure_logging

if __name__ == "__main__":
    configure_logging(logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info(f"Initialised logger for process {__name__}")

    uvicorn.run(
        app="src.ska_src_maltopuft_backend.core.server:app",
        reload=True,
        workers=1,
        host="0.0.0.0",
    )
