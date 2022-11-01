from django.urls import path

from .views import get_list

urlpatterns = [
    path("stock/list", get_list),
]
