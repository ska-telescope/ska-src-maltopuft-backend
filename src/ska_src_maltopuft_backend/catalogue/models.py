"""External catalogue known radio pulse source models."""

import datetime as dt

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ska_src_maltopuft_backend.core.database.base import Base
from ska_src_maltopuft_backend.core.mixins import TimestampMixin


class Catalogue(Base, TimestampMixin):
    """Catalogue model.

    Metadata about external pulsar catalogues.
    """

    __tablename__ = "catalogue"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False, unique=True)

    # Relationships
    catalogue_visits: Mapped[list["CatalogueVisit"]] = relationship(
        back_populates="catalogue",
    )
    known_pulsars: Mapped[list["KnownPulsar"]] = relationship(
        back_populates="catalogue",
    )

    def __repr__(self) -> str:
        """Catalogue repr."""
        return (
            "<Catalogue: "
            f"id={self.id},"
            f"name={self.name},"
            f"url={self.url},"
        )


class CatalogueVisit(Base, TimestampMixin):
    """Catalogue visit model.

    Records the access times of each catalogue.
    """

    __tablename__ = "catalogue_visit"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    visited_at: Mapped[dt.datetime] = mapped_column(nullable=False)

    # Foreign keys
    catalogue_id: Mapped[int] = mapped_column(
        sa.ForeignKey("catalogue.id"),
        nullable=False,
    )

    # Relationships
    catalogue: Mapped["Catalogue"] = relationship(
        back_populates="catalogue_visits",
    )

    def __repr__(self) -> str:
        """CatalogueVisit repr."""
        return (
            "<CatalogueVisit: "
            f"id={self.id},"
            f"visited_at={self.visited_at},"
            f"catalogue_id={self.catalogue_id},"
        )


class KnownPulsar(Base, TimestampMixin):
    """Known pulsar model.

    Records pulsar properties from external catalogues.
    """

    __tablename__ = "known_pulsar"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    dm: Mapped[float] = mapped_column(nullable=True)
    width: Mapped[float] = mapped_column(nullable=True)
    ra: Mapped[str] = mapped_column(sa.Unicode(12), nullable=True)
    dec: Mapped[str] = mapped_column(sa.Unicode(12), nullable=True)
    period: Mapped[float] = mapped_column(nullable=True)

    # Foreign keys
    catalogue_id: Mapped[int] = mapped_column(
        sa.ForeignKey("catalogue.id"),
        nullable=False,
    )

    # Relationships
    catalogue: Mapped["Catalogue"] = relationship(
        back_populates="known_pulsars",
    )

    def __repr__(self) -> str:
        """KnownPulsar repr."""
        return (
            "<KnownPulsar: "
            f"id={self.id},"
            f"name={self.name},"
            f"dm={self.dm},"
            f"width={self.width},"
            f"ra={self.ra},"
            f"dec={self.dec},"
            f"period={self.period},"
            f"catalogue_id={self.catalogue_id},"
        )
