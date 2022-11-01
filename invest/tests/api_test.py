from pyexpat import model
import pytest
from rest_framework import status
from django.test import TestCase
from invest.models import Account, InvestInfo, Stock
from invest.repository import AccountRepo, InvestInfoRepo, StockRepo
from invest.tests.fake_repo import fakeAccountRepo, fakeInvestInfoRepo, fakeStockRepo, fakeUserRepo
from user.models import User
from user.repository import UserRepo

fake_invest_info_repo = fakeInvestInfoRepo(model=InvestInfo)
fake_account_repo = fakeAccountRepo(model=Account)
fake_stock_repo = fakeStockRepo(model=Stock)
fake_user_repo = fakeUserRepo(model=User)


class GetAllInfomationTest(TestCase):
    """Test module for GET API"""
    @pytest.fixture(scope="session")
    def set_up_fake_db():
        fake_invest_info_repo.in_memory_db = dict()
        fake_account_repo.in_memory_db = dict()
        fake_stock_repo.in_memory_db = dict()
        fake_user_repo.in_memory_db = dict()
        test_users = [
             {"id": 1,
            "name": "user1",
            "email": "test@test.com",
            "created_at": "2022-09-13 13:12:00",
            "updated_at": "2022-09-13 13:12:00",}]
        fake_account_repo.create
        
        fake_post_repo.create(
        {
            "id": 1,
            "user": 1,
            "board": 1,
            "content": "created context",
            "created_at": "2022-09-13 13:12:00",
            "updated_at": "2022-09-13 13:12:00",
        }
    )


    def test_update_non_exist_post(set_up_fake_db):
        with pytest.raises(Post.DoesNotExist):
            sut = board_service.update_post(
                post_id=2, user_id=1, update_content="updated content"
        )
    


"""Repo 테스트"""


vaild_data_account = {
    "user_id": "1",
    "brokerage": "디셈버증권",
    "number": "5736692368320",
    "name": "계좌1",
    "investment_principal": 1911386,
}


@pytest.mark.django_db()
def test_get_account_repo():
    sut = account_repo.get(1)
    isinstance(sut, dict)


@pytest.mark.django_db()
def test_find_by_account_id():
    sut = invest_info_repo.get_by_account_id()
    isinstance(sut, list)


valid_data_invest_info = {
    "stock_id": "1",
    "account_id": "1",
    "amount": "21",
    "current_price": "8585",
}


@pytest.mark.django_db()
def test_find_invest_info_by_account_number():
    sut = invest_info_repo.find_by_account_number()
    isinstance(sut, list)
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
