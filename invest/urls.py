from django.urls import path

from invest.views import get_invest_detail, get_invest_info


urlpatterns = [
    path("invest/details/<int:account_number>", get_invest_detail),
    path("invest/<int:account_number>", get_invest_info),
    path("stock/list", get_list),
]
