from django.conf import settings
import pytest
from invest.repository import AccountRepo, InvestInfoRepo, StockRepo

# Create your tests here.



invest_info_repo = InvestInfoRepo()
account_repo = AccountRepo()
stock_repo = StockRepo()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


"""Repo 테스트"""

vaild_data_account = {
    "user_id": "",
    "brokerage": "디셈버증권",
    "number": "5736692368320 ",
    "name": "계좌1",
    "investment_principal": "1911386",
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