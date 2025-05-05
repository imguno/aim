from django.db import models

class MemberBalance(models.Model):
    member_no = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0)

class TransactionType(models.TextChoices):
    DEPOSIT = 'deposit', '입금'
    WITHDRAW = 'withdraw', '출금'

class MemberTransaction(models.Model):
    member_no = models.IntegerField()
    tx_type = models.CharField(max_length=10, choices=TransactionType.choices)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    balance_after = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)