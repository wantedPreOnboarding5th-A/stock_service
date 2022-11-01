from django.urls import path

from .views import get_list

urlpatterns = [
    path("user/stock", get_list),
]
