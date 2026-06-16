from chemlab_api.core.config import Settings


def test_database_url_assembles_async_postgres_url() -> None:
    settings = Settings(
        postgres_host="localhost",
        postgres_port=5432,
        postgres_user="u",
        postgres_password="p@ss:word/!",
        postgres_db="chem",
    )
    url = settings.database_url

    assert url.drivername == "postgresql+asyncpg"
    assert url.username == "u"
    assert url.password == "p@ss:word/!"
    assert url.host == "localhost"
    assert url.port == 5432
    assert url.database == "chem"
    # str () masks the password; the URL object keeps the real value
    assert "p@ss" not in str(url)
