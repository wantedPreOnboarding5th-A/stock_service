from invest.serializers import InvestInfoDetailResSchema, InvestInfoResSchema
from invest.repository import  InvestInfoRepo, AbstractInvestInfoRepo
from user.repository import AbstractUserRepo
from .models import Account


class StockService:
    def __init__(self) -> None:
        self.repository = InvestInfoRepo()

    def get_stock_held_list(self, user_id: int) -> dict:
        account_ids = Account.objects.filter(user_id=user_id)
        params = []

        for account_id in account_ids:
            params.append(account_id.id)

        repos = self.repository.get_list_by_account_id(account_id=params)

        res = [
            {
                "name": repo["stock"]["name"],
                "group": repo["stock"]["group"],
                "evaluation_amount": repo["amount"] * repo["current_price"],
                "isin_number": repo["stock"]["isin_number"],
            }
            for repo in repos
        ]

        return res


class InvestInfoManagementSerivice:
    def __init__(
        self, invest_info_repo: AbstractInvestInfoRepo, user_repo: AbstractUserRepo
    ) -> None:
        self.invest_info_repo = invest_info_repo
        self.user_repo = user_repo

    def get_invest_info(self, account_number: str) -> dict:

        invest_info_list = self.invest_info_repo.find_by_account_number(
            account_number=account_number
        )
        user_info = self.user_repo.get_by_account_number(account_number=account_number)

        all_assets = 0
        for i in invest_info_list:
            all_assets = all_assets + i["amount"] * i["current_price"]
        account_name = invest_info_list[0]["account"]["name"]
        brokerage = invest_info_list[0]["account"]["brokerage"]
        account_number = invest_info_list[0]["account"]["number"]
        user_name = user_info["name"]

        data = {
            "user_name": user_name,
            "brokerage": brokerage,
            "number": account_number,
            "account_name": account_name,
            "all_assets": all_assets,
        }

        res = InvestInfoResSchema(data=data)
        res.is_valid(raise_exception=True)

        return res.data

    def get_invest_detail(self, account_number: str) -> dict:

        invest_info_list = self.invest_info_repo.find_by_account_number(
            account_number=account_number
        )
        user_info = self.user_repo.get_by_account_number(account_number=account_number)

        all_assets = 0
        for i in invest_info_list:
            all_assets = all_assets + i["amount"] * i["current_price"]

        user_name = user_info["name"]
        account_name = invest_info_list[0]["account"]["name"]
        brokerage = invest_info_list[0]["account"]["brokerage"]
        account_number = invest_info_list[0]["account"]["number"]
        investment_principal = invest_info_list[0]["account"]["investment_principal"]
        total_profit = all_assets - investment_principal
        profit_percentage = (total_profit / investment_principal) * 100

        # 유저쪽 이름 가져오기 #TODO 하드코딩 되어있음
        user_name = "str"

        data = {
            "account_name": account_name,
            "brokerage": brokerage,
            "number": account_number,
            "all_assets": all_assets,
            "investment_principal": investment_principal,
            "total_profit": total_profit,
            "profit_percentage": profit_percentage,
        }
        
        res = InvestInfoDetailResSchema()

        return data