from django.conf import settings
import pytest
from invest.models import Account, InvestInfo, Stock
from invest.repository import AccountRepo, InvestInfoRepo, StockRepo
from invest.tests.fake_repo import MockAccountRepo, MockInvestInfoRepo, MockStockRepo, MockUserRepo
from user.models import User
from user.repository import UserRepo

# Create your tests here.
mock_invest_info_repo = MockInvestInfoRepo()
mock_account_repo = MockAccountRepo()
mock_stock_repo = MockStockRepo()
mock_user_repo = MockUserRepo()

board_service = BoardService(repo=fake_post_repo)


@pytest.fixture(scope="session")
def set_up_fake_db():
        mock_invest_info_repo.in_memory_db = dict()
        mock_account_repo.in_memory_db = dict()
        mock_stock_repo.in_memory_db = dict()
        mock_user_repo.in_memory_db = dict()
    fake_users = [
        {
            "id": 1,
            "name": "user1",
            "email": "test@test.com",
            "created_at": "2022-09-13 13:12:00",
            "updated_at": "2022-09-13 13:12:00",
        },
        {
            "id": 2,
            "name": "user2",
            "email": "test2@test.com",
            "created_at": "2022-09-13 13:12:00",
            "updated_at": "2022-09-13 13:12:00",
        },
    ]
    for user in fake_users:
        fake_user_repo.create(user)

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


valid_data_stock = {"name": "미국S&P500", "isin_number": "KR7360750004", "group": "미국 주식"}
