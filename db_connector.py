import os
from dotenv import load_dotenv
from db_mysql import DbCursor

load_dotenv()

cursor = DbCursor(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME"),
)


def persist_address_on_db(address: str, crypto_currency: str) -> str:
    """
    Persists an address on the database for the given cryptocurrency.

    Args:
        address (str): The address to persist.
        crypto_currency (str): The cryptocurrency associated with the address.

    Returns:
        str: The success message indicating if the address was successfully persisted or not.
    """
    cursor.persist_on_database(address, crypto_currency)


def list_addresses_from_db() -> list:
    """
    Lists all addresses from the database.

    Returns:
        list: A list of addresses stored in the database.
    """
    addresses = cursor.list_all_addresses()
    return addresses


def retrieve_address_from_id(id: int) -> str:
    """
    Retrieves an address from the database based on the given ID.

    Args:
        id (int): The ID of the address.

    Returns:
        str: The retrieved address.
    """
    address = cursor.retrieve_address(id)
    return address