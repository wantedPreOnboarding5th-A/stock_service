from pydantic import BaseModel
from pydantic import BaseModel, ValidationError


def _validate_is_numeric_str(data: str):
    if data.isnumeric():
        return True
    else:
        raise ValidationError("Not a Number string")


def _str_must_be_given_digit_validator(v, digit_cnt: int, exception_value: str = None):
    if (len(v) == digit_cnt) or (exception_value != None and exception_value == v):
        return v.title()
    else:
        raise ValidationError(f"str must be {digit_cnt} digit")


def _validate_number_str(v, digit_cnt: int = None, exception_value: str = None):
    _validate_is_numeric_str(v)  # raise error if not valid
    number = int(v)
    if digit_cnt != None:
        return _str_must_be_given_digit_validator(v, digit_cnt, exception_value)
    else:
        if number >= 0:
            return v
        else:
            raise ValidationError("Number must be bigger than or same 0")


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
        if _validate_number_str(acccount_number, 13):  # 올바르지 않은 경우 raise error
            return acccount_number


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


class PositiveIntString(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_positive_int

    @classmethod
    def validate_positive_int(cls, number: str) -> str:
        _validate_is_numeric_str(number)  # raise error if not valid
        int_number = int(number)

        if int_number >= 0:
            return number
        else:
            raise ValidationError("Number must be bigger than or same 0")


class CustomBaseModel(BaseModel):
    @classmethod
    def get_fields_name_list(cls) -> list[str]:
        return list(cls.__fields__.keys())


class AccountBasicInfoSchema(CustomBaseModel):
    account_number: AccountNumber
    investment_principal: PositiveIntString


class AccountAssetInfoSchema(CustomBaseModel):
    user_name: NameFiled
    brokerage: NameFiled
    number: AccountNumber
    account_name: NameFiled
    isin_number: ISIN
    current_price: PositiveIntString
    amount: PositiveIntString


class AssetGroupInfoSchema(CustomBaseModel):
    name: NameFiled
    isin_number: ISIN
    group: str
