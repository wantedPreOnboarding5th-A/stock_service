from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema

from .service import StockService
from provider.auth_provider import AuthProvider

stock_service = StockService()
auth_provider = AuthProvider()


@api_view(["GET"])
@parser_classes([JSONParser])
@swagger_auto_schema(
    responses={
        "name": "name",
        "group": "group",
        "evaluation_amount": "evaluation_amount",
        "isin_number": "isin_number",
    },
)
def get_list(request):
    auth_token = request.META.get("HTTP_AUTHORIZATION", None)
    decoded = auth_provider._decode(token=auth_token)
    user_id = decoded["id"]
    return JsonResponse(stock_service.get_stock_held_list(user_id=user_id))
