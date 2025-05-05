from rest_framework.response import Response
from rest_framework import status

def login_required(view_func):
    def wrapper(self, request, *args, **kwargs):
        if not request.session.get("member_no"):
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(self, request, *args, **kwargs)
    return wrapper

def is_admin(view_func):
    def wrapper(self, request, *args, **kwargs):

        if not request.session.get("member_no"):
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        # 관리자 계정 확인
        is_admin = True
        if is_admin:
            return view_func(self, request, *args, **kwargs)
        return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
                 
    return wrapper