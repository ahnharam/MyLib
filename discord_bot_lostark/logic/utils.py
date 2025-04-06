# logic/utils.py

import datetime

def parse_time_string(time_str: str) -> datetime.datetime:
    try:
        hour, minute = map(int, time_str.split(":"))
        now = datetime.datetime.now()
        return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    except ValueError:
        raise ValueError("❌ 시간 형식이 잘못되었습니다. `HH:MM` 형태로 입력해주세요.")
