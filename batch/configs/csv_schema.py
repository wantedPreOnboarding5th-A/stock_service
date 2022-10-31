from pydantic import BaseModel
from pydantic import BaseModel, ValidationError, validator


class CustomBaseModel(BaseModel):
    @classmethod
    def get_fields_name_list(cls) -> list[str]:
        return list(cls.__fields__.keys())


def _check_str_max_length(input_str: str, max_length: int):
    return len(input_str) <= max_length


def _str_max_length_validator(v, max_legnth: int):
    if _check_str_max_length(v, max_legnth):
        return v.title()
    else:
        raise ValidationError("str max length limited")


def _str_must_be_given_digit_validator(v, digit_cnt: int, exception_value: str = None):
    if (len(v) == digit_cnt) or (exception_value != None and exception_value == v):
        return v.title()
    else:
        raise ValidationError(f"str must be {digit_cnt} digit")


class AccountBasicInfoSchema(CustomBaseModel):
    account_number: str
    investment_principal: str

    @validator("account_number")
    def account_number_must_be_13_digit(cls, v):
        return _str_must_be_given_digit_validator(v, 13)


class AccountAssetInfoSchema(CustomBaseModel):
    user_name: str
    brokerage: str
    number: str
    account_name: str
    isin_number: str
    current_price: str
    amount: str


class AssetGroupIngoSchema(CustomBaseModel):
    name: str
    isin_number: str
    group: str

    @validator("name")
    def name_str_max_length_validator(cls, v):
        return _str_max_length_validator(v, 20)

    @validator("group")
    def group_str_max_length_validator(cls, v):
        return _str_max_length_validator(v, 20)

    @validator("isin_number")
    def isin_number_must_be_12_digit(
        cls,
        v,
    ):
        return _str_must_be_given_digit_validator(v, 12, exception_value="CASH")
