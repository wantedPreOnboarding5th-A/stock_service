from transfer.repository import TransferRepo, PayRepo
from transfer.models import Transfer
from transfer.serializers import PayforTransSchema
from transfer.enums import TransferStatus
from transfer.exceptions import NotFoundErrorTransfer


class TransferService:
    """
    phase1을 위한 서비스
    """
    
    def __init__(self) -> None:
        self.transfer_refo = TransferRepo()

    def create(self, user_name: str, account_number: str, transfer_amount: int) -> dict: 
        
        created_transfer = self.transfer_refo.create(
            user_name = user_name,
            account_number = account_number,
            transfer_amount = transfer_amount
        )
        return created_transfer


class PayService:
    """
    phase2을 위한 서비스
    """
    
    def __init__(self):
        self.pay_repo = PayRepo()


    def create(self, signature: str, transfer_identifier: int) -> bool:
        try:
            trans_obj = Transfer.objects.get(id = transfer_identifier)
            self.pay_repo.is_already_success(trans_obj)
            serializer = PayforTransSchema(instance=trans_obj)
            hashed = self.pay_repo.check_signatrue(signature, **serializer.data )
            
            if hashed: # True인 경우는 account의 investment_principal에 플러스            
                trans_obj.account.investment_principal += trans_obj.transfer_amount
                trans_obj.account.save()
                trans_obj.status = TransferStatus.SCCUESS.value
                trans_obj.save()
                return True
            else: # False인 경우는 Transfer객체의 상태를 Fail로 처리
                trans_obj.status = TransferStatus.FAILED.value
                trans_obj.save()
                return False  
        
        except Transfer.DoesNotExist:
            raise NotFoundErrorTransfer()