from email.policy import default
from django.db import models
from stock_service.models import BaseModel
from user.models import User as CustomUser


class Stock(BaseModel):
    name = models.CharField(max_length=20, null=False)  # 종목명
    isin_number = models.CharField(max_length=12, null=False)  # ISIN
    group = models.CharField(max_length=20, null=False)  # 자산그룹

    class Meta:
        db_table = "stock"
        abstract = False
        managed = True


class Account(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        db_column="user_id",
    )
    brokerage = models.CharField(max_length=20, null=False)  # 증권사
    number = models.CharField(max_length=13, null=False, unique=True)  # 계좌번호
    name = models.CharField(max_length=20, null=False)  # 계좌명
    investment_principal = models.IntegerField(null=False, default=0)  # 투자원금

    class Meta:
        db_table = "account"
        abstract = False
        managed = True


class InvestInfo(BaseModel):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        db_column="stock_id",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        db_column="account_id",
    )
    amount = models.IntegerField(null=False)  # 보유 수량
    current_price = models.IntegerField(null=False)  # 현재가
    account_isin_number = models.CharField(
        max_length=26, null=False, unique=True, default=""
    )  # "{account_number}_{isin_number}" 값 저장

    class Meta:
        db_table = "invest_info"
        abstract = False
        managed = True
