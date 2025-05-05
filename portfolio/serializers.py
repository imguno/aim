from rest_framework import serializers
from .models import PortfolioRequestPreset, PortfolioRequestStatus, PortfolioRequest, PortfolioResult, PortfolioResultItem, SecuritiesMarket
from decimal import Decimal
from rest_framework.validators import UniqueValidator

class PortfolioRequestSerializer(serializers.ModelSerializer):
    preset = serializers.ChoiceField(
        choices=PortfolioRequestPreset.choices,
        required=False,
        error_messages={
            'invalid_choice': "[AIM]허용된 투자 위험도가 아닙니다.",
        }
    )
    balance_ratio = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False
    )

    preset_label = serializers.SerializerMethodField()
    status_label = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioRequest
        fields = ['uuid', 'balance_ratio', 'preset', 'preset_label', 'status_label', 'created_at', 'result']
        read_only_fields = ['uuid', 'status', 'created_at']

    def get_preset_label(self, obj):
        return obj.get_preset_display()

    def get_status_label(self, obj):
        return obj.get_status_display()

    def get_result(self, obj):
        if obj.status != PortfolioRequestStatus.COMPLETED: return None

        result = PortfolioResult.objects.filter(request_no=obj.no).first()
        if not result: return None

        items = PortfolioResultItem.objects.filter(result_no=result.no).values(
            "security_code", "security_name", "price", "units", "amount"
        )

        return {
            "invested_balance": result.invested_balance,
            "items": list(items)
        }

    def validate(self, data):
        preset = data.get('preset')
        balance_ratio = data.get('balance_ratio')

        if not preset and balance_ratio is None:
            raise serializers.ValidationError("[AIM]preset 또는 balance_ratio 중 하나는 반드시 입력해야 합니다.")

        if preset == PortfolioRequestPreset.AGGRESSIVE:
            data['balance_ratio'] = Decimal("1.00")
        elif preset == PortfolioRequestPreset.MODERATE:
            data['balance_ratio'] = Decimal("0.50")

        if 'balance_ratio' in data:
            if not (Decimal("0.01") <= data['balance_ratio'] <= Decimal("1.00")):
                raise serializers.ValidationError("[AIM]balance_ratio는 0.01 이상 1.00 이하여야 합니다.")

        return data


# 증권 등록
class SecuritiesMarketRegisterSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=16)
    name = serializers.CharField(max_length=128)
    price = serializers.IntegerField(min_value=1)
    class Meta:
        model = SecuritiesMarket
        fields = ['code', 'name', 'price']
    
    def validate_code(self, value):
        if SecuritiesMarket.objects.filter(code=value).exists():
            raise serializers.ValidationError("[AIM]이미 등록된 증권 코드입니다.")
        return value

# 증권 수정
class SecuritiesMarketUpdatePriceSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=16)
    price = serializers.IntegerField(min_value=1)

    def validate_code(self, value):
        if not SecuritiesMarket.objects.filter(code=value).exists():
            raise serializers.ValidationError("[AIM]해당 증권이 존재하지 않습니다.")
        return value

#증권 삭제
class SecuritiesMarketDeleteSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=16)

    def validate_code(self, value):
        if not SecuritiesMarket.objects.filter(code=value).exists():
            raise serializers.ValidationError("[AIM]해당 증권이 존재하지 않습니다.")
        return value