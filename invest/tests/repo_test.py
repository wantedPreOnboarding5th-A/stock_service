from django.conf import settings
import pytest
from invest.models import Account, InvestInfo, Stock
from invest.repository import AccountRepo, InvestInfoRepo, StockRepo
from user.models import User
from user.repository import UserRepo

# Create your tests here.
invest_info_repo = InvestInfoRepo()
account_repo = AccountRepo()
stock_repo = StockRepo()
user_repo = UserRepo()

@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES
    
@pytest.fixture(scope="session")
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


valid_data_stock = {"name": "미국S&P500", "isin_number": "KR7360750004", "group": "미국 주식"}
