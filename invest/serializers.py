from rest_framework import serializers

from invest.models import Account, InvestInfo, Stock


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
