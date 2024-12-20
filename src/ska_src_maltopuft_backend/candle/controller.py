"""Data controller for the Candle models."""

import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.app.models import Candidate, SPCandidate
from ska_src_maltopuft_backend.app.schemas.requests import (
    CreateCandidate,
    CreateSPCandidate,
)
from ska_src_maltopuft_backend.candle.repository import (
    CandidateRepository,
    SPCandidateRepository,
)
from ska_src_maltopuft_backend.core.controller import BaseController
from ska_src_maltopuft_backend.core.schemas import CommonQueryParams
from ska_src_maltopuft_backend.core.types import ModelT
from ska_src_maltopuft_backend.observation.controller import (
    ObservationController,
)

if TYPE_CHECKING:
    from sqlalchemy import Row

logger = logging.getLogger(__name__)


class CandidateController(BaseController[Candidate, CreateCandidate, None]):
    """Data controller for the Candidate model."""

    def __init__(self, repository: CandidateRepository) -> None:
        """Initalise a CandidateController instance."""
        super().__init__(
            model=Candidate,
            repository=repository,
        )
        self.repository = repository


class SPCandidateController(
    BaseController[SPCandidate, CreateSPCandidate, None],
):
    """Data controller for the SPCandidate model."""

    def __init__(
        self,
        repository: SPCandidateRepository,
        observation_controller: ObservationController,
    ) -> None:
        """Initalise a SPCandidateController instance."""
        super().__init__(model=SPCandidate, repository=repository)
        self.repository = repository
        self.observation_controller = observation_controller

    async def _get_latest_observation_id(self, db: Session) -> int | None:
        latest_obs = await self.observation_controller.get_all(
            db=db,
            order_={"desc": ["t_min"]},
            q=[CommonQueryParams(skip=0, limit=1)],
        )
        if len(latest_obs) == 0:
            return None
        return latest_obs[0].id

    def _is_fetch_latest_observation(self, params: dict[str, Any]) -> bool:
        return params.get("latest", False)

    async def _prepare_query_parameters(
        self,
        db: Session,
        params: list[BaseModel] | None = None,
    ) -> dict[str, Any]:
        _params = self._merge_query_parameters(params=params)
        if self._is_fetch_latest_observation(params=_params):
            _params["observation_id"] = [
                await self._get_latest_observation_id(db=db),
            ]
        _ = _params.pop("latest", None)
        return _params

    async def count(
        self,
        db: Session,
        join_: list[str] | None = None,
        q: list[BaseModel] | None = None,
    ) -> int:
        """Return count of objects matching given query parameters."""
        return (
            await self.repository.count(
                db=db,
                join_=join_,
                q=await self._prepare_query_parameters(db=db, params=q),
            )
            or 0
        )

    async def get_all(
        self,
        db: Session,
        join_: list[str] | None = None,
        order_: dict[str, list[str]] | None = None,
        q: list[BaseModel] | None = None,
    ) -> Sequence[ModelT]:
        """Returns a list of records based on query params.

        :param skip: The number of records to skip.
        :param limit: The number of records to return.
        :param join_: The joins to make.
        :param order_: Dict whose keys are sort order and values are lists of
            fields
        :param q: The query parameters.
        :return: A list of records.
        """
        _params = await self._prepare_query_parameters(db=db, params=q)
        if self._is_fetch_latest_observation(params=_params):
            order_ = {"asc": ["candidate.observed_at"]}
        rows: Sequence[Row[ModelT]] = await self.repository.get_all(
            db=db,
            join_=join_,
            order_=order_,
            q=_params,
        )
        logger.info(
            f"Database returned {len(rows)} {self.model_class} objects.",
        )
        return [row[0] for row in rows]
