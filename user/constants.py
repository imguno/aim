# 유저 히스토리 관련 이벤트 
class UserHistoryEventCode:

    # 로그인
    class Signin:
        BASE = 1000
        SUCCESS = BASE + 0
        WRONG_PASSWORD = BASE + 300 + 1
        NO_SUCH_ID = BASE + 300 + 2
        INTERNAL_ERROR = BASE + 400 + 1

    # 로그아웃
    class Signout:
        BASE = 2000
        SUCCESS = BASE + 0

    # 회원가입
    class Signup:
        BASE = 5000
        SUCCESS = BASE + 0
        DUPLICATE_ID = BASE + 300 + 1
        INTERNAL_ERROR = BASE + 400 + 1

    _messages = {
        Signin.SUCCESS: "로그인 성공",
        Signin.WRONG_PASSWORD: "비밀번호가 올바르지 않습니다.",
        Signin.NO_SUCH_ID: "존재하지 않는 ID입니다.",
        Signin.INTERNAL_ERROR: "로그인 중 서버 오류가 발생했습니다.",

        Signout.SUCCESS: "로그아웃 성공",

        Signup.SUCCESS: "회원가입 성공",
        Signup.DUPLICATE_ID: "이미 사용 중인 ID입니다.",
        Signup.INTERNAL_ERROR: "회원가입 중 서버 오류가 발생했습니다.",
    }

    @classmethod
    def get_message(cls, code):
        return cls._messages.get(code, f"지정되지 않은 이벤트 코드: {code}")
