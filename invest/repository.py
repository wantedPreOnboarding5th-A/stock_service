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
            res = []
            for account in account_id:
                createds = self.model.objects.select_related("stock").filter(account_id=account)
            for created in createds:
                data = self.serializer(created).data
                res.append(data)
            return res
        except self.model.DoesNotExist:
            raise NotFoundError
    
