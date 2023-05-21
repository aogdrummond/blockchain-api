import pytest
from unittest import mock


class TestKeyManager:
    @pytest.mark.parametrize("key_manager", ["BTC", "ETH", "TRO"], indirect=True)
    def test_initialize_private_key_with_existing_key(self, key_manager) -> None:
        """
        Test initializing private key with an existing key.

        Args:
            key_manager: The key manager fixture.

        Returns:
            None
        """
        with mock.patch("cryptography.key_vault.recover_from_s3") as mock_recover:
            crypto_symbol = key_manager["input"]
            mock_recover.return_value = {crypto_symbol: "existing_key"}
            private_key = key_manager["main"].initialize_private_key(crypto_symbol)
            assert private_key == "existing_key"

    @pytest.mark.parametrize("key_manager", ["BTC", "ETH", "TRO"], indirect=True)
    def test_initialize_private_key_without_existing_key(self, key_manager) -> None:
        """
        Test initializing private key without an existing key.

        Args:
            key_manager: The key manager fixture.

        Returns:
            None
        """
        with (
            mock.patch("cryptography.key_vault.recover_from_s3") as mock_recover,
            mock.patch("cryptography.KeyManager.generate_private_key") as mock_generate,
        ):
            crypto_symbol = key_manager["input"]
            mock_recover.return_value = {}
            mock_generate.return_value = "new_key"
            private_key = key_manager["main"].initialize_private_key(crypto_symbol)
            assert private_key == "new_key"

    @pytest.mark.parametrize("key_manager", ["BTC", "ETH", "TRO"], indirect=True)
    def test_recover_private_key(self, key_manager) -> None:
        """
        Test recovering private key.

        Args:
            key_manager: The key manager fixture.

        Returns:
            None
        """
        with mock.patch("cryptography.key_vault.recover_from_s3") as mock_recover:
            crypto_symbol = key_manager["input"]
            mock_recover.return_value = {crypto_symbol: "existing_key"}
            private_key = key_manager["main"].recover_private_key(crypto_symbol)
            assert private_key == "existing_key"

    @pytest.mark.parametrize("key_manager", ["BTC", "ETH", "TRO"], indirect=True)
    def test_generate_private_key(self, key_manager) -> None:
        """
        Test generating private key.

        Args:
            key_manager: The key manager fixture.

        Returns:
            None
        """
        with mock.patch("cryptography.key_vault.persist_on_s3") as mock_persist:
            mock_persist.return_value = None
            private_key = key_manager["main"].generate_private_key(key_manager["input"])
            assert private_key is not None

    @pytest.mark.parametrize("key_manager", ["BTC", "ETH", "TRO"], indirect=True)
    def test_persist_private_key(self, key_manager) -> None:
        """
        Test persisting private key.

        Args:
            key_manager: The key manager fixture.

        Returns:
            None
        """
        with mock.patch("cryptography.key_vault.persist_on_s3") as mock_persist:
            key_manager["main"].persist_private_key("private_key", key_manager["input"])
            mock_persist.assert_called_once_with("private_key", key_manager["input"])
            # asserts that "persist_on_s3" was called one time, and with "private_key"
            # as an argument

class TestCurrencyEncrypter:

    @pytest.mark.parametrize("crypto_n_prefix", [("BTC", ("1", "3", "bc1")),
                                                 ("ETH", "0x"),
                                                 ("TRO", "41")])
    def test_generate_address(self, currencies_encrypter, crypto_n_prefix) -> None:
        """
        Test generating a currency address.

        Args:
            currencies_encrypter: The currencies encrypter fixture.
            crypto_n_prefix: A tuple containing the crypto currency symbol and address prefix.

        Returns:
            None
        """
        def len_is_valid(crypto_symbol: str, result: str) -> bool:
            """
            Check if the length of the generated address is valid for the given crypto currency.

            Args:
                crypto_symbol: The crypto currency symbol.
                result: The generated address.

            Returns:
                True if the length is valid, False otherwise.
            """
            if crypto_symbol == "BTC":
                is_valid = 26 <= len(result) <= 35
            elif crypto_symbol == "ETH":
                is_valid = len(result) > 40
            elif crypto_symbol == "TRO":
                is_valid = len(result) == 42
            else:
                is_valid = False
            return is_valid

        private_key = "my_private_key"
        result = currencies_encrypter.generate_address(crypto_n_prefix[0], private_key)

        assert len_is_valid(crypto_n_prefix[0], result)
        assert isinstance(result, str)
        assert result.startswith(crypto_n_prefix[1])

    def test_bitcoin_generator(self, currencies_encrypter) -> None:
        """
        Test generating a Bitcoin address.

        Args:
            currencies_encrypter: The currencies encrypter fixture.

        Returns:
            None
        """
        with (
            mock.patch("cryptography.random.choice") as mock_choice,
            mock.patch("cryptography.random.randint") as mock_length,
            mock.patch("cryptography.hashlib.sha256") as mock_sha256,
            mock.patch("cryptography.CurrenciesEncrypter.trim_bitcoin_key") as mock_trim,
        ):
            mock_choice.return_value = "1"
            mock_length.return_value = 30
            mock_sha256.return_value.hexdigest.return_value = "generated_hash"
            mock_trim.return_value = "trimmed_key"

            private_key = "private_key"
            generated_address = currencies_encrypter.bitcoin_generator(private_key)

            mock_choice.assert_called_once_with(["1", "3", "bc1"])
            mock_sha256.assert_called_once_with(private_key.encode())
            mock_trim.assert_called_once_with("1generated_hash")
            assert generated_address == "trimmed_key"

    def test_trim_bitcoin_key_long_address(self, currencies_encrypter) -> None:
        """
        Test trimming a long Bitcoin address.

        Args:
            currencies_encrypter: The currencies encrypter fixture.

        Returns:
            None
        """
        public_key = "public_key_with_over_thirty_five_chars"
        trimmed_key = currencies_encrypter.trim_bitcoin_key(public_key)
        assert trimmed_key == public_key[:35]

    def test_trim_bitcoin_key_short_address(self, currencies_encrypter) -> None:
        """
        Test trimming a short Bitcoin address.

        Args:
            currencies_encrypter: The currencies encrypter fixture.

        Returns:
            None
        """
        public_key = "short_public_key"
        trimmed_key = currencies_encrypter.trim_bitcoin_key(public_key)
        assert len(trimmed_key) == 26

    def test_trim_bitcoin_key_tiny_address(self, currencies_encrypter) -> None:
        """
        Test trimming a tiny Bitcoin address.

        Args:
            currencies_encrypter: The currencies encrypter fixture.

        Returns:
            None
        """
        with mock.patch("random.choice") as mock_choice:
            mock_choice.return_value = "."
            public_key = "tiny_public_key"
            trimmed_key = currencies_encrypter.trim_bitcoin_key(public_key)
            assert trimmed_key == public_key + "..........."

    def test_ethereum_generator(self, currencies_encrypter) -> None:
        """
        Test generating an Ethereum address.

        Args:
            currencies_encrypter: The currencies encrypter fixture.

        Returns:
            None
        """
        with mock.patch("cryptography.keccak_256") as mock_keccak:
            dummy_hash = b"22ca8686bfa31a2ae5f55a7f60009e14"
            dummy_address = "3161326165356635356137663630303039653134"
            mock_keccak.return_value.digest.return_value = dummy_hash
            private_key = "private_key"
            generated_address = currencies_encrypter.ethereum_generator(private_key)
            assert generated_address == '0x' + dummy_address

    def test_tron_generator(self, currencies_encrypter) -> None:
        """
        Test generating a Tron address.

        Args:
            currencies_encrypter: The currencies encrypter fixture.

        Returns:
            None
        """
        with mock.patch("cryptography.keccak_256") as mock_keccak:
            dummy_hash = b"22ca8686bfa31a2ae5f55a7f60009e14"
            dummy_address = "3161326165356635356137663630303039653134"
            mock_keccak.return_value.digest.return_value = dummy_hash
            private_key = "private_key"
            generated_address = currencies_encrypter.tron_generator(private_key)
            assert generated_address == '41' + dummy_address
