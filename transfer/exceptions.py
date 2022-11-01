from rest_framework import status
from exceptions import CustomBaseExecption


class DoesNotSameAccountNumber(CustomBaseExecption):
    def __init__(self):
        self.msg = "The account Number does not same"
        self.status = status.HTTP_400_BAD_REQUEST


class NegativeAmountError(CustomBaseExecption):
    def __init__(self):
        self.msg = "The amount can not be Negative Number"
        self.status = status.HTTP_400_BAD_REQUEST


class AlreadyPayedError(CustomBaseExecption):
    def __init__(self):
        self.msg = "This Transfer is already Paied"
        self.status = status.HTTP_400_BAD_REQUEST
