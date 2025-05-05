from rest_framework import serializers
from .models import Member, MembersHistory
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
import re


class SignupSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        max_length=100,
        error_messages={
            'max_length': '[AIM]아이디는 100자 이하로 입력해 주세요.',
            'required': '[AIM]아이디를 입력해 주세요.',
        },
    )

    password = serializers.CharField(
        write_only=True,
        max_length=128,
        error_messages={
            'max_length': '[AIM]비밀번호는 128자 이하로 입력해 주세요.',
            'required': '[AIM]비밀번호를 입력해 주세요.',
        }
    )
    
    class Meta:
        model = Member
        fields = ['id', 'password']
    
    def validate_id(self, value):
        if Member.objects.filter(id=value).exists():
            raise serializers.ValidationError("[AIM]이미 사용 중인 아이디입니다.")
        return value

    def validate_password(self, value):
        if len(value) < 8 :
            raise serializers.ValidationError("[AIM]비밀번호는 최소 8자 이어야 합니다.")

        conditions = 0
        if re.search(r'[A-Z]', value): conditions += 1
        if re.search(r'[a-z]', value): conditions += 1
        if re.search(r'[0-9]', value): conditions += 1
        if len(re.findall(r'[!@#$%^&*(),.?\":{}|<>]', value)) >= 2: conditions += 1

        if conditions < 3:
            raise serializers.ValidationError("[AIM]비밀번호 보안 조건을 최소 3개 이상 만족해야 합니다.")
        return value
        
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password']) 
        return super().create(validated_data)

class SigninSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(write_only=True)

class MembersHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MembersHistory
        fields = [
            'event_code',
            'action',
            'result',
            'reason',
            'session_key',
            'request_meta',
            'created_at'
        ]