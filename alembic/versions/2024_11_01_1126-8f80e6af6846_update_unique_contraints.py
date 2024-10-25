"""Update unique contraints

Revision ID: 8f80e6af6846
Revises: 6d975c10c6ce
Create Date: 2024-11-01 11:26:07.425988

"""

from collections.abc import Sequence

from alembic import op

revision: str = "8f80e6af6846"
down_revision: str | None = "6d975c10c6ce"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Update observation and candidate unique constraints."""
    op.create_unique_constraint(
        op.f("beam_number_key"),
        "beam",
        ["number", "coherent", "ra", "dec", "host_id", "observation_id"],
    )
    op.drop_constraint(
        "candidate_observed_at_beam_id_key", "candidate", type_="unique",
    )
    op.create_unique_constraint(
        op.f("candidate_dm_key"),
        "candidate",
        ["dm", "snr", "width", "ra", "dec", "observed_at", "beam_id"],
    )
    op.create_unique_constraint(
        op.f("host_ip_address_key"), "host", ["ip_address", "hostname"],
    )
    op.create_unique_constraint(
        op.f("meerkat_schedule_block_schedule_block_id_key"),
        "meerkat_schedule_block",
        ["schedule_block_id"],
    )
    op.create_unique_constraint(
        op.f("observation_t_min_key"),
        "observation",
        [
            "t_min",
            "s_ra",
            "s_dec",
            "facility_name",
            "instrument_name",
            "coherent_beam_config_id",
            "schedule_block_id",
        ],
    )
    op.create_unique_constraint(
        op.f("tiling_config_coordinate_type_key"),
        "tiling_config",
        [
            "coordinate_type",
            "epoch",
            "epoch_offset",
            "method",
            "nbeams",
            "overlap",
            "reference_frequency",
            "shape",
            "target",
            "ra",
            "dec",
            "observation_id",
        ],
    )


def downgrade() -> None:
    """Undo updates to observation and candidate unique constraints."""
    op.drop_constraint(
        op.f("tiling_config_coordinate_type_key"),
        "tiling_config",
        type_="unique",
    )
    op.drop_constraint(
        op.f("observation_t_min_key"), "observation", type_="unique",
    )
    op.drop_constraint(
        op.f("meerkat_schedule_block_schedule_block_id_key"),
        "meerkat_schedule_block",
        type_="unique",
    )
    op.drop_constraint(op.f("host_ip_address_key"), "host", type_="unique")
    op.drop_constraint(op.f("candidate_dm_key"), "candidate", type_="unique")
    op.create_unique_constraint(
        "candidate_observed_at_beam_id_key",
        "candidate",
        ["observed_at", "beam_id"],
    )
    op.drop_constraint(op.f("beam_number_key"), "beam", type_="unique")
    # ### end Alembic commands ###
