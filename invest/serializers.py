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


class InvestInfoResSchema(serializers.Serializer):
    pass


class InvestAccountStockSerializer(serializers.ManyRelatedField):
    stocks = StockSerializer(many=True, read_only=True)
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ["isin_number"]
        model = Account
        fields = "__all__"
