
from rest_framework import status
from django.test import TestCase
from invest.models import Account, InvestInfo, Stock
from user.models import User
from provider.auth_provider import AuthProvider

class StockAPITest(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(
            name="김가나",
            email="test1@test.com",
            password="test",
        )
        self.accunt1 = Account.objects.create(
            user=self.user1,
            number=1111111111111,
            brokerage="테스트증권1",
            name="테스트계좌1",
            investment_principal=10000,
        )
        self.accunt2 = (
            Account.objects.create(
                user=self.user1,
                number=1111111111111,
                brokerage="테스트증권2",
                name="테스트계좌2",
                investment_principal=10000,
            ),
        )
        self.stock1 = Stock.objects.create(
            name="코스피 50",
            isin_number="KR7360750004",
            group="국내",
        )
        InvestInfo.objects.create(
            stock=self.stock1,
            accout=self.accunt1,
            amount=100,
            current_price=200000,
            account_isin_number="KR7360750004",
        )

    def tearDown(self) -> None:
        User.objects.all().delete()
        Account.objects.all().delete()
        Stock.objects.all().delete()
        InvestInfo.objects.all().delete()

    def test_get_list_stock_held_complete(self):
        self.auth_provider = AuthProvider()
        self.access_token = self.auth_provider.create_token(user_id=self.user1.id)
        headers = {"HTTP_AUTHORIZATION": self.access_token["access"]}
        response = self.client.get("/user/stock/", **headers)

        self.assertEqual(
            response,
            {
                "name": "코스피 50",
                "group": "국내",
                "evaluation_amount": 20000000,
                "isin_number": "KR7360750004",
            },
        )