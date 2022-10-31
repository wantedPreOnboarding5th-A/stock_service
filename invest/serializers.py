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


class InvestAccountStockListSerializer(serializers.ListSerializer):
    """Join 전용 Serializer"""

    stocks = StockSerializer(many=True, read_only=True)
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = InvestInfo
        fields = ["stocks", "accounts", "current_price", "amount"]


class InvestInfoResSchema(serializers.Serializer):
    """투자정보 조회 서비스 응답 필드"""

    account_name = serializers.CharField()
    brokerage = serializers.CharField()
    number = serializers.CharField()
    user_name = serializers.CharField()
    all_assets = serializers.IntegerField()


class InvestInfoDetailResSchema(serializers.Serializer):
    """투자정보 상세 조회 서비스 응답 필드"""

    account_name = serializers.CharField()
    brokerage = serializers.CharField()
    number = serializers.CharField()
    user_name = serializers.CharField()
    all_assets = serializers.IntegerField()
    investment_principal = serializers.IntegerField()
    total_profit = serializers.IntegerField()
    profit_percentage = serializers.IntegerField()


class InvestInfoDetailResSchema:
    """투자 상세정보 조회 서비스 응답 필드"""
