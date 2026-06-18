from chemlab_api.models.enums import ElementCategory, OrbitalBlock, StandardState


def test_orbital_block_labels() -> None:
    assert [b.value for b in OrbitalBlock] == ["s", "p", "d", "f"]


def test_standard_state_labels() -> None:
    assert [s.value for s in StandardState] == ["solid", "liquid", "gas"]


def test_element_category_has_ten_families() -> None:
    assert len(ElementCategory) == 10
    assert ElementCategory.NOBLE_GAS.value == "Noble gas"
