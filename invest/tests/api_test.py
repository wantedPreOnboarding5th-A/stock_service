from rest_framework import status
from django.test import TestCase
from invest.models import Account, InvestInfo, Stock
from user.models import User


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
