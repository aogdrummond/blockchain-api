import os
import json
import random
from dotenv import load_dotenv
from requests import post, get

load_dotenv()
SERVER_URL = os.environ.get("SERVER_URL")

class TestApiIntegration():
     
    def test_hello_world(self):
        response = get(SERVER_URL)
        assert response.status_code == 200
        assert response.text == "Hello, World!"

    def test_generate_address(self):
        data = {"crypto_currency": "BTC"}
        response = post(SERVER_URL+"/api/generate", json=data)
        assert response.status_code == 201
        address_data = json.loads(response.text)
        assert "address" in address_data

    def test_generate_address_missing_parameter(self):
        data = {}  # Missing "crypto_currency" parameter
        response = post(SERVER_URL+"/api/generate", json=data)
        assert response.status_code == 400
        error_data = json.loads(response.text)
        assert "error" in error_data

    def test_list_addresses(self):
        response = get(SERVER_URL+"/api/list")
        assert response.status_code == 200
        addresses_data = json.loads(response.text)
        assert "addresses" in addresses_data

    def test_retrieve_address(self):
        address_id = "10"
        response = get(SERVER_URL+f"/api/addresses/{address_id}")
        assert response.status_code == 200
        address_data = json.loads(response.text)
        assert "address" in address_data

    def test_retrieve_address_not_found(self):
        address_id = random.getrandbits(32)
        response = get(SERVER_URL+f"/api/addresses/{address_id}")
        assert response.status_code == 404
        error_data = json.loads(response.text)
        assert "error" in error_data
