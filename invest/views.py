from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from .service import StockService

stock_service = StockService()


@api_view(["GET"])
@parser_classes([JSONParser])
def get_list(request):
    user_id = request.user
    return JsonResponse(stock_service.get_stock_held_list())
