from invest.repository import AbstractInvestInfoRepo
from exceptions import NotFoundError
from user.repository import AbstractUserRepo

""" In DB condition

    user = {
            "name": "UserName",
            "email": "example@email.com",
            "password": "88a0fec0ab09d7109929828a6e3f96d4947cf7cd82ea3dfd359043de9b2485e4",
        }
    stocks = [{"name": "StockName", "group": "Group", "isin_number": 1},"stocks": {"name": "CASH", "group": "Group", "isin_number": 1}]
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
# Mock Object
class MockUserRepo(AbstractUserRepo):
    def get_by_account_number(account_number: str) -> dict:
        res = {
            "id":1,
            "name": "UserName",
            "email": "example@email.com",
            "password": "88a0fec0ab09d7109929828a6e3f96d4947cf7cd82ea3dfd359043de9b2485e4",
        }
        return res


class MockUserRepoHasNotFound(AbstractUserRepo):
    def get_by_account_number(account_number: str) -> dict:
        res = NotFoundError
        return res


# Mock Object
class MockInvestInfoRepo(AbstractInvestInfoRepo):
    def find_by_account_number(account_number: str) -> dict:
        res = [
            {
                "stocks": {"name": "StockName", "group": "Group", "isin_number": 1},
                "account": {
                    "user_id": 1,
                    "brokerage": "brokerage",
                    "number": "1234123412",
                    "name": "계좌명1",
                    "investment_principal": 200000,
                },
                "amount": 5,
                "current_price": 2000,
            },
            {
                "stocks": {"name": "CASH", "group": "Group", "isin_number": 1},
                "account": {
                    "user_id": 1,
                    "brokerage": "brokerage",
                    "number": "1234123412",
                    "name": "계좌명1",
                    "investment_principal": 200000,
                },
                "amount": 1,
                "current_price": 10000,
            }
        ]
        return res
