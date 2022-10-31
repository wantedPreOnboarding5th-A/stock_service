from typing import List

from .models import Stock
from .serializers import StockSerializer

from .utils.exceptions import NotFoundError


class StockRepo:
    def __init__(self) -> None:
        self.model = Stock
        self.serializer = StockSerializer

    def get_list_by_account_id(self, accout_id: List[int]) -> dict:
        try:
            for account in accout_id:
                created = self.serializer(
                    self.model.objects.prefetch_related("investinfo_set").filter(accout_id=account)
                ).data
        except self.model.DoesNotExist:
            raise NotFoundError
