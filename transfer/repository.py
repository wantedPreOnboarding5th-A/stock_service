import bcrypt
from transfer.models import Transfer
from transfer.serializers import TransferSerializer
from invest.models import Account
from transfer.enums import TransferStatus
from exceptions import NotFoundError
from .exceptions import NegativeAmountError, AlreadyPayedError


class TransferRepo:
    """
    Trans처리를 위한 Repo
    """
    
    def __init__(self)-> None:
        self.model = Transfer
        self.serializer = TransferSerializer

    def create(self, user_name: str, account_number: str, transfer_amount: int) -> dict:
        try:
            account_obj = Account.objects.get(number = account_number)
            
            if not self.is_postive_amount(transfer_amount):
                raise NegativeAmountError()

            serialize = self.serializer(
                data={
                    "user": account_obj.user.id, 
                    "account": account_obj.id,
                    "account_number" : account_number,
                    "status": TransferStatus.CREATED.value,
                    "transfer_amount": transfer_amount
                }
            )
            serialize.is_valid(raise_exception=True)
            serialize.save()

            return serialize.data
        
        except Account.DoesNotExist:
            raise NotFoundError()
            

    def is_postive_amount(self, transfer_amount: int)-> bool:
        """
        음수로 들어온 수에 대한 확인 메서드
        """
        return True if transfer_amount > 0 else False        


class PayRepo:
    """
    Pay처리를 위한 Repo
    """
    
    def __init__(self)-> None:
        self.model = Transfer
    

    def check_signatrue(self, signature: str, user: str,  account_number: str, transfer_amount: int) -> bool:
        """
        signatrue와 transfer 객체 저장된 정보 일치 확인 메서드
        """
        
        hash = user+account_number+str(transfer_amount)
    
        test = bcrypt.hashpw(hash.encode("utf8"), bcrypt.gensalt()).decode("utf8") 
        print(test)
        
        hashed = self.check_hash(hash, signature)
        return hashed 
    

    def check_hash(self, hash: str, signature: str) -> bool:
        return bcrypt.checkpw(hash.encode('utf-8'), signature.encode('utf-8'))

    
    def is_already_success(self, trans_obj: object) -> bool:
        """
        이미 처리된 Trans객체에 대한 확인 메서드
        """
        if trans_obj.status != TransferStatus.SCCUESS.value:
            return True 
        else: 
            raise AlreadyPayedError()