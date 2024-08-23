"""Data controller for the Observation metadata models."""

from typing import Any

from sqlalchemy.orm import Session

from ska_src_maltopuft_backend.app.schemas.requests import (
    GetKnownPulsarQueryParams,
)
from ska_src_maltopuft_backend.catalogue.controller import (
    KnownPulsarController,
)
from ska_src_maltopuft_backend.core.controller import BaseController

from .models import Observation
from .repository import ObservationRepository


class ObservationController(BaseController[Observation, None, None]):
    """Data controller for the Observation model."""

    def __init__(
        self,
        repository: ObservationRepository,
        known_pulsar_controller: KnownPulsarController,
    ) -> None:
        """Initalise a ObservationController instance."""
        super().__init__(
            model=Observation,
            repository=repository,
        )
        self.repository = repository
        self.pulsar_controller = known_pulsar_controller

    async def get_sources_by_id(
        self,
        db: Session,
        ids_: list[int],
        radius: float,
    ) -> list[dict[str, Any | list[dict[str, Any]]]]:
        """Returns known sources within a radius of list of observation ids."""
        db_obj = await self.get_by_id_multi(
            db=db,
            ids_=ids_,
        )

        res: list[dict[str, Any | list[dict[str, Any]]]] = []
        for obs in db_obj:
            params = GetKnownPulsarQueryParams(
                ra=obs.s_ra,
                dec=obs.s_dec,
                radius=radius,
            )
            results_dict: dict[str, Any | list[dict[str, Any]]] = {}
            obs_dict = obs.__dict__
            pulsars = await self.pulsar_controller.get_all(db=db, q=[params])
            observation_pulsars: list[dict[str, Any]] = []
            for ps in pulsars:
                ps_dict = ps.__dict__
                observation_pulsars.append(ps_dict)

            results_dict["observation"] = obs_dict
            results_dict["sources"] = observation_pulsars
            res.append(results_dict)

        return res
