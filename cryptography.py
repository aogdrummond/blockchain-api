import hashlib
import random
import uuid
import logging
import key_vault
from string import ascii_letters
from Crypto.Hash import keccak

SEED = 42

logger = logging.getLogger()
logger.setLevel("INFO")

class KeyManager:
    """
    Manages the private key for encryption.

    This encapsulation allows dealing with the private key in an isolated manner,
    enabling the creation or retrieval of the key independently of the user.
    """
    def __init__(self):
        random.seed(SEED)
        self.private_key: str = self.initialize_private_key()

    def initialize_private_key(self) -> str:
        """
        Initializes the private key.

        Returns:
            str: The initialized private key.
        """
        private_key = self.recover_private_key()
        if private_key:
            return private_key
        else:
            return self.generate_private_key()

    def recover_private_key(self) -> str:
        """
        Recovers the private key from the S3 bucket.

        Returns:
            str: The recovered private key if it exists in the S3 bucket, otherwise None.
        """
        private_key = key_vault.recover_from_s3()
        return private_key

    def generate_private_key(self) -> str:
        """
        Generates a random private key.

        Returns:
            str: The generated private key.
        """
        length = random.randint(0, 100)
        dummy_str = "".join([random.choice(ascii_letters) for _ in range(length)])
        private_key = hashlib.sha256(str(dummy_str).encode()).hexdigest()
        self.persist_private_key(private_key)
        logger.warning("Fresh private key created.")
        return private_key

    def persist_private_key(self, private_key: str):
        """
        Persists the private key in the S3 bucket.

        Args:
            private_key (str): The private key to persist.
        """
        key_vault.persist_on_s3(private_key)
        
class CurrenciesEncrypter:
    def __init__(self):
        random.seed(SEED)

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
            "TRO": self.tron_generator
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
        generated_hash = hashlib.sha256("".join([private_key, prefix, length.__str__()]).encode()).hexdigest()
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
            trimmed_key = public_key + "".join([random.choice(ascii_letters) for _ in range(missing_chars)])
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
        k = keccak.new(digest_bits=256)
        random_id = uuid.uuid1().__str__()
        hashed_str = "".join([private_key, random_id])
        k.update(hashed_str.encode('utf-8'))
        hash = k.hexdigest().encode('utf-8').hex()
        public_key = "".join(["0x", hash])
        logger.info("Ethereum address generated.")
        return public_key

    def tron_generator(self, private_key: str) -> str:
        """
        Generates an address according to Tron rules.

        Args:
            private_key (str): The private key.

        Returns:
            str: The generated Tron address.
        """
        k = keccak.new(digest_bits=256)
        random_id = uuid.uuid1().__str__()
        hashed_str = "".join([private_key, random_id])
        k.update(hashed_str.encode('utf-8'))
        hash = k.hexdigest().encode('utf-8')[-20:].hex()
        public_key = "".join(["41", hash])
        logger.info("Tron address generated.")
        return public_key
