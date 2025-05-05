
# 허용되지 않은 메시지는 fallback 메시지로 대신 반환합니다.
def filter_allow_error_message(message, fallback="알 수 없는 에러입니다."):
    return message.replace("[AIM]", "") if message.startswith("[AIM]") else fallback

# serializer error 메시지에서 외부 노출이 허용된 메시지를 자동으로 반환합니다.
def filter_error_message(serializer_error, fallback='알 수 없는 에러입니다.'):
    field = next(iter(serializer_error))
    error_msg = serializer_error[field][0]
    filtered_message = filter_allow_error_message(error_msg)
    print(error_msg)
    return dict(field = field, message = filtered_message)