from rest_framework import status
from django.test import TestCase
from invest.models import Account, InvestInfo, Stock
from user.models import User
from provider.auth_provider import AuthProvider


class GetAllInfomationTest(TestCase):
    """Test module for GET API"""

    def setUp(self) -> None:
        a = self.user = User.objects.create(
            name="UserName",
            email="example@email.com",
            password="88a0fec0ab09d7109929828a6e3f96d4947cf7cd82ea3dfd359043de9b2485e4",
        )
        b = self.stock = Stock.objects.create(name="StockName", group="Group", isin_number=1)
        c = self.account = Account.objects.create(
            user_id=1,
            brokerage="brokerage",
            number="1234123412",
            name="계좌명1",
            investment_principal=200000,
        )
        d = self.invest_info = InvestInfo.objects.create(
            stock_id=1, account_id=1, amount=5, current_price="2000"
        )
        e = 1

    def test_get_invest_info(self):
        e = 1
        # User.objects.create(User=self.user, name="Potato")
        # Stock.objects.create(Stock=self.stock, name="StockName")
        # Account.objects.create(Account=self.account, name="account")
        # InvestInfo.objects.create(InvestInfo=self.invest_info, name="account")
        e = e
        expected_data = {
            "user_name": "UserName",
            "brokerage": "brokerage",
            "number": "1234123412",
            "account_name": "계좌명1",
            "all_assets": 10000,
        }
        # get API response
        response = self.client.get(
            "get_invest_info", kwargs={"account_number": 1234123412}, foramt="json"
        )
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_get_invest_detail(self):
    #     expected_data = {
    #         "user_name": "UserName",
    #         "brokerage": "brokerage",
    #         "number": "1234123412",
    #         "account_name": "계좌명1",
    #         "all_assets": 10000,
    #     }
    #     # get API response
    #     response = self.client.get(
    #         reverse("get_invest_detail", kwargs={"account_number": 1234123412}, format="json")
    #     )
    #     self.assertEqual(response.data, expected_data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


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
