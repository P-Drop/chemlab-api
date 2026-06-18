"""Enum types for the Element model, mapped to native PostgreSQL enums."""

from enum import StrEnum


class ElementCategory(StrEnum):
    """The 10 element families (PubChem `GroupBlock')."""

    ALKALI_METAL = "Alcali metal"
    ALKALINE_EARTH_METAL = "Alkaline earth metal"
    TRANSITION_METAL = "Transition metal"
    POST_TRANSITION_METAL = "Post-transition metal"
    METALLOID = "Metalloid"
    NONMETAL = "Nonmetal"
    HALOGEN = "Halogen"
    NOBLE_GAS = "Noble gas"
    LANTHANIDE = "Lanthanide"
    ACTINIDE = "Actinide"


class StandardState(StrEnum):
    """Physical state at standard conditions."""

    SOLID = "solid"
    LIQUID = "liquid"
    GAS = "gas"


class OrbitalBlock(StrEnum):
    """Periodic table block."""

    S = "s"
    P = "p"
    D = "d"
    F = "f"
