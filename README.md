
# Cryptocurrency Key Management Project

This project aims to provide functionality for managing cryptocurrency keys, including generating addresses, persisting keys, and retrieving keys from a database or an S3 bucket. It consists of several scripts that can be used independently or integrated into a larger application.

## Prerequisites

- Python 3.x
- MySQL server (if using the `db_mysql.py` script)
- AWS S3 bucket (if using the `key_vault.py` script)

## Installation

1. Clone the repository:

    <div align="center">

   ```bash
   git clone https://github.com/aogdrummond/blockchain-api.git
   ```
2. Navigate to the project directory:
    <div align="center">

    ```bash
    cd blockchain-api
    ```
3. Install the required dependencies:
    <div align="center">

    ```bash
    pip install -r requirements.txt
    ```
Set up the necessary environment variables:

* Create a .env file in the project root directory.

* Add the following variables and their corresponding values:

```
# For the key_vault.py script
ACCESS_KEY_ID=your_access_key_id
SECRET_ACCESS_KEY=your_secret_access_key
BUCKET_NAME=your_bucket_name

# For the db_mysql.py script
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=your_database_name
```
# Usage
## KeyManager
The `cryptography.py` script provides a `KeyManager` class for managing cryptocurrency keys.
```
from cryptography import KeyManager

# Create an instance of KeyManager
key_manager = KeyManager(crypto_symbol="BTC", seed=12345)

# Generate or recover a private key
private_key = key_manager.private_key

# Generate an address for a given cryptocurrency and private key
address = key_manager.generate_address(crypto_symbol="BTC", private_key=private_key)
```
# CurrenciesEncrypter

The `cryptography.py` script provides a `CurrenciesEncrypter` class for generating addresses for different cryptocurrencies.
```
from cryptography import CurrenciesEncrypter

# Create an instance of CurrenciesEncrypter
encrypter = CurrenciesEncrypter(seed=54321)

# Generate a Bitcoin address
bitcoin_address = encrypter.generate_address(crypto_symbol="BTC", private_key="my_private_key")

# Generate an Ethereum address
ethereum_address = encrypter.generate_address(crypto_symbol="ETH", private_key="my_private_key")
```

# DbCursor
The `db_mysql.py` script provides a `DbCursor` class for interacting with a MySQL database to persist and retrieve addresses.
```
from db_mysql import DbCursor

# Create an instance of DbCursor
cursor = DbCursor(
    host="your_database_host",
    user="your_database_user",
    password="your_database_password",
    database="your_database_name"
)

# Persist an address on the database
cursor.persist_on_database(address="my_address", crypto="BTC")

# Retrieve an address from the database by ID
address = cursor.retrieve_address(id=1)

# List all addresses from the database
addresses = cursor.list_all_addresses()
```

# Key Vault
The `key_vault.py` script provides functions for persisting and retrieving the private keys used to generate the addresses. It generates a new private key if it does not exist for the cryptocurrency, or utilize the one already saved in the storage.
```
from cryptography import persist_on_s3, recover_from_s3

# Persist a private key on the S3 bucket
persist_on_s3(key="my_private_key", crypto_currency="BTC")

# Recover a private key from the S3 bucket
private_key = recover_from_s3()
```
Please note that the database and AWS S3 bucket configurations should be set up and the corresponding environment variables should be provided for the scripts to work correctly.

# Contributing
Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

# License
This project is licensed under the MIT License.
