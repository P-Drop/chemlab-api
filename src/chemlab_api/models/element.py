"""The Element ORM model (ADR-0004)."""

import enum
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Double,
    Enum,
    Identity,
    SmallInteger,
    String,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from chemlab_api.db.base import Base
from chemlab_api.models.enums import ElementCategory, OrbitalBlock, StandardState


def _enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    """Use the enum *values* (not member names) as native PG enum labels."""
    return [str(member.value) for member in enum_cls]


class Element(Base):
    """A chemical element (ADR-0004)"""

    __tablename__ = "element"

    __table_args__ = (
        CheckConstraint("atomic_number BETWEEN 1 AND 118", name="atomic_number_range"),
        CheckConstraint("period BETWEEN 1 AND 7", name="period_range"),
        CheckConstraint("group_number BETWEEN 1 AND 18", name="group_number_range"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)

    atomic_number: Mapped[int] = mapped_column(SmallInteger, unique=True)
    symbol: Mapped[str] = mapped_column(String(3), unique=True)
    name_en: Mapped[str] = mapped_column(String(50))
    name_es: Mapped[str] = mapped_column(String(50))

    period: Mapped[int] = mapped_column(SmallInteger)
    group_number: Mapped[int | None] = mapped_column(SmallInteger)
    block: Mapped[OrbitalBlock] = mapped_column(
        Enum(OrbitalBlock, name="orbital_block", values_callable=_enum_values)
    )

    electron_configuration: Mapped[str] = mapped_column(String(50))
    atomic_mass: Mapped[float] = mapped_column(Double)

    electronegativity: Mapped[float | None] = mapped_column(Double)
    atomic_radius: Mapped[float | None] = mapped_column(Double)
    ionization_energy: Mapped[float | None] = mapped_column(Double)
    electron_affinity: Mapped[float | None] = mapped_column(Double)

    category: Mapped[ElementCategory] = mapped_column(
        Enum(ElementCategory, name="element_category", values_callable=_enum_values)
    )
    standard_state: Mapped[StandardState] = mapped_column(
        Enum(StandardState, name="standard_state", values_callable=_enum_values)
    )
    state_is_predicted: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
