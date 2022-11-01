from typing import Union
from pydantic import BaseModel
from pydantic import BaseModel, ValidationError


def _validate_is_numeric_str(data: str):

    if isinstance(data, int) or data.isnumeric():
        return True
    else:
        raise ValidationError("Not a Number string")


def _validate_account_number(account_number: Union[int, str]):
    _validate_is_numeric_str(account_number)  # raise error if not valid
    str_number = str(account_number)
    if len(str_number) >= 12 and len(str_number) <= 13:
        return str_number
    else:
        raise ValidationError("account number must be 12 or 13 digit number")


class NameFiled(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_name

    @classmethod
    def validate_name(cls, name: str) -> str:
        if len(name) <= 20:
            return name
        else:
            raise ValidationError("name maximum length is 20")


class AccountNumber(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_acccount_number

    @classmethod
    def validate_acccount_number(cls, acccount_number: str) -> str:
        return _validate_account_number(acccount_number)  # 올바르지 않은 경우 raise error


class ISIN(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_isin_number

    @classmethod
    def validate_isin_number(cls, isin_number: str) -> str:
        if len(isin_number) == 12 or isin_number == "CASH":
            return isin_number
        else:
            raise ValidationError("Invalid ISIN")


class PositiveInt(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_positive_int

    @classmethod
    def validate_positive_int(cls, number: Union[str, int]) -> str:
        _validate_is_numeric_str(number)  # raise error if not valid
        int_number = int(number)

        if int_number >= 0:
            return int_number
        else:
            raise ValidationError("Number must be bigger than or same 0")


class CustomBaseModel(BaseModel):
    @classmethod
    def get_fields_name_list(cls) -> list[str]:
        return list(cls.__fields__.keys())


class AccountBasicInfoSchema(CustomBaseModel):
    account_number: AccountNumber
    investment_principal: PositiveInt


class AccountAssetInfoSchema(CustomBaseModel):
    user_name: NameFiled
    brokerage: NameFiled
    number: AccountNumber
    account_name: NameFiled
    isin_number: ISIN
    current_price: PositiveInt
    amount: PositiveInt


class AssetGroupInfoSchema(CustomBaseModel):
    name: NameFiled
    isin_number: ISIN
    group: str
