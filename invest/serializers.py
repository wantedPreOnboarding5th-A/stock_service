from rest_framework import serializers

from .models import Stock, InvestInfo, Account


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"


class InvestInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestInfo
        fields = "__all__"


class InvestAccountStockListSerializer(serializers.ModelSerializer):
    """조인 전용 Serializer"""

    stocks = StockSerializer(many=True, read_only=True)
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = InvestInfo
        fields = ["stocks", "accounts", "current_price", "amount"]
