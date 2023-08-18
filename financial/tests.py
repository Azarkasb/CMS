from django.test import TestCase
from django.contrib.auth import get_user_model
from financial.models import Transaction, Wallet
from datetime import date, timedelta
import json

User = get_user_model()


class TestFinancial(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_pass'
        )
        self.wallet = Wallet.objects.get(user=self.user)

        # Create Some Transactions
        Transaction.objects.create(
            wallet=self.wallet,
            amount=10000,
            type="I"
        )

        Transaction.objects.create(
            wallet=self.wallet,
            amount=500,
            type="E"
        )

        Transaction.objects.create(
            wallet=self.wallet,
            amount=200,
            type="E",
            date=date.today() - timedelta(weeks=2),
            category="G",
        )

        Transaction.objects.create(
            wallet=self.wallet,
            amount=200,
            type="E",
            date=date.today() - timedelta(weeks=5),
            category="U",
        )

    def login_header(self):
        login_response = self.client.post(
            "/api-token-auth/",
            data={"username": "test_user", "password": "test_pass"},
            content_type="application/json",
        )

        token = login_response.data.get("token")
        return {"HTTP_AUTHORIZATION": f"Token {token}"}

    def test_balance_calculation(self):
        self.assertEqual(self.wallet.balance, 9100)

        Transaction.objects.create(
            wallet=self.wallet,
            amount=900,
            type='I',
        )

        self.assertEqual(self.wallet.balance, 10000)

        t2 = Transaction.objects.create(
            wallet=self.wallet,
            amount=5000,
            type='E'
        )

        self.assertEqual(self.wallet.balance, 5000)

        t2.delete()

        self.assertEqual(self.wallet.balance, 10000)

    def test_create_transaction(self):
        auth_headers = self.login_header()
        response = self.client.post(
            "/financial/transactions/",
            data=json.dumps({"amount": 10000, "type": "I"}),
            content_type="application/json",
            **auth_headers
        )

        self.assertEqual(response.status_code, 201)
        transaction_id = response.data['id']
        self.assertTrue(Transaction.objects.filter(id=transaction_id).exists())

    def test_retrieve_transactions(self):

        auth_headers = self.login_header()
        response = self.client.get(
            "/financial/transactions/",
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.wallet.transaction_set.count())

    def test_retrieve_transactions_with_filter(self):

        auth_headers = self.login_header()
        response = self.client.get(
            "/financial/transactions/?type=I",
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), self.wallet.transaction_set.filter(type='I').count())

    def test_retrieve_transactions_with_order(self):

        auth_headers = self.login_header()
        response = self.client.get(
            "/financial/transactions/?ordering=-amount",
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['amount'], 10000)

    def test_retrieve_a_single_transaction(self):

        auth_headers = self.login_header()
        response = self.client.get(
            "/financial/transactions/1/",
            **auth_headers
        )
        self.assertEqual(response.status_code, 200)

    def test_update_transaction(self):
        auth_headers = self.login_header()
        response = self.client.put(
            "/financial/transactions/1/",
            data=json.dumps({"amount": 7, "type": "I"}),
            content_type="application/json",
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.get(id=1).amount, 7)

    def test_delete_transaction(self):
        auth_headers = self.login_header()
        response = self.client.delete(
            "/financial/transactions/1/",
            **auth_headers
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Transaction.objects.filter(id=1).exists())

    def test_generate_report(self):
        auth_headers = self.login_header()
        response = self.client.get(
            "/financial/report/?start_date=2000-08-10&end_date=2023-08-18",
            **auth_headers
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("current_balance"), 9100)
