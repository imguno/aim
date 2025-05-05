from rest_framework import serializers
from .models import MemberTransaction

class TransactionRequestSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    description = serializers.CharField(required=False, allow_blank=True, max_length=255)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("[AIM]금액은 0보다 커야 합니다.")
        return value

        
class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberTransaction
        fields = [
            'tx_type',
            'amount',
            'description',
            'created_at'
        ]