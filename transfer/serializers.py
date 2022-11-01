from rest_framework import serializers
from transfer.models import Transfer

class TransferSchema(serializers.Serializer):
    """
    phase1의 Transfer 요청에 필요한 파라미터 정의
    """
    user_name = serializers.CharField(max_length = 20)
    account_number = serializers.CharField(max_length = 13)
    transfer_amount = serializers.IntegerField()


class TransferSerializer(serializers.ModelSerializer):
    """
    phase1의 Transfer 객체 생성을 위한 파라미터 정의
    """
    class Meta:
        model = Transfer
        fields = "__all__" 


class TransferIDSchema(serializers.Serializer):
    """
    phase2의 pay 요청에 필요한 파라미터 정의
    """
    
    transfer_identifier = serializers.IntegerField()
    signature = serializers.CharField(max_length = 250)


class PayforTransSchema(serializers.Serializer):
    """
    hash화된 signature와 비교를 위한 파라미터 정의
    """
    
    account_number = serializers.CharField(max_length = 13)
    user = serializers.CharField(max_length = 20, source = "user.name")
    transfer_amount = serializers.IntegerField()