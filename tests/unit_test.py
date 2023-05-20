import pytest
from unittest import mock

class TestKeyManager:

    def test_initialize_private_key_with_existing_key(self,key_manager):
        with mock.patch("cryptography.key_vault.recover_from_s3") as mock_recover:
            mock_recover.return_value = "existing_key"
            private_key = key_manager.initialize_private_key()
            assert private_key == "existing_key"

    def test_initialize_private_key_without_existing_key(self,key_manager):
        with mock.patch("cryptography.key_vault.recover_from_s3") as mock_recover, \
                mock.patch("cryptography.KeyManager.generate_private_key") as mock_generate:
            mock_recover.return_value = None
            mock_generate.return_value = "new_key"
            private_key = key_manager.initialize_private_key()
            assert private_key == "new_key"

    def test_recover_private_key(self,key_manager):
        with mock.patch("cryptography.key_vault.recover_from_s3") as mock_recover:
            mock_recover.return_value = "existing_key"
            private_key = key_manager.recover_private_key()
            assert private_key == "existing_key"

    def test_generate_private_key(self,key_manager):
        with mock.patch("cryptography.key_vault.persist_on_s3") as mock_persist:
            mock_persist.return_value = None
            private_key = key_manager.generate_private_key()
            print(f"Key {private_key}")
            assert private_key is not None

    def test_persist_private_key(self,key_manager):
        with mock.patch("cryptography.key_vault.persist_on_s3") as mock_persist:
            key_manager.persist_private_key("private_key")
            mock_persist.assert_called_once_with("private_key")
            #asserts that "persist_on_s3" was called one time, and with "private_key"
            #as argument



class TestCurrencyEncrypter:

    @pytest.mark.parametrize("crypto_n_prefix", [("BTC",("1","3","bc1")), 
                                                 ("ETH","0x"),
                                                 ("TRO","41")])
    def test_generate_address(self, currencies_encrypter, crypto_n_prefix):
        def len_is_valid(crypto_symbol,result):
            if crypto_symbol == "BTC":
                is_valid = (26 <= len(result) <= 35)
            if crypto_symbol == "ETH":
                is_valid = (len(result) > 40)
            if crypto_symbol == "TRO":
                is_valid = (len(result) == 42)
            return is_valid

        private_key = "my_private_key"

        result = currencies_encrypter.generate_address(crypto_n_prefix[0], private_key)

        assert len_is_valid(crypto_n_prefix[0],result)
        assert isinstance(result, str)
        assert result.startswith(crypto_n_prefix[1])
        


    def test_bitcoin_generator(self,currencies_encrypter):
        with mock.patch("cryptography.random.choice") as mock_choice, \
                mock.patch("cryptography.random.randint") as mock_length, \
                mock.patch("cryptography.hashlib.sha256") as mock_sha256, \
                mock.patch("cryptography.CurrenciesEncrypter.trim_bitcoin_key") as mock_trim:
                
            mock_choice.return_value = "1"
            mock_length.return_value = 30
            mock_sha256.return_value.hexdigest.return_value = "generated_hash"
            mock_trim.return_value = "trimmed_key"

            private_key = "private_key"
            generated_address = currencies_encrypter.bitcoin_generator(private_key)

            mock_choice.assert_called_once_with(["1", "3", "bc1"])
            mock_sha256.assert_called_once_with("".join([private_key, "1", "30"]).encode())
            mock_trim.assert_called_once_with("1generated_hash")
            assert generated_address == "trimmed_key"


    def test_trim_bitcoin_key_long_address(self,currencies_encrypter):
        public_key = "public_key_with_over_thirty_five_chars"
        trimmed_key = currencies_encrypter.trim_bitcoin_key(public_key)
        assert trimmed_key == public_key[:35]

    def test_trim_bitcoin_key_short_address(self,currencies_encrypter):
        public_key = "short_public_key"
        trimmed_key = currencies_encrypter.trim_bitcoin_key(public_key)
        assert len(trimmed_key) == 26

    def test_trim_bitcoin_key_tiny_address(self,currencies_encrypter):
        with mock.patch("random.choice") as mock_choice:
            mock_choice.return_value = "."
            public_key = "tiny_public_key"
            trimmed_key = currencies_encrypter.trim_bitcoin_key(public_key)
            assert trimmed_key == public_key + "..........."
#

    def test_ethereum_generator(self,currencies_encrypter):
        with mock.patch("cryptography.keccak.new") as mock_keccak, \
                mock.patch("cryptography.uuid.uuid1") as mock_uuid:
            mock_uuid.return_value.__str__.return_value = "random_id"
            mock_keccak.return_value.hexdigest.return_value.encode.return_value.hex.return_value = "hash"
            mock_keccak.return_value.update.return_value = None

            private_key = "private_key"
            generated_address = currencies_encrypter.ethereum_generator(private_key)

            mock_uuid.assert_called_once_with()
            mock_uuid.return_value.__str__.assert_called_once_with()
            mock_keccak.assert_called_once_with(digest_bits=256)
            mock_keccak.return_value.hexdigest.assert_called_once_with()
            assert generated_address == "0xhash"

    def test_tron_generator(self,currencies_encrypter):
        
        with mock.patch("cryptography.keccak.new") as mock_keccak, \
                mock.patch("cryptography.uuid.uuid1") as mock_uuid:
            mock_uuid.return_value.__str__.return_value = "random_id"
            # mock_keccak.return_value.hexdigest.return_value.encode.return_value = "hash".encode("utf-8")[-20:].hex()
            mock_keccak.return_value.hexdigest.return_value.encode('utf-8')[-20:].hex.return_value = "hash"
            mock_keccak.return_value.update.return_value = None

            private_key = "private_key"
            generated_address = currencies_encrypter.tron_generator(private_key)

            mock_uuid.assert_called_once_with()
            mock_uuid.return_value.__str__.assert_called_once_with()
            mock_keccak.assert_called_once_with(digest_bits=256)
            mock_keccak.return_value.hexdigest.assert_called_once_with()
            assert generated_address == "41" + "hash"