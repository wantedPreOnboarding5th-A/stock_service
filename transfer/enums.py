from stock_service.enums import BaseEnum


class TransferStatus(BaseEnum):
    CREATED = "C"  # 생성되었으나, 사용자의 요청이 오지 않은 상태
    SCCUESS = "S"  # 인증이 완료되어, 입금이 완료된 상태
    FAILED = "F"  # 인증이 실패하여, 입금이 취소된 상태
