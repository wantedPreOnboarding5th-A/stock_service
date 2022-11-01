"""
테스트를 위한 인 메모리 DB 리포지토리
"""

from typing import Union
from exceptions import NotFoundError
from invest.models import Account, InvestInfo
from invest.repository import AbstractAccountRepo, AbstractInvestInfoRepo, AbstractStockRepo
from user.models import User
from user.repository import AbstractUserRepo
from user.serializers import UserSerializer


class fakeUserRepo(AbstractUserRepo):
    def __init__(self, model: User) -> None:
        self.fakeAccountRepo = fakeAccountRepo(AbstractAccountRepo)
        self.in_memory_db = dict()
        self.model = model

    def create(self, data: dict) -> dict:
        self.in_memory_db[str(data["id"])] = data
        return data

    def get_by_id(self, id: int) -> Union[dict, None]:
        data_id_str = str(id)
        return self.in_memory_db.get(data_id_str, None)

    def get_by_account_number(self, account_number: int):
        """계좌번호로 유저 정보를 찾는 메서드 in fake Repo"""
        account = self.fakeAccountRepo.get_by_account_number(account_number=account_number)
        uid = account["user_id"]
        user = self.get_by_id(uid)
        return user

class fakeInvestInfoRepo(AbstractInvestInfoRepo):
    def __init__(self, model: User) -> None:
        self.fakeAccountRepo = fakeAccountRepo(AbstractAccountRepo)
        self.in_memory_db = dict()
        self.model = model

    def create(self, data: dict) -> dict:
        self.in_memory_db[str(data["id"])] = data
        return data

    def get_by_id(self, id: int) -> Union[dict, None]:
        data_id_str = str(id)
        return self.in_memory_db.get(data_id_str, None)
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

            return self.invest_acc_stock_serializer(invest_info_list).data
        except self.model.DoesNotExist:
            raise NotFoundError


class fakeAccountRepo(AbstractAccountRepo):
    def __init__(self, model: Account) -> None:
        self.in_memory_db = dict()
        self.model = model

    def create(self, data: dict) -> dict:
        self.in_memory_db[str(data["id"])] = data
        return data

    def get_by_id(self, id: int) -> Union[dict, None]:
        data_id_str = str(id)
        return self.in_memory_db.get(data_id_str, None)

    def get_by_account_number(self, account_number: int) -> dict:
        res = self.dict(filter("number" == str(account_number), self.in_memory_db))
        return res

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
            return self.invest_acc_stock_serializer(cash_info).data
        except self.model.DoesNotExist:
            raise NotFoundError

    # fake Repo 전용 메서드
    def create(self, data: dict) -> dict:
        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class fakeStockRepo(AbstractStockRepo):
    # deprecated
    def get(self, stock_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=stock_id))
        except self.model.DoesNotExist:
            raise NotFoundError

    # fake Repo 전용 메서드
    def create(self, data: dict) -> dict:
        serializer = self.serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
