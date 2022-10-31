from django.db import models
from stock_service.models import BaseModel


class User(BaseModel):
    name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = "user"
