"""Fake observation metadata generators."""

from typing import Any

from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from ska_src_maltopuft_backend.app.models import (
    Beam,
    CoherentBeamConfig,
    Host,
    Observation,
    ScheduleBlock,
)


def set_sqlalchemy_factory_args(
    data: dict[str, Any],
    **kwargs: dict[str, Any],
) -> dict[str, Any]:
    """Set SQLAlchemy model factory arguments from kwargs."""
    for arg, value in kwargs.items():
        if arg not in data:
            continue
        if value is None:
            continue
        if value == "":
            data[arg] = None
        else:
            data[arg] = value
    return {k: v for k, v in data.items() if k not in "_sa_instance_state"}


class ScheduleBlockFactory(SQLAlchemyFactory[ScheduleBlock]):
    """ScheduleBlock SQLAlchemy model factory."""


def sb_data_generator(**kwargs: Any) -> ScheduleBlock:
    """Generate fake schedule block data."""
    data = ScheduleBlockFactory.build().__dict__
    return ScheduleBlock(
        **set_sqlalchemy_factory_args(data, **kwargs),
    )


class ObservationFactory(SQLAlchemyFactory[Observation]):
    """Observation SQLAlchemy model factory."""


def obs_data_generator(**kwargs: Any) -> Observation:
    """Generate fake observation data."""
    data = ObservationFactory.build().__dict__
    return Observation(
        **set_sqlalchemy_factory_args(data, **kwargs),
    )


class CoherentBeamConfigFactory(SQLAlchemyFactory[CoherentBeamConfig]):
    """CoherentBeamConfig SQLAlchemy model factory."""


def cb_config_data_generator(**kwargs: Any) -> CoherentBeamConfig:
    """Generate fake coherent beam configuration data."""
    data = CoherentBeamConfigFactory.build().__dict__
    return CoherentBeamConfig(
        **set_sqlalchemy_factory_args(data, **kwargs),
    )


class HostFactory(SQLAlchemyFactory[Host]):
    """Host SQLAlchemy model factory."""


def host_data_generator(**kwargs: Any) -> Host:
    """Generate fake host data."""
    data = HostFactory.build().__dict__
    return Host(
        **set_sqlalchemy_factory_args(data, **kwargs),
    )


class BeamFactory(SQLAlchemyFactory[Beam]):
    """Beam SQLAlchemy model factory."""


def beam_data_generator(**kwargs: Any) -> Beam:
    """Generate fake beam data."""
    data = BeamFactory.build().__dict__
    return Beam(
        **set_sqlalchemy_factory_args(data, **kwargs),
    )
