"""Backend<>database connection integration tests."""

from src.ska_src_maltopuft_backend.core.database import database


def test_ping_db() -> None:
    """Test database connection."""
    assert database.ping_db()

def test_ping_db_from_pool() -> None:
    """Test database connection in get_db dependency."""
    assert database.ping_db_from_pool()
