"""Observation metadata models."""

import datetime as dt
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.mixins import TimestampMixin

if TYPE_CHECKING:
    from ska_src_maltopuft_backend.app.models import Candidate


class ScheduleBlock(Base, TimestampMixin):
    """Schedule block metadata."""

    __tablename__ = "schedule_block"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    start_at: Mapped[dt.datetime] = mapped_column(nullable=False)
    est_end_at: Mapped[dt.datetime] = mapped_column(nullable=False)

    # Relationships
    meerkat_schedule_block: Mapped["MeerkatScheduleBlock"] = relationship(
        back_populates="schedule_block",
    )
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="schedule_block",
    )

    __table_args__ = (sa.UniqueConstraint("start_at", "est_end_at"),)

    def __repr__(self) -> str:
        """ScheduleBlock repr."""
        return (
            "<ScheduleBlock: "
            f"id={self.id},"
            f"start_at={self.start_at},"
            f"est_end_at={self.est_end_at},"
        )


class MeerkatScheduleBlock(Base, TimestampMixin):
    """Meerkat telescope schedule block metadata."""

    __tablename__ = "meerkat_schedule_block"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    meerkat_id: Mapped[int] = mapped_column(nullable=False)
    meerkat_id_code: Mapped[str] = mapped_column(nullable=False)
    proposal_id: Mapped[str] = mapped_column(nullable=False)

    # Foreign keys
    schedule_block_id: Mapped[int] = mapped_column(
        sa.ForeignKey("schedule_block.id"),
        nullable=False,
    )

    # Relationships
    schedule_block: Mapped["ScheduleBlock"] = relationship(
        back_populates="meerkat_schedule_block",
    )

    __table_args__ = (
        sa.UniqueConstraint("meerkat_id"),
        sa.UniqueConstraint("meerkat_id_code"),
    )

    def __repr__(self) -> str:
        """MeerkatScheduleBlock repr."""
        return (
            "<MeerkatScheduleBlock: "
            f"id={self.id},"
            f"meerkat_id={self.meerkat_id},"
            f"meerkat_id_code={self.meerkat_id_code},"
            f"proposal_id={self.proposal_id},"
            f"schedule_block_id={self.schedule_block_id},"
        )


class CoherentBeamConfig(Base, TimestampMixin):
    """Meerkat telescope observation coherent beam configuration."""

    __tablename__ = "coherent_beam_config"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    angle: Mapped[float] = mapped_column(nullable=False)
    fraction_overlap: Mapped[Decimal] = mapped_column(nullable=False)
    x: Mapped[float] = mapped_column(nullable=False)
    y: Mapped[float] = mapped_column(nullable=False)

    # Relationships
    observations: Mapped[list["Observation"]] = relationship(
        back_populates="coherent_beam_config",
    )

    __table_args__ = (
        sa.UniqueConstraint("angle", "fraction_overlap", "x", "y"),
    )

    def __repr__(self) -> str:
        """CoherentBeamConfig repr."""
        return (
            "<CoherentBeamConfig: "
            f"id={self.id},"
            f"angle={self.angle},"
            f"fraction_overlap={self.fraction_overlap},"
            f"x={self.x},"
            f"y={self.y},"
        )


class Observation(Base, TimestampMixin):
    """Observation metadata."""

    __tablename__ = "observation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    dataproduct_type: Mapped[str] = mapped_column(nullable=True)
    dataproduct_subtype: Mapped[str] = mapped_column(nullable=True)
    calib_level: Mapped[int] = mapped_column(nullable=True)
    obs_id: Mapped[str] = mapped_column(nullable=True)
    s_ra: Mapped[str] = mapped_column(nullable=True)
    s_dec: Mapped[str] = mapped_column(nullable=True)
    t_min: Mapped[dt.datetime] = mapped_column(nullable=True)
    t_max: Mapped[dt.datetime] = mapped_column(nullable=True)
    t_exptime: Mapped[dt.timedelta] = mapped_column(nullable=True)
    t_resolution: Mapped[float] = mapped_column(nullable=True)
    em_min: Mapped[float] = mapped_column(nullable=True)
    em_max: Mapped[float] = mapped_column(nullable=True)
    em_resolution: Mapped[float] = mapped_column(nullable=True)
    em_xel: Mapped[int] = mapped_column(nullable=True)
    pol_states: Mapped[str] = mapped_column(nullable=True)
    pol_xel: Mapped[int] = mapped_column(nullable=True)
    facility_name: Mapped[str] = mapped_column(nullable=True)
    instrument_name: Mapped[str] = mapped_column(nullable=True)
    target_name: Mapped[str] = mapped_column(nullable=True)
    target_class: Mapped[str] = mapped_column(nullable=True)

    # Foreign keys
    coherent_beam_config_id: Mapped[int] = mapped_column(
        sa.ForeignKey("coherent_beam_config.id"),
        nullable=False,
    )
    schedule_block_id: Mapped[int] = mapped_column(
        sa.ForeignKey("schedule_block.id"),
        nullable=False,
    )

    # Relationships
    beams: Mapped["Beam"] = relationship(
        back_populates="observation",
    )
    coherent_beam_config: Mapped["CoherentBeamConfig"] = relationship(
        back_populates="observations",
    )
    schedule_block: Mapped["ScheduleBlock"] = relationship(
        back_populates="observations",
    )
    tiling_config: Mapped["TilingConfig"] = relationship(
        back_populates="observation",
    )

    def __repr__(self) -> str:
        """Observation repr."""
        return (
            "<Observation: "
            f"id={self.id},"
            f"schedule_block_id={self.schedule_block_id},"
        )


class TilingConfig(Base, TimestampMixin):
    """Observation tiling configurations."""

    __tablename__ = "tiling_config"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    coordinate_type: Mapped[str] = mapped_column(nullable=False)
    epoch: Mapped[float] = mapped_column(nullable=False)
    epoch_offset: Mapped[float] = mapped_column(nullable=False)
    method: Mapped[str] = mapped_column(nullable=False)
    nbeams: Mapped[int] = mapped_column(nullable=False)
    overlap: Mapped[float] = mapped_column(nullable=False)
    reference_frequency: Mapped[float] = mapped_column(nullable=False)
    shape: Mapped[str] = mapped_column(nullable=False)
    target: Mapped[str] = mapped_column(nullable=False)
    ra: Mapped[str] = mapped_column(nullable=False)
    dec: Mapped[str] = mapped_column(nullable=False)

    # Foreign keys
    observation_id: Mapped[int] = mapped_column(
        sa.ForeignKey("observation.id"),
        nullable=False,
    )

    # Relationships
    observation: Mapped["Observation"] = relationship(
        back_populates="tiling_config",
    )

    def __repr__(self) -> str:
        """TilingConfig repr."""
        return (
            "<TilingConfig: "
            f"id={self.id},"
            f"observation_id={self.observation_id},"
        )


class Beam(Base, TimestampMixin):
    """Observation beam list."""

    __tablename__ = "beam"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    number: Mapped[int] = mapped_column(nullable=False)
    coherent: Mapped[bool] = mapped_column(nullable=False)
    ra: Mapped[str] = mapped_column(nullable=False)
    dec: Mapped[str] = mapped_column(nullable=False)

    # Foreign keys
    host_id: Mapped[int] = mapped_column(
        sa.ForeignKey("host.id"),
        nullable=False,
    )
    observation_id: Mapped[int] = mapped_column(
        sa.ForeignKey("observation.id"),
        nullable=False,
    )

    # Relationships
    candidates: Mapped["Candidate"] = relationship(
        back_populates="beam",
    )
    host: Mapped["Host"] = relationship(
        back_populates="beams",
    )
    observation: Mapped["Observation"] = relationship(
        back_populates="beams",
    )

    def __repr__(self) -> str:
        """Beam repr."""
        return (
            "<Beam: "
            f"id={self.id},"
            f"number={self.number},"
            f"coherent={self.coherent},"
            f"ra={self.ra},"
            f"dec={self.dec},"
            f"host_id={self.host_id},"
            f"observation_id={self.observation_id},"
        )


class Host(Base, TimestampMixin):
    """Observation servers."""

    __tablename__ = "host"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    ip_address: Mapped[str] = mapped_column(nullable=False)
    hostname: Mapped[str] = mapped_column(nullable=True)
    port: Mapped[int] = mapped_column(nullable=False)

    # Relationships
    beams: Mapped["Beam"] = relationship(
        back_populates="host",
    )

    def __repr__(self) -> str:
        """Host repr."""
        return (
            "<Host: "
            f"id={self.id},"
            f"ip_address={self.ip_address},"
            f"hostname={self.hostname},"
            f"port={self.port},"
        )
