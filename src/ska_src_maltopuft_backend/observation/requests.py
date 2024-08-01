"""Observation service request schemas."""

import datetime as dt

from pydantic import PastDatetime

from ska_src_maltopuft_backend.core.schemas import CommonQueryParams


class GetObservationQueryParams(CommonQueryParams):
    """Query parameters for Observation model HTTP GET requests."""

    t_min: PastDatetime | None = None
    t_max: dt.datetime | None = None
