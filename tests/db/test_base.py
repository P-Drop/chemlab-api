from chemlab_api.db.base import Base


def test_base_metadata_uses_naming_convention() -> None:
    convention = Base.metadata.naming_convention

    assert convention["pk"] == "pk_%(table_name)s"
    assert convention["fk"] == "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"
    assert convention["ck"] == "ck_%(table_name)s_%(constraint_name)s"
