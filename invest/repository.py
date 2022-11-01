<<<<<<< HEAD
from invest.exceptions import NotFoundError
from invest.models import Account, InvestInfo
from invest.serializers import (
    AccountSerializer,
    InvestAccountStockListSerializer,
    InvestInfoSerializer,
)

invest_acc_stock_serializer = InvestAccountStockListSerializer


class InvestInfoRepo:
    def __init__(self) -> None:
        self.serilaizer = InvestInfoSerializer
        self.model = InvestInfo

    def get_by_account_id(self, account_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(account_id=account_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def find_by_account_id(self, account_id: int) -> list:
        try:
            info_list = InvestInfo.objects.filter(account_id=account_id).order_by("-stock_id")
            return self.serilaizer(info_list)
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_stock_id(self, stock_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(stock_id=stock_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def find_by_stock_id(self, stock_id: int) -> list:
        try:
            info_list = InvestInfo.objects.filter(stock_id=stock_id).order_by("-stock_id")
            return self.serilaizer(info_list)
        except self.model.DoesNotExist:
            raise NotFoundError

        """
        계좌번호로 역참조 후 필터링해서 가져오는 메서드
        현금은 제외합니다.
        """

    def find_by_account_number(self, account_number: int) -> list:
        # 테이블 3개 조인
        try:
            invest_info_list = (
                InvestInfo.objects.prefetch_related("Account")
                .prefetch_related("Stock")
                .filter(account__number__exact=account_number)
                .exclude(stock__isin_number__exact="CASH")
            )

            # 비어있을시 오류 출력
            if not invest_info_list.values():
                raise NotFoundError

            return invest_acc_stock_serializer(invest_info_list).data
        except self.model.DoesNotExist:
            raise NotFoundError


class AccountRepo:
    def __init__(self) -> None:
        self.serilaizer = AccountSerializer
        self.model = Account

    def get(self, user_id: str) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(user_id=user_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

        """
        계좌 내에서 투자 원금이 아닌 현금만 찾아서 가져옵니다.
        """

    def find_by_account_cash(self, account_number: int) -> dict:
        try:
            cash_info = (
                self.model.objects.prefetch_related("Stock")
                .filter(number=account_number)
                .get(stock__isin_number__exact="CASH")
            )
            return invest_acc_stock_serializer(cash_info).data
        except self.model.DoesNotExist:
            raise NotFoundError
=======
from typing import List

from .models import Stock
from .serializers import StockSerializer

from .utils.exceptions import NotFoundError
>>>>>>> 2104b3c ([feat] 보유 종목 API 작성중)


class StockRepo:
    def __init__(self) -> None:
<<<<<<< HEAD
        self.serilaizer = AccountSerializer
        self.model = Account

    def get(self, stock_id: int) -> dict:
        try:
            return self.serilaizer(self.model.objects.get(id=stock_id))
=======
        self.model = Stock
        self.serializer = StockSerializer

    def get_list_by_account_id(self, accout_id: List[int]) -> dict:
        try:
            for account in accout_id:
                created = self.serializer(
                    self.model.objects.prefetch_related("investinfo_set").filter(accout_id=account)
                ).data
>>>>>>> 2104b3c ([feat] 보유 종목 API 작성중)
        except self.model.DoesNotExist:
            raise NotFoundError
