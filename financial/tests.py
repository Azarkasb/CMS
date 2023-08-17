from django.test import TestCase
from financial.models import Transaction, Wallet


class TestFinancial(TestCase):
    def setUp(self):
        self.client.post(
            "/register/",
            data={"username": "user", "password": "pass"},
            format="json",
        )

    def login_header(self):
        login_response = self.client.post(
            "/api-token-auth/",
            data={"username": "user", "password": "pass"},
            format="json",
        )

        token = login_response.data.get("token")
        return {"HTTP_AUTHORIZATION": f"Token {token}"}

    def test_create_transaction(self):
        auth_headers = self.login_header()
        response = self.client.post(
            "/financial/transactions/",
            data={"amount": 10000, "type": "I"},
            format="json",
            **auth_headers
        )

        self.assertEqual(response.status_code, 201)

    def test_retrieve_transaction(self):

        auth_headers = self.login_header()
        response = self.client.get(
            "/financial/transactions/",
            **auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_generate_report(self):
        auth_headers = self.login_header()
        response = self.client.post(
            "/financial/report/",
            **auth_headers
        )
        self.assertEqual(response.status_code, 200)



