from datetime import datetime
from pydantic import BaseModel, ValidationError, validator


def _check_str_max_length(input_str: str, max_length: int):
    return len(input_str) <= max_length


def _str_max_length_validator(cls, v, max_legnth: int):
    if _check_str_max_length(v, max_legnth):
        return v.title()
    else:
        raise ValidationError("str max length limited")


def _str_must_be_given_digit_validator(
    cls, v, digit_cnt: int, exception_value: str = None
):
    if (len(v) == digit_cnt) or (exception_value != None and exception_value == v):
        return v.title()
    else:
        raise ValidationError(f"str must be {digit_cnt} digit")


class CustomBaseModel(BaseModel):
    id: int
    created_at: datetime
    updated_at = datetime


class User(CustomBaseModel):
    name: str

    @validator("name")
    def name_str_max_length_validator(cls, v):
        return _str_max_length_validator(cls, v, 20)


class Stock(CustomBaseModel):
    name: str
    isin_number: str
    group: str

    @validator("name")
    def name_str_max_length_validator(cls, v):
        return _str_max_length_validator(cls, v, 20)

    @validator("group")
    def group_str_max_length_validator(cls, v):
        return _str_max_length_validator(cls, v, 20)

    @validator("isin_number")
    def isin_number_must_be_12_digit(
        cls,
        v,
    ):
        return _str_must_be_given_digit_validator(cls, v, 12, exception_value="CASH")


class Account(CustomBaseModel):
    user: int
    name: str
    brokerage: str
    number: str
    investment_principal: int

    @validator("number")
    def account_number_must_be_13_digit(cls, v):
        return _str_must_be_given_digit_validator(cls, v, 13)

    @validator("name")
    def name_str_max_length_validator(cls, v):
        return _str_max_length_validator(cls, v, 20)

    @validator("brokerage")
    def brokerage_str_max_length_validator(cls, v):
        return _str_max_length_validator(cls, v, 20)


class InvestInfo(CustomBaseModel):
    stock: int
    account: int
    amount: int
    current_price: int
