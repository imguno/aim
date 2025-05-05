from django.db import models
from django.utils import timezone
import uuid

class Member(models.Model):
    no = models.AutoField(primary_key=True) 
    id = models.CharField(max_length=100, unique=True) 
    password = models.CharField(max_length=128) 
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 


class MembersHistory(models.Model):
    no = models.AutoField(primary_key=True)
    member_no = models.IntegerField()
    event_code = models.IntegerField()
    action = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    reason = models.TextField(blank=True)

    session_key = models.CharField(max_length=100, blank=True, null=True)
    request_meta = models.JSONField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['member_no', 'event_code']), 
        ]