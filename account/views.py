from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import MemberBalance, MemberTransaction, TransactionType
from user.models import Member
from .serializers import TransactionRequestSerializer, TransactionHistorySerializer
from config import decorator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BalanceView(APIView):
    @swagger_auto_schema(
        tags=["2. ACCOUNT API"],
        operation_id="잔고 조회",
        responses={
            200: openapi.Response(
                description="현재 잔고 조회 결과",
                examples={
                    "application/json": {
                        "balance": "150000"
                    }
                }
            )
        }
    )

    @decorator.login_required
    def get(self, request):
        member_no = request.session.get("member_no")
        balance = MemberBalance.objects.filter(member_no=member_no).first()
        amount = balance.amount if balance else 0
        return Response({"balance": str(amount)})

class BalanceHistoryView(APIView):
    @swagger_auto_schema(
        tags=["2. ACCOUNT API"],
        operation_id="입출금 내역",
        responses={
            200: openapi.Response(
                description="입출금 트랜잭션 목록",
                examples={
                    "application/json": [
                        {
                            "tx_type": "deposit",
                            "amount": 10000,
                            "balance_after": 15000,
                            "description": "첫 입금",
                            "created_at": "2025-05-06T01:34:00Z"
                        },
                        {
                            "tx_type": "withdraw",
                            "amount": 5000,
                            "balance_after": 10000,
                            "description": "ATM 출금",
                            "created_at": "2025-05-06T01:35:00Z"
                        }
                    ]
                }
            )
        }
    )

    @decorator.login_required
    def get(self, request):
        member_no = request.session.get("member_no")
        history = MemberTransaction.objects.filter(member_no=member_no).order_by('-created_at')
        serializer = TransactionHistorySerializer(history, many=True)

        return Response(serializer.data)

class DepositView(APIView):

    @swagger_auto_schema(
        tags=["2. ACCOUNT API"],
        operation_id="입금",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["amount"],
            properties={
                "amount": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="입금할 금액 (예: 10000)"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="입금 메모",
                    maxLength=255
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="입금 성공",
                examples={
                    "application/json": {
                        "message": "입금 완료",
                        "balance": "20000"
                    }
                }
            ),
            400: openapi.Response(
                description="입력 오류",
                examples={
                    "application/json": {
                        "amount": ["금액은 0보다 커야 합니다."]
                    }
                }
            ),
            500: openapi.Response(
                description="서버 오류",
                examples={
                    "application/json": {
                        "message": "입금 처리 중 오류 발생"
                    }
                }
            )
        }
    )

    @decorator.login_required
    def post(self, request):
        member_no = request.session.get("member_no")
        serializer = TransactionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get('description', '')

        # 입출금 요청 시 검증 로직이 필요하지만 본 과제에서는 해당 검증 로직은 구현 범위에서 제외하였습니다.

        try:
            with transaction.atomic():
                balance, _ = MemberBalance.objects.select_for_update().get_or_create(member_no=member_no)
                balance.amount += amount
                balance.save()

                MemberTransaction.objects.create(
                    member_no=member_no,
                    tx_type=TransactionType.DEPOSIT,
                    amount=amount,
                    balance_after=balance.amount,
                    description=description,
                )

        except Exception as e:
            return Response({"message": f"입금 처리 중 오류 발생"}, status=500)

        return Response({"message": "입금 완료", "balance": str(balance.amount)})

class WithdrawView(APIView):
    @swagger_auto_schema(
        tags=["2. ACCOUNT API"],
        operation_id="출금",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["amount"],
            properties={
                "amount": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="출금할 금액 (예: 10000)"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="출금 메모",
                    maxLength=255
                )
            }
        ),
        responses={
            200: openapi.Response(
                description="출금 성공",
                examples={
                    "application/json": {
                        "message": "출금 완료",
                        "balance": "5000"
                    }
                }
            ),
            400: openapi.Response(
                description="잔고 부족 또는 입력 오류",
                examples={
                    "application/json": {
                        "message": "잔고 부족"
                    }
                }
            ),
            404: openapi.Response(
                description="잔고 정보 없음",
                examples={
                    "application/json": {
                        "message": "잔고 정보가 존재하지 않습니다."
                    }
                }
            ),
            500: openapi.Response(
                description="서버 오류",
                examples={
                    "application/json": {
                        "message": "출금 처리 중 오류가 발생"
                    }
                }
            )
        }
    )

    @decorator.login_required
    def post(self, request):
        member_no = request.session.get("member_no")
        serializer = TransactionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        amount = serializer.validated_data['amount']
        description = serializer.validated_data.get('description', '')

        # 입출금 요청 시 검증 로직이 필요하지만 본 과제에서는 해당 검증 로직은 구현 범위에서 제외하였습니다.

        try:
            with transaction.atomic():
                balance = MemberBalance.objects.select_for_update().get(member_no=member_no)
                if balance.amount < amount:
                    return Response({"message": "잔고 부족"}, status=400)

                balance.amount -= amount
                balance.save()

                MemberTransaction.objects.create(
                    member_no=member_no,
                    tx_type=TransactionType.WITHDRAW,
                    amount=amount,
                    balance_after=balance.amount,
                    description=description,
                )

        except MemberBalance.DoesNotExist:
            return Response({"message": "잔고 정보가 존재하지 않습니다."}, status=404)
        except Exception as e:
            return Response({"message": f"출금 처리 중 오류가 발생"}, status=500)

        return Response({"message": "출금 완료", "balance": str(balance.amount)})
