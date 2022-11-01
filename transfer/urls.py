from django.urls import path
from transfer.controller  import TransferAPI, PayAPI

urlpatterns = [
    path("transfer/", TransferAPI.as_view()),
    path("pay/", PayAPI.as_view())
]