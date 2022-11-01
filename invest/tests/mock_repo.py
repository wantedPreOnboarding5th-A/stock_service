from invest.repository import AbstractInvestInfoRepo
from exceptions import NotFoundError

# Mock Object
class MockUserRepo(AbstractInvestInfoRepo):
    def get_by_account_number(account_number: str) -> dict:
        res = {
            "name": "UserName",
            "email": "example@email.com",
            "password": "88a0fec0ab09d7109929828a6e3f96d4947cf7cd82ea3dfd359043de9b2485e4",
        }
        return res


class MockUserRepoHasNotFound(AbstractInvestInfoRepo):
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
            }
        ]
        return res
