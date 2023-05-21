import os
import json
import random
from dotenv import load_dotenv
from requests import post, get

load_dotenv()
SERVER_URL = os.environ.get("SERVER_URL")


class TestApiIntegration:
    def test_hello_world(self) -> None:
        """
        Test the "Hello, World!" endpoint.

        Returns:
            None
        """
        response = get(SERVER_URL + "/api-blockchain/")
        assert response.status_code == 200
        assert json.loads(response.text) == "Hello, World!"

    def test_generate_address(self) -> None:
        """
        Test the generate address endpoint.

        Returns:
            None
        """
        data = {"crypto_currency": "BTC"}
        response = post(SERVER_URL + "/api-blockchain/generate", json=data)
        assert response.status_code == 201
        address_data = json.loads(response.text)
        assert "address" in address_data

    def test_generate_address_missing_parameter(self) -> None:
        """
        Test the generate address endpoint with a missing parameter.

        Returns:
            None
        """
        data = {}  # Missing "crypto_currency" parameter
        response = post(SERVER_URL + "/api-blockchain/generate", json=data)
        assert response.status_code == 400
        error_data = json.loads(response.text)
        assert "error" in error_data

    def test_list_addresses(self) -> None:
        """
        Test the list addresses endpoint.

        Returns:
            None
        """
        response = get(SERVER_URL + "/api-blockchain/list")
        assert response.status_code == 200
        addresses_data = json.loads(response.text)
        assert "addresses" in addresses_data

    def test_retrieve_address(self) -> None:
        """
        Test the retrieve address endpoint.

        Returns:
            None
        """
        address_id = "3"
        response = get(SERVER_URL + f"/api-blockchain/addresses/{address_id}")
        assert response.status_code == 200
        address_data = json.loads(response.text)
        assert "address" in address_data

    def test_retrieve_address_not_found(self) -> None:
        """
        Test the retrieve address endpoint with an invalid address ID.

        Returns:
            None
        """
        address_id = random.getrandbits(32)
        response = get(SERVER_URL + f"/api-blockchain/addresses/{address_id}")
        assert response.status_code == 404
        error_data = json.loads(response.text)
        assert "error" in error_data