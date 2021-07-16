# 시간 정보를 년,월,일,시간,분 으로 변환
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)