from sqlalchemy import CheckConstraint, Table

from chemlab_api.db.base import Base
from chemlab_api.models import Element


def test_element_registered_on_metadata() -> None:
    assert Element.__tablename__ == "element"
    assert "element" in Base.metadata.tables


def test_element_has_three_check_constraints() -> None:
    table: Table = Base.metadata.tables["element"]
    checks = [c for c in table.constraints if isinstance(c, CheckConstraint)]
    assert len(checks) == 3


def test_element_unique_altenate_keys() -> None:
    table: Table = Base.metadata.tables["element"]
    assert table.c["atomic_number"].unique
    assert table.c["symbol"].unique
