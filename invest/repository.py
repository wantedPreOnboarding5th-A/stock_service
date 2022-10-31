from invest.models import Account, InvestInfo
from invest.serializers import AccountSerializer, InvestInfoSerializer


class InvestInfoRepo:
    def __init__(self) -> None:
        self.serilaizer = InvestInfoSerializer
        self.model = InvestInfo
        
    def get_by_account_id(self, account_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(account_id=account_id)).data
        except self.model.DoesNotExist:
            raise 
        
    def find_by_account_id(self, account_id:int) -> list:
        try:
            info_list = InvestInfo.objects.filter(account_id=account_id).order_by("-stock_id")
            return self.serilaizer(info_list)
        except self.model.DoesNotExist:
            raise 
    
    def get_by_stock_id(self, stock_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(stock_id=stock_id)).data
        except self.model.DoesNotExist:
            raise 
    
    def find_by_stock_id(self, stock_id: int) -> list:
        try:
            info_list = InvestInfo.objects.filter(stock_id=stock_id).order_by("-stock_id")
            return self.serilaizer(info_list)
        except self.model.DoesNotExist:
            raise 
            
        
class AccountRepo:
    def __init__(self) -> None:
        self.serilaizer = AccountSerializer
        self.model = Account
        
    def get(self, user_id: str) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(user_id = user_id)).data
        except self.model.DoesNotExist:
            raise
    
class StockRepo:
    def __init__(self) -> None:
        self.serilaizer = AccountSerializer
        self.model = Account
        
    def get(self, stock_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(id=stock_id))
        except self.model.DoesNotExist:
            raise