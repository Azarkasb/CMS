from django.test import TestCase


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
