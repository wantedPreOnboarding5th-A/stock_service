from django.test import TestCase
from exceptions import NotFoundError
from invest.service import InvestInfoManagementSerivice
from invest.mock_repo.mock_repo import MockInvestInfoRepo, MockUserRepo, MockUserRepoHasNotFound

""" In DB condition

    user = {
            "name": "UserName",
            "email": "example@email.com",
            "password": "88a0fec0ab09d7109929828a6e3f96d4947cf7cd82ea3dfd359043de9b2485e4",
        }
    stocks = {"name": "StockName", "group": "Group", "isin_number": 1}
    account = {
            "user_id": 1,
            "brokerage": "brokerage",
            "number": "1234123412",
            "name": "계좌명1",
            "investment_principal": 200000,
        }
    invest_info = {
            "account_id": 1,
            "stock_id": 1,
            "amount": 5,
            "current_price": 2000,
        }
"""


class TestAllService(TestCase):
    def set_up(self):
        pass

    def test_get_invest_info(self) -> dict:
        # given
        expected_data = {
            "user_name": "UserName",
            "brokerage": "brokerage",
            "number": "1234123412",
            "account_name": "계좌명1",
            "all_assets": 20000,
        }

        # when
        response = InvestInfoManagementSerivice(
            invest_info_repo=MockInvestInfoRepo, user_repo=MockUserRepo
        ).get_invest_info(account_number="1234123412")

        e = response
        # then
        self.assertEqual(response, expected_data)

    def test_get_invest_detail(self):
        # given
        expected_data = {
            "user_name": "UserName",
            "brokerage": "brokerage",
            "number": "1234123412",
            "account_name": "계좌명1",
            "all_assets": 20000,
            "investment_principal": 200000,
            "total_profit": -180000,
            "profit_percentage": -90,
        }

        # when
        response = InvestInfoManagementSerivice(
            invest_info_repo=MockInvestInfoRepo, user_repo=MockUserRepo
        ).get_invest_detail(account_number="1234123412")
        e = response

        # then
        self.assertEqual(response, expected_data)


from user.models import User
from invest.models import Account, InvestInfo, Stock
from invest.service import StockService


class StockRepoTest(TestCase):
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

    def test_get_stock_held_list_success(self):
        self.user_id = 1
        self.stock_service = StockService()
        response = self.stock_service.get_stock_held_list(user_id=self.user_id)

        self.assertEqual(
            response,
            {
                "name": "코스피 50",
                "group": "국내",
                "evaluation_amount": 20000000,
                "isin_number": "KR7360750004",
            },
        )
