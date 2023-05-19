import pytest
import os
import sys
current_file = os.path.abspath(__file__)
grandparent_dir = os.path.dirname(os.path.dirname(current_file))
sys.path.insert(0,grandparent_dir)
from dotenv import load_dotenv
from cryptography import KeyManager, CurrenciesEncrypter
from db_mysql import DbCursor

load_dotenv()
@pytest.fixture
def key_manager():
    return KeyManager()

@pytest.fixture
def currencies_encrypter():
    return CurrenciesEncrypter()

@pytest.fixture
def db():
    db = DbCursor(host=os.environ.get("DB_HOST"),
                  user=os.environ.get("DB_USER"),
                  password=os.environ.get("DB_PASSWORD"),
                  database =os.environ.get("TEST_DB_NAME"))
    return db