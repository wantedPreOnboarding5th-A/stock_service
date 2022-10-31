from django.db import models
from stock_service.models import BaseModel
from user.models import User as CustomUser
from invest.models import Account


class Transfer(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        db_column="account_id",
    )
    account_number = models.CharField(
        max_length=13, null=False
    )  # 계좌번호, 조회 성능 향상을 위해 역정규화
    status = models.CharField(
        max_length=1, null=False, default="C"
    )  # 상태값, enum으로 선언하여 관리
    transfer_amount = models.IntegerField(null=False, default=0)  # 송금 금액

    class Meta:
        db_table = "transfer"
        abstract = False
        managed = True
