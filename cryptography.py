import random
import logging
import hashlib
import key_vault
from typing import Optional
from sha3 import keccak_256
from secrets import token_bytes
from coincurve import PublicKey
from string import ascii_letters

logger = logging.getLogger()
logger.setLevel("INFO")


class KeyManager:
    def __init__(self, crypto_symbol: str, seed: Optional[int] = None) -> None:
        """
        Initializes a KeyManager object.

        Args:
            crypto_symbol (str): The symbol of the cryptocurrency.
            seed (int, optional): Seed for the random number generator. Defaults to None.
        """
        random.seed(seed)
        self.private_key: str = self.initialize_private_key(crypto_symbol)

    def initialize_private_key(self, crypto_symbol: str) -> str:
        """
        Initializes the private key.

        Args:
            crypto_symbol (str): The symbol of the cryptocurrency.

        Returns:
            str: The initialized private key.
        """
        private_key = self.recover_private_key(crypto_symbol)
        if private_key:
            return private_key
        else:
            return self.generate_private_key(crypto_symbol)

    def recover_private_key(self, crypto_currency: str) -> str:
        """
        Recovers the private key from the S3 bucket.

        Args:
            crypto_currency (str): The symbol of the cryptocurrency.

        Returns:
            str: The recovered private key if it exists in the S3 bucket, otherwise an empty string.
        """
        private_keys = key_vault.recover_from_s3()
        private_key = private_keys.get(crypto_currency, "")
        return private_key

    def generate_private_key(self, crypto_currency: Optional[str] = None) -> str:
        """
        Generates a random private key.

        Args:
            crypto_currency (str, optional): The symbol of the cryptocurrency. Defaults to None.

        Returns:
            str: The generated private key.
        
        Raises:
            ValueError: If the cryptocurrency symbol is invalid.
        """
        length = random.randint(0, 100)
        dummy_str = "".join([random.choice(ascii_letters) for _ in range(length)])
        if crypto_currency in ["ETH", "TRO"]:
            private_key = hashlib.sha256(str(dummy_str).encode()).hexdigest()
        elif crypto_currency == "BTC":
            private_key = keccak_256(token_bytes(32)).digest().hex()
        else:
            raise ValueError("Invalid cryptocurrency")
        self.persist_private_key(private_key, crypto_currency)
        logger.warning("Fresh private key created.")
        return private_key

    def persist_private_key(self, private_key: str, crypto_currency: str) -> None:
        """
        Persists the private key in the S3 bucket.

        Args:
            private_key (str): The private key to persist.
            crypto_currency (str): The symbol of the cryptocurrency.
        """
        key_vault.persist_on_s3(private_key, crypto_currency)

class CurrenciesEncrypter:
    def __init__(self, seed: Optional[int] = None) -> None:
        """
        Initializes a CurrenciesEncrypter object.

        Args:
            seed (int, optional): Seed for the random number generator. Defaults to None.
        """
        random.seed(seed)

    def generate_address(self, crypto_symbol: str, private_key: str) -> str:
        """
        Generates an address for the given cryptocurrency symbol and private key.

        Args:
            crypto_symbol (str): The cryptocurrency symbol.
            private_key (str): The private key.

        Returns:
            str: The generated address for the given cryptocurrency and private key.
        """
        crypto_mapping = {
            "BTC": self.bitcoin_generator,
            "ETH": self.ethereum_generator,
            "TRO": self.tron_generator,
        }

        generate_address = crypto_mapping[crypto_symbol]
        return generate_address(private_key)

    def bitcoin_generator(self, private_key: str) -> str:
        """
        Generates a Bitcoin address according to Bitcoin rules.

        Args:
            private_key (str): The private key.

        Returns:
            str: The generated Bitcoin address.
        """
        prefix = random.choice(["1", "3", "bc1"])
        length = random.randint(25, 34)
        generated_hash = hashlib.sha256(private_key.encode()).hexdigest()
        public_key = self.trim_bitcoin_key(prefix + generated_hash[-length:])
        logger.info("Bitcoin address generated.")
        return public_key

    def trim_bitcoin_key(self, public_key: str) -> str:
        """
        Trims the Bitcoin address if it exceeds the maximum length or adds missing characters if it's too short.

        Args:
            public_key (str): The Bitcoin address.

        Returns:
            str: The trimmed Bitcoin address.
        """
        if len(public_key) > 35:
            trimmed_key = public_key[:35]
        elif len(public_key) < 26:
            missing_chars = 26 - len(public_key)
            trimmed_key = public_key + "".join(
                [random.choice(ascii_letters) for _ in range(missing_chars)]
            )
        else:
            return public_key
        return trimmed_key

    def ethereum_generator(self, private_key: str) -> str:
        """
        Generates an address according to Ethereum rules.

        Args:
            private_key (str): The private key.

        Returns:
            str: The generated Ethereum address.
        """
        public_key = PublicKey.from_valid_secret(private_key.encode()).format(
            compressed=False)[1:]
        address = keccak_256(public_key).digest()
        address = "0x" + address[-20:].hex()
        logger.info("Ethereum address generated.")
        return address

    def tron_generator(self, private_key: str) -> str:
        """
        Generates an address according to Tron rules.

        Args:
            private_key (str): The private key.

        Returns:
            str: The generated Tron address.
        """
        public_key = PublicKey.from_valid_secret(private_key.encode()).format(
            compressed=False)[1:]
        address = keccak_256(public_key).digest()[-20:].hex()
        address = "41" + address
        logger.info("Tron address generated.")
        return address