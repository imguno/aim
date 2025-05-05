from django.db import models
from decimal import Decimal
from django.utils import timezone
import uuid


# 포트폴리오 관련
class PortfolioRequestPreset(models.TextChoices):
    AGGRESSIVE = "aggressive", "공격형"
    MODERATE = "moderate", "중간형"

class PortfolioRequestStatus(models.IntegerChoices):
    REQUESTED = 0, "요청됨"
    IN_PROGRESS = 1, "작업중"
    COMPLETED = 2, "완료됨"
    FAIL = 4, "자문 실패"

class PortfolioRequest(models.Model):
    no = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    member_no = models.IntegerField()
    preset = models.CharField(
        choices=PortfolioRequestPreset.choices,
        max_length=10, null=True, blank=True
    )
    balance_ratio  = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        choices=PortfolioRequestStatus.choices,
        default=PortfolioRequestStatus.REQUESTED
    )
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


class PortfolioResult(models.Model):
    no = models.AutoField(primary_key=True)

    request_no = models.IntegerField(unique=True, editable=False)

    invested_balance = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        indexes = [
            models.Index(fields=["request_no"])
        ]

class PortfolioResultItem(models.Model):
    no = models.AutoField(primary_key=True)

    result_no = models.IntegerField()

    security_code = models.CharField(max_length=16)
    security_name = models.CharField(max_length=128)

    price = models.PositiveIntegerField()
    units = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        indexes = [
            models.Index(fields=["result_no"])
        ]


# 증권 관련
class SecuritiesMarket(models.Model):
    no = models.AutoField(primary_key=True)
    code = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

