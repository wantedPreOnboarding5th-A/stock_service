from django.http import JsonResponse
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from transfer.serializers import TransferSchema, TransferIDSchema
from transfer.service import TransferService, PayService
from decorators.execption_handler import execption_hanlder
from decorators.auth_handler import must_be_user
from transfer.exceptions import DoesNotSameName

transfer_service = TransferService()
pay_service = PayService()

class TransferAPI(APIView):
    def post(self, request):
        return transfer(request)


@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def transfer(request):
    """
    "account_number"    : "123123",
    "user_name"         : "아이작",
    "transfer_amount"   : 1000
    """
    
    params = request.data
    params = TransferSchema(data=params)
    params.is_valid(raise_exception=True)
    
    if request.user["name"] != params.data["user_name"]:
        raise DoesNotSameName()

    create_transfer = transfer_service.create(**params.data)
    return JsonResponse({"transfer_identifier": create_transfer["id"]}, status=status.HTTP_201_CREATED)

  
class PayAPI(APIView):
    def post(self, request):
        return pay(request)


@execption_hanlder()
@must_be_user()
@parser_classes([JSONParser])
def pay(request):
    """
    "123123아이작1000" 을 sha512 hash 한 값
    
    "signature"             :"82b64b05dfe897e1c2bce88a62467c084d79365af1"
    "transfer_identifier"   : 111
    """
    
    params = request.data
    params = TransferIDSchema(data=params)
    params.is_valid(raise_exception=True)
    transfer_pay = pay_service.create(**params.data)    
    return JsonResponse({"status": transfer_pay},status=status.HTTP_201_CREATED)