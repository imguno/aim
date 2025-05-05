from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.contrib.auth.hashers import check_password
from .models import Member, MembersHistory
from .serializers import SignupSerializer, SigninSerializer, MembersHistorySerializer
from .constants import UserHistoryEventCode
from common.utils import filter_allow_error_message
from config import decorator

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# 기본 요구사항
# 로그인, 로그아웃 시에 이력을 저장해야 한다. 
# 추후 활용 가능성이 있는 메타 데이터도 추가로 저장합니다.
def sign_log_event(member_no, code, action, result, request):
    def extract_request_meta(request):
        keys = [
            "HTTP_USER_AGENT",
            "HTTP_REFERER",
            "HTTP_HOST",
            "HTTP_ACCEPT_LANGUAGE",
            "REMOTE_ADDR",
            "HTTP_X_FORWARDED_FOR",
        ]
        return {key: request.META.get(key) for key in keys if request.META.get(key) is not None}

    MembersHistory.objects.create(
        member_no=member_no,
        event_code=code,
        action=action,
        result=result,
        reason=UserHistoryEventCode.get_message(code),
        session_key=request.session.session_key,
        request_meta=extract_request_meta(request)
    )

# 회원가입 API
class SignupView(APIView):
    @swagger_auto_schema(
        tags=["1. USER API"],
        operation_id="회원가입",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'password'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
            }
        ),
        responses={
            201: openapi.Response(
                description="회원가입 성공",
                examples={
                    "application/json": {"message": "회원가입 완료"}
                }
            ),
            400: openapi.Response(
                description="유효성 검증 실패",
                examples={
                    "application/json": {
                        "field": "id",
                        "message": "이미 사용 중인 아이디입니다."
                    }
                }
            ),
            500: openapi.Response(
                description="서버 오류",
                examples={
                    "application/json": {
                        "message": "회원가입 처리 중 오류가 발생했습니다."
                    }
                }
            )
        }
    )

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    member = serializer.save()
                    code = UserHistoryEventCode.Signup.SUCCESS
                    sign_log_event(member.no, code, 'signup', 'success', request)
            except Exception as e:
                return Response(
                    {'message': '회원가입 처리 중 오류가 발생했습니다.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            return Response({'message': "회원가입 완료"}, status=status.HTTP_201_CREATED)

        errors = serializer.errors
        field = next(iter(errors))
        error_msg = errors[field][0]
        filtered_message = filter_allow_error_message(error_msg)
        return Response(
            {'field': field, 'message': filtered_message},
            status=status.HTTP_400_BAD_REQUEST
        )
   

# 로그인 API
class SigninView(APIView):
    @swagger_auto_schema(
        tags=["1. USER API"],
        operation_id="로그인 상태 확인",
        responses={
            200: openapi.Response(
                description="로그인 여부 반환",
                examples={
                    "application/json": {
                        "logged_in": True,
                        "uuid": "aaaaaaaa-bbbb-cccc-dddd-ffffffffffff"
                    }
                }
            )
        }
    )

    def get(self, request):
        if not request.session.get("member_no"):
            return Response({'logged_in': False}, status=status.HTTP_200_OK)
        try:
            member_no = request.session.get("member_no")
            member = Member.objects.get(no=member_no)
            return Response({
                'logged_in': True,
                'uuid': str(member.uuid)
            }, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({'logged_in': False}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=["1. USER API"],
        operation_id="로그인",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['id', 'password'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='비밀번호')
            }
        ),
        responses={
            200: openapi.Response(
                description="로그인 성공",
                examples={
                    "application/json": {
                        "logged_in": True,
                        "uuid": "aaaaaaaa-bbbb-cccc-dddd-ffffffffffff"
                    }
                }
            ),
            401: openapi.Response(
                description="로그인 실패",
                examples={
                    "application/json": {
                        "message": "아이디와 비밀번호를 확인해주세요."
                    }
                }
            )
        }
    )

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            try:
                member = Member.objects.get(id=serializer.validated_data['id'])
            except Member.DoesNotExist:
                return Response({'message': "아이디와 비밀번호를 확인해주세요."}, status=status.HTTP_401_UNAUTHORIZED)

            if check_password(serializer.validated_data['password'], member.password):
                request.session['member_no'] = member.no
                request.session.save()
                code = UserHistoryEventCode.Signin.SUCCESS
                sign_log_event(member.no, code, 'signin', 'success', request)
                return Response({
                    'logged_in': True,
                    'uuid': str(member.uuid)
                }, status=status.HTTP_200_OK)
            
            else:
                code = UserHistoryEventCode.Signin.WRONG_PASSWORD
                sign_log_event(member.no, code, 'signin', 'failure', request)
                return Response({'message': "아이디와 비밀번호를 확인해주세요."}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'message': "아이디와 비밀번호를 확인해주세요."}, status=status.HTTP_401_UNAUTHORIZED)


# 로그아웃 API
class SignoutView(APIView):
    
    @swagger_auto_schema(
        tags=["1. USER API"],
        operation_id="로그아웃",
        responses={
            200: openapi.Response(
                description="로그아웃 성공",
                examples={
                    "application/json": {
                        "message": "로그아웃되었습니다."
                    }
                }
            ),
            500: openapi.Response(
                description="서버 오류",
                examples={
                    "application/json": {
                        "message": "로그아웃 처리 중 오류가 발생했습니다."
                    }
                }
            )
        }
    )
    @decorator.login_required
    def post(self, request):
        member_no = request.session.get("member_no")
        try:
            code = UserHistoryEventCode.Signout.SUCCESS
            sign_log_event(member_no, code, 'signout', 'success', request)
            request.session.flush()

            return Response(
                {'message': "로그아웃되었습니다."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            print(e)
            return Response(
                {'message': '로그아웃 처리 중 오류가 발생했습니다.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# 사용자 이력 조회 (로그인/회원가입/로그아웃)
class SignHistoryView(APIView):
    @swagger_auto_schema(
        tags=["1. USER API"],
        operation_id="사용자 이력 조회",
        responses={
            200: openapi.Response(
                description="사용자의 로그인/회원가입/로그아웃 등 이력 목록",
                examples={
                    "application/json": [
                        {
                            "event_code": 1001,
                            "action": "signin",
                            "result": "success",
                            "reason": "",
                            "session_key": "abc123...",
                            "ip_address": "192.168.0.1",
                            "user_agent": "Mozilla/5.0...",
                            "extra": {
                                "HTTP_REFERER": "...",
                                "HTTP_ACCEPT_LANGUAGE": "..."
                            },
                            "created_at": "2025-05-06T01:12:00Z"
                        },
                    ]
                }
            )
        }
    )
    @decorator.login_required
    def get(self, request):
        member_no = request.session.get("member_no")
        history = MembersHistory.objects.filter(
            member_no=member_no
        ).order_by('-created_at')

        serializer = MembersHistorySerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
