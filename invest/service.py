from invest.repository import AbstractInvestInfoRepo
from invest.serializers import InvestInfoDetailResSchema, InvestInfoResSchema


from user.repository import AbstractUserRepo


class InvestInfoManagementSerivice:
    def __init__(
        self, invest_info_repo: AbstractInvestInfoRepo, user_repo: AbstractUserRepo
    ) -> None:
        self.invest_info_repo = invest_info_repo
        self.user_repo = user_repo

    #Question 왜 생성자를 놔두고 이쪽에있는 self 를 인자로 받으려고 하는걸까?
    
    def get_invest_info(self, account_number: str) -> dict:
        
        #point
        invest_info_list = self.invest_info_repo.find_by_account_number(self,
            account_number=account_number
        )
        user_info = self.user_repo.get_by_account_number(self,account_number=account_number)

        # filter, .select_related, 자동 캐싱된다.
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

        # filter, .select_related, 자동 캐싱된다.
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

        data = {
            "user_name": user_name,
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
