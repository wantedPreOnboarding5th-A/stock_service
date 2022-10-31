from rest_framework import serializers

from .models import Stock, InvestInfo


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class InvestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestInfo
        fields = "__all__"
