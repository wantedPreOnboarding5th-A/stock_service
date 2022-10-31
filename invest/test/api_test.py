from django.test import Client, TestCase
from django.urls import reverse

from invest.models import Account, InvestInfo, Stock
from rest_framework import status


class GetAllInfomationTest(TestCase):
    """Test module for GET API"""

    def setUp(self):
        Stock.objects.create(name="StockName", group="Group", isin_number=1)
        Account.objects.create(
            user_id=1,
            brokerage="brokerage",
            number="1234123412",
            name="계좌명1",
            investment_principal=200000,
        )
        InvestInfo.objects.create(stock_id=1, account_id=1, amount=5, current_price="2000")
        
        # 유저명: "str" service쪽 하드코딩 해놓음
        # user.objects.create(
        #     name='Project 4', email='project4@project.com', score=4)

    def test_get_invest_info(self):
        expected_data = {
            "user_name": "str",
            "brokerage": "brokerage",
            "number": "1234123412",
            "account_name": "계좌명1",
            "all_assets": 10000,
        }
        # get API response
        response = Client.get(reverse("get_invest_info", kwargs={'account_number': self}))
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_invest_detail(self):
        expected_data = {
            "user_name": "str",
            "brokerage": "brokerage",
            "number": "1234123412",
            "account_name": "계좌명1",
            "all_assets": 10000,
        }
        # get API response
        response = Client.get(reverse("get_invest_info", kwargs={'account_number': self}))
        self.assertEqual(response.data, expected_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


