import os
import pytest
from typing import Dict
from dotenv import load_dotenv
from cryptography import KeyManager, CurrenciesEncrypter
from db_mysql import DbCursor

load_dotenv()

@pytest.fixture
def key_manager(request) -> Dict[str, KeyManager]:
    """
    Fixture for KeyManager.

    Args:
        request: pytest request object.

    Returns:
        dict: A dictionary containing 'main' and 'input' keys with KeyManager objects.
    """
    return {"main": KeyManager(request.param), "input": request.param}

@pytest.fixture
def currencies_encrypter() -> CurrenciesEncrypter:
    """
    Fixture for CurrenciesEncrypter.

    Returns:
        CurrenciesEncrypter: CurrenciesEncrypter object.
    """
    return CurrenciesEncrypter()

@pytest.fixture
def db() -> DbCursor:
    """
    Fixture for DbCursor.

    Returns:
        DbCursor: DbCursor object.
    """
    db = DbCursor(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("TEST_DB_NAME"),
    )
    return db