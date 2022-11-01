from invest.repository import AccountRepo, InvestInfoRepo, StockRepo
from user.repository import UserRepo


invest_info_repo = InvestInfoRepo()
account_repo = AccountRepo()
stock_repo = StockRepo()
user_repo = UserRepo()


class InvestManagementSerivice:
    def get_invest_info(self, account_number: int) -> dict:
        invest_info_list = invest_info_repo.find_by_account_number(account_number=account_number)
        user_info = user_repo.get_by_account_number(account_number=account_number)
        # filter, .select_related, 자동 캐싱된다.
        all_assets = 0
        for i in invest_info_list:
            all_assets = all_assets + i["amount"] * i["current_price"]

        # 1인 1계좌, 계좌에서 이름 가져오기.
        account_name = invest_info_list[1]["name"]
        brokerage = invest_info_list[1]["brokerage"]
        account_number = invest_info_list[1]["number"]
        user_name = user_info["name"]

        data = {
            "user_name": user_name,
            "brokerage": brokerage,
            "number": account_number,
            "account_name": account_name,
            "all_assets": all_assets,
        }

        return data

    def get_invest_detail(self, account_number: str) -> dict:

        invest_info_list = invest_info_repo.find_by_account_number(account_number=account_number)
        # filter, .select_related, 자동 캐싱된다.
        all_assets = 0
        for i in invest_info_list:
            all_assets = all_assets + i["amount"] * i["current_price"]

        # 1인 1계좌, 계좌에서 이름 가져오기.
        account_name = invest_info_list[1]["name"]
        brokerage = invest_info_list[1]["brokerage"]
        account_number = invest_info_list[1]["Account"]["number"]
        investment_principal = [1]["Account"]["investment_principal"]
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

        return data
