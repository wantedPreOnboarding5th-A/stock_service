from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from invest.repository import InvestInfoRepo

from invest.service import InvestInfoManagementSerivice
from user.repository import UserRepo

# Create your views here.
invest_management_service = InvestInfoManagementSerivice(
    invest_info_repo=InvestInfoRepo, user_repo=UserRepo
)


@api_view(["GET"])
@parser_classes([JSONParser])
def get_invest_info(request, account_number: str):
    return JsonResponse(invest_management_service.get_invest_info(account_number=account_number))


@api_view(["GET"])
@parser_classes([JSONParser])
def get_invest_detail(request, account_number: str):
    return JsonResponse(invest_management_service.get_invest_detail(account_number=account_number))
