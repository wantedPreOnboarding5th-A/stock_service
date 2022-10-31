from .repository import StockRepo
from .models import Account


class StockService:
    def __init__(self) -> None:
        self.stock_repo = StockRepo()

    def get_stock_held_list(self, user_id: int) -> dict:
        account_ids = Account.objects.filter(user_id=user_id)
        params = []

        for account_id in account_ids:
            params.append(account_id.id)

        return self.stock_repo.get_list_by_account_id(accout_id=account_id)
