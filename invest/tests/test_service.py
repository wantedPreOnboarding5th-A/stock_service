from django.test import TestCase
from exceptions import NotFoundError
from invest.models import Account, InvestInfo, Stock
from invest.service import InvestInfoManagementSerivice
from invest.tests.mock_repo import MockInvestInfoRepo, MockUserRepo, MockUserRepoHasNotFound
from user.models import User


class TestAllService(TestCase):

    # 없어도 무관, 참고용
    def set_up(self):
        # given
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

    def test_get_invest_info(self):
        # given
        expected_data = {
            "user_name": "UserName",
            "brokerage": "brokerage",
            "number": "1234123412",
            "account_name": "계좌명1",
            "all_assets": 10000,
        }
        #이하는 참고용
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
        # when
        response = InvestInfoManagementSerivice(
            invest_info_repo=MockInvestInfoRepo, user_repo=MockUserRepo
        )
        # then
        self.assertEqual(response, expected_data)

    def test_get_invest_info_user_not_found(self):
        #given
        expected_data = NotFoundError
        #when
        response = InvestInfoManagementSerivice(
            invest_info_repo=MockInvestInfoRepo, user_repo=MockUserRepoHasNotFound
        )
        #then
        self.assertEqual(response, expected_data)

    def test_get_invest_detail(self):
        expected_data = {  # 수정필요
            "user_name": "UserName",
            "brokerage": "brokerage",
            "number": "1234123412",
            "account_name": "계좌명1",
            "all_assets": 10000,
        }
        response = 
        self.assertEqual(response, expected_data)
        pass
