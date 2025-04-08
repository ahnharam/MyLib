# logic/scheduler_helper.py

import discord
import datetime

from database.raids import get_future_raids
from database.participants import is_already_joined
from database.raids import get_raid_with_participants_by_title

from apscheduler.triggers.date import DateTrigger

# 레이드 알림 설정 함수
def schedule_raid_alarm(scheduler, alarm_time, server_id, raid_id, boss_name, scheduled_time):
    print(f"📌 예약 시도: {boss_name} → 알림시각 {alarm_time}, 현재 {datetime.datetime.now()}")

    if alarm_time > datetime.datetime.now():
        scheduler.add_job(
            func=send_raid_alarm,
            trigger=DateTrigger(run_date=alarm_time),
            args=[server_id, raid_id, boss_name, scheduled_time],  # ✅ 여기에 추가됨
            id=f"alarm_{raid_id}",
            replace_existing=True,
            misfire_grace_time=600,
        )
        print(f"✅ 예약 완료: alarm_{raid_id}")
    else:
        print(f"⚠️ 예약 스킵: {boss_name} 알림은 과거 시각 {alarm_time}이라 무시됨")


# 레이드 알림 DM 발송 함수
# 🔔 참가자 대상 DM 알림 함수 (스케줄러에서 호출됨)
async def send_raid_alarm(server_id, raid_id, title, scheduled_time):
    guild = discord.utils.get(bot.guilds, id=int(server_id))
    if not guild:
        print(f"[알림 실패] 서버 {server_id}를 찾을 수 없습니다.")
        return

    print(f"[알림 예약 실행] {title} 레이드 알림 시작")

    # 참가자 목록 조회
    _, participants = get_raid_with_participants_by_title(server_id, title)
    if not participants:
        print(f"[알림 스킵] 참가자가 없어 알림을 발송하지 않습니다.")
        return

    # 알림 Embed 메시지 구성
    embed = discord.Embed(
        title=f"⏰ {title} 레이드 알림",
        description=f"10분 후 시작 예정입니다! 🕒 `{scheduled_time.strftime('%H:%M')}`",
        color=discord.Color.orange()
    )
    embed.add_field(name="👥 참가자 수", value=f"{len(participants)}명", inline=True)

    # 참가자 닉네임 리스트
    name_list = []
    for user_id in participants:
        member = guild.get_member(int(user_id))
        if member:
            name_list.append(f"- {member.display_name}")
    if name_list:
        embed.add_field(name="📋 참가자 목록", value="\n".join(name_list), inline=False)

    # 참가자에게만 DM 발송
    for user_id in participants:
        member = guild.get_member(int(user_id))
        if not member or member.bot:
            continue
        try:
            await member.send(embed=embed)
        except Exception as e:
            print(f"[DM 실패] {member.display_name if member else user_id} → {e}")

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

        if alarm_time > now:
            schedule_raid_alarm(scheduler, alarm_time, server_id, raid_id, title, scheduled_time)  # ✅ 여기에 scheduled_time 전달
            print(f"✅ 재등록: {title} @ {alarm_time.strftime('%H:%M')}")

    print("✅ [완료] 레이드 알림 재등록")
