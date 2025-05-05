from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PortfolioRequest, SecuritiesMarket
from .serializers import PortfolioRequestSerializer,SecuritiesMarketRegisterSerializer, SecuritiesMarketUpdatePriceSerializer, SecuritiesMarketDeleteSerializer
from config import decorator
from common.utils import filter_error_message

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .task import run_portfolio_progress

class PortfolioRequestView(APIView):
    @swagger_auto_schema(
        tags=["4. PORTFOLIO API"],
        operation_id="자문 요청",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[],
            properties={
                'preset': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='위험도 선택 (aggressive | moderate)',
                    enum=["aggressive", "moderate"]
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="자문 요청 성공",
                examples={
                    "application/json": {
                        "uuid": "a1b2c3d4-...",
                        "preset": "aggressive",
                        "balance_ratio": "1.00",
                        "status": 0,
                        "created_at": "2025-05-06T01:40:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="입력 오류",
                examples={
                    "application/json": {
                        "field": "preset",
                        "message": "허용된 투자 위험도가 아닙니다."
                    }
                }
            )
        }
    )
    @decorator.login_required
    def post(self, request):
        member_no = request.session.get("member_no")
        serializer = PortfolioRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_obj = serializer.save(member_no=member_no)
            # 자문요청 진행 시 시간이 소요될 수 있기 때문에 비동기로 진행
            run_portfolio_progress.delay(request_obj.no)
            return Response(PortfolioRequestSerializer(request_obj).data, status=201)
        return Response(filter_error_message(serializer.errors), status=400)


    @swagger_auto_schema(
        tags=["4. PORTFOLIO API"],
        operation_id="자문 내역 확인",
        responses={
            200: openapi.Response(
                description="자문 요청 리스트",
                examples={
                    "application/json": [
                        {
                            "uuid": "637bd118-25b9-48f9-96d6-1ae4c40f203b",
                            "balance_ratio": "1.00",
                            "preset": "aggressive",
                            "preset_label": "공격형",
                            "status_label": "완료됨",
                            "created_at": "2025-05-06T03:08:12.399482",
                            "result": {
                            "invested_balance": 22000,
                            "items": [
                                {
                                "security_code": "AIM001",
                                "security_name": "AIM",
                                "price": 1000,
                                "units": 22,
                                "amount": 22000
                                }
                            ]
                            }
                        },
                    ]
                }
            )
        }
    )
    @decorator.login_required
    def get(self, request):
        member_no = request.session.get("member_no")
        history = PortfolioRequest.objects.filter(
            member_no=member_no
        ).order_by('-created_at')

        serializer = PortfolioRequestSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SecuritiesRegisterView(APIView):

    @swagger_auto_schema(
        tags=["3. MARKET API"],
        operation_id="증권 등록",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["code", "name", "price"],
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING, description="증권 코드"),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="증권 이름"),
                "price": openapi.Schema(type=openapi.TYPE_INTEGER, description="가격 (원 단위)")
            }
        ),
        responses={
            201: openapi.Response(
                description="등록 성공",
                examples={
                    "application/json": {
                        "code": "005930",
                        "name": "삼성전자",
                        "price": 54300
                    }
                }
            ),
            400: openapi.Response(
                description="유효성 실패",
                examples={
                    "application/json": {
                        "code": "이미 등록된 증권입니다."
                    }
                }
            )
        }
    )

    @decorator.is_admin
    def post(self, request):
        serializer = SecuritiesMarketRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(filter_error_message(serializer.errors), status=400)

    @swagger_auto_schema(
        tags=["3. MARKET API"],
        operation_id="증권 조회",
        responses={
            200: openapi.Response(
                description="전체 증권 목록",
                examples={
                    "application/json": [
                        {
                            "code": "005930",
                            "name": "삼성전자",
                            "price": 54300
                        }
                    ]
                }
            )
        }
    )

    def get(self, request):
        securities = SecuritiesMarket.objects.all().order_by('-created_at')
        serializer = SecuritiesMarketRegisterSerializer(securities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SecuritiesUpdatePriceView(APIView):

    @swagger_auto_schema(
        tags=["3. MARKET API"],
        operation_id="증권 수정",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["code", "price"],
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING, description="증권 코드"),
                "price": openapi.Schema(type=openapi.TYPE_INTEGER, description="변경할 가격")
            }
        ),
        responses={
            200: openapi.Response(
                description="수정 완료",
                examples={
                    "application/json": {
                        "code": "005930",
                        "name": "삼성전자",
                        "price": 54300
                    }
                }
            ),
            400: openapi.Response(
                description="유효성 오류",
                examples={
                    "application/json": {
                        "code": "해당 증권이 존재하지 않습니다."
                    }
                }
            )
        }
    )

    @decorator.is_admin
    def post(self, request):
        serializer = SecuritiesMarketUpdatePriceSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            price = serializer.validated_data['price']
            security = SecuritiesMarket.objects.get(code=code)
            security.price = price
            security.save()
            return Response({
                "code": code,
                "name" : security.name,
                "price": price
            }, status=200)
        return Response(filter_error_message(serializer.errors), status=400)

class SecuritiesDeleteView(APIView):

    @swagger_auto_schema(
        tags=["3. MARKET API"],
        operation_id="증권 삭제",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["code"],
            properties={
                "code": openapi.Schema(type=openapi.TYPE_STRING, description="삭제할 증권 코드")
            }
        ),
        responses={
            200: openapi.Response(
                description="삭제 완료",
                examples={
                    "application/json": {
                        "message": "005930 증권이 삭제되었습니다.",
                    }
                }
            ),
            400: openapi.Response(
                description="유효성 오류",
                examples={
                    "application/json": {
                        "code": "해당 증권이 존재하지 않습니다."
                    }
                }
            )
        }
    )
    @decorator.is_admin
    def post(self, request):
        serializer = SecuritiesMarketDeleteSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            SecuritiesMarket.objects.filter(code=code).delete()
            return Response({"message": f"{code} 증권이 삭제되었습니다."}, status=200)
        return Response(filter_error_message(serializer.errors), status=400)