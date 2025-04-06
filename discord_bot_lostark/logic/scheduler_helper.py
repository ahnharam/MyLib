# logic/scheduler_helper.py

import discord
import datetime

from database.raids import get_future_raids
from database.participants import is_already_joined

from apscheduler.triggers.date import DateTrigger

# 레이드 알림 설정 함수
def schedule_raid_alarm(scheduler, alarm_time, server_id, raid_id, boss_name):
    print(f"📌 예약 시도: {boss_name} → 알림시각 {alarm_time}, 현재 {datetime.datetime.now()}")
    
    if alarm_time > datetime.datetime.now():
        scheduler.add_job(
            func=send_raid_alarm,
            trigger=DateTrigger(run_date=alarm_time),
            args=[server_id, raid_id, boss_name],
            id=f"alarm_{raid_id}",
            replace_existing=True,
            misfire_grace_time=600,
        )
        print(f"✅ 예약 완료: alarm_{raid_id}")
    else:
        print(f"⚠️ 예약 스킵: {boss_name} 알림은 과거 시각 {alarm_time}이라 무시됨")


# 레이드 알림 DM 발송 함수
async def send_raid_alarm(server_id, raid_id, title):
    guild = discord.utils.get(bot.guilds, id=int(server_id))
    if not guild:
        print(f"[알림 실패] 서버 {server_id}를 찾을 수 없습니다.")
        return

    print(f"[알림 예약 실행] {title} 레이드 알림 시작")

    for member in guild.members:
        if member.bot:
            continue
        try:
            if is_already_joined(raid_id, str(member.id)):
                await member.send(f"⏰ **[{title}] 레이드**가 10분 후에 시작됩니다!")
        except Exception as e:
            print(f"[DM 실패] {member.display_name} → {e}")

# ⏰ 봇 재시작 시, 미래 레이드들을 다시 APScheduler에 등록하는 함수
# - 알림 시각이 아직 유효한 레이드만 등록
# - 과거 알림은 조용히 무시 (별도 로그 없음)
async def load_pending_alarms(scheduler):
    print("📦 [시작] 미래 레이드 알림 재등록 중...")
    now = datetime.datetime.now()

    # 1. 미래 레이드 정보 DB에서 조회
    raids = get_future_raids(now)

    for raid in raids:
        raid_id, server_id, title, scheduled_time = raid
        alarm_time = scheduled_time - datetime.timedelta(minutes=10)

        # 2. 알림 시각이 아직 유효한 경우에만 재등록
        if alarm_time > now:
            schedule_raid_alarm(scheduler, alarm_time, server_id, raid_id, title)
            print(f"✅ 재등록: {title} @ {alarm_time.strftime('%H:%M')}")

    print("✅ [완료] 레이드 알림 재등록")
