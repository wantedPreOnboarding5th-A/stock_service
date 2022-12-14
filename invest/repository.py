from invest.exceptions import NotFoundError
from typing import List


from .utils.exceptions import NotFoundError
from invest.models import InvestInfo
from invest.serializers import (
    InvestAccountStockListSerializer,
    InvestInfoSerializer,
)
from typing import List

from .utils.exceptions import NotFoundError


class AbstractInvestInfoRepo:
    def __init__(self) -> None:
        self.serializer = InvestInfoSerializer
        self.model = InvestInfo
        self.invest_acc_stock_serializer = InvestAccountStockListSerializer


class InvestInfoRepo(AbstractInvestInfoRepo):
    def __init__(self) -> None:
        super().__init__()

        """
        계좌번호로 참조 후 필터링해서 가져오는 메서드
        현금도 포함합니다.
        """

    def find_by_account_number(self, account_number: str) -> list:
        # 테이블 3개 조인
        try:

            invest_info_list = (
                InvestInfo.objects.select_related("account")
                .select_related("stock")
                .filter(account__number__exact=account_number)
            )
            # 비어있을시 오류 출력
            if not invest_info_list.values():
                raise NotFoundError
            return self.invest_acc_stock_serializer(invest_info_list, many=True).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_list_by_account_id(self, account_id: List[int]) -> dict:
        try:
            createds = self.model.objects.select_related("stock").filter(account_id__in=account_id)
            data = investinfo_stock_serializer(createds, many=True).data
            return data
        except self.model.DoesNotExist:
            raise NotFoundError


class AbstractAccountRepo:
    def __init__(self) -> None:
        self.serializer = AccountSerializer
        self.model = Account
        self.invest_acc_stock_serializer = InvestAccountStockListSerializer


class AccountRepo(AbstractAccountRepo):
    def __init__(self) -> None:
        super().__init__()

    # deprecated
    def get(self, user_id: str) -> dict:
        try:
            return self.serializer(self.model.objects.get(user_id=user_id)).data
        except self.model.DoesNotExist:
            raise NotFoundError

        """
        계좌 내에서 투자 원금이 아닌 현금만 찾아서 가져옵니다.
        """

    def get_by_account_cash(self, account_number: str) -> dict:
        try:
            cash_info = (
                self.model.objects.prefetch_related("Stock")
                .filter(number=account_number)
                .get(stock__isin_number__exact="CASH")
            )
            return self.invest_acc_stock_serializer(cash_info).data
        except self.model.DoesNotExist:
            raise NotFoundError


class AbstractStockRepo:
    def __init__(self) -> None:
        self.serializer = AccountSerializer
        self.model = Account


class StockRepo(AbstractStockRepo):
    def __init__(self) -> None:
        super().__init__()

    # deprecated
    def get(self, stock_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=stock_id))
            res = []
            for account in accout_id:
                created = self.serializer(
                    self.model.objects.prefetch_related("investinfo_set").filter(accout_id=account)
                ).data
                res.append(created)
            return res
        except self.model.DoesNotExist:
            raise NotFoundError
