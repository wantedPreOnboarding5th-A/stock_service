from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from invest.service import InvestManagementSerivice, StockService

invest_management_service = InvestManagementSerivice()

stock_service = StockService()


@api_view(["GET"])
@parser_classes([JSONParser])
def get_invest_info(request, account_number: int):
    return JsonResponse(invest_management_service.get_invest_info(account_number=account_number))


@api_view(["GET"])
@parser_classes([JSONParser])
def get_invest_detail(request, account_number: int):
    return JsonResponse(invest_management_service.get_invest_detail(account_number=account_number))
