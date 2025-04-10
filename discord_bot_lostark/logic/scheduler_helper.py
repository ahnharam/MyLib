import discord
import datetime
from apscheduler.triggers.date import DateTrigger

from database.raids import (
    get_future_raids,
    get_raid_with_participants_by_title,
    get_all_raids_with_count
)

bot = None  # 외부에서 주입될 봇 인스턴스

# ✅ 알림 스케줄 등록 함수
def schedule_raid_alarm(scheduler, alarm_time, server_id, raid_id, boss_name, scheduled_time):
    print(f"📌 예약 시도: {boss_name} → 알림시각 {alarm_time}, 현재 {datetime.datetime.now()}")

    if alarm_time > datetime.datetime.now():
        scheduler.add_job(
            func=send_raid_alarm,
            trigger=DateTrigger(run_date=alarm_time),
            args=[server_id, raid_id, boss_name, scheduled_time],
            id=f"alarm_{raid_id}",
            replace_existing=True,
            misfire_grace_time=600,
        )
        print(f"✅ 예약 완료: alarm_{raid_id}")
    else:
        print(f"⚠️ 예약 스킵: {boss_name} 알림은 과거 시각 {alarm_time}이라 무시됨")


# ✅ 레이드 알림 DM 발송 함수
async def send_raid_alarm(server_id, raid_id, title, scheduled_time):
    if not bot:
        print("❌ 봇 인스턴스가 없습니다.")
        return

    guild = discord.utils.get(bot.guilds, id=int(server_id))
    if not guild:
        print(f"[알림 실패] 서버 {server_id}를 찾을 수 없습니다.")
        return

    print(f"[알림 예약 실행] {title} 레이드 알림 시작")

    _, participants = get_raid_with_participants_by_title(server_id, title)
    if not participants:
        print(f"[알림 스킵] 참가자가 없어 알림을 발송하지 않습니다.")
        return

    embed = discord.Embed(
        title=f"⏰ {title} 레이드 알림",
        description=f"10분 후 시작 예정입니다! 🕒 `{scheduled_time.strftime('%H:%M')}`",
        color=discord.Color.orange()
    )
    embed.add_field(name="👥 참가자 수", value=f"{len(participants)}명", inline=True)

    name_list = []
    for user_id in participants:
        member = guild.get_member(int(user_id))
        if member:
            name_list.append(f"- {member.display_name}")
    if name_list:
        embed.add_field(name="📋 참가자 목록", value="\n".join(name_list), inline=False)

    for user_id in participants:
        member = guild.get_member(int(user_id))
        if not member or member.bot:
            continue
        try:
            await member.send(embed=embed)
        except Exception as e:
            print(f"[DM 실패] {member.display_name if member else user_id} → {e}")


# ✅ 봇 재시작 시 미래 알림 재등록
async def load_pending_alarms(scheduler):
    print("📦 [시작] 미래 레이드 알림 재등록 중...")
    now = datetime.datetime.now()

    raids = get_future_raids(now)
    for raid in raids:
        raid_id, server_id, title, scheduled_time = raid
        alarm_time = scheduled_time - datetime.timedelta(minutes=10)

        if alarm_time > now:
            schedule_raid_alarm(scheduler, alarm_time, server_id, raid_id, title, scheduled_time)
            print(f"✅ 재등록: {title} @ {alarm_time.strftime('%H:%M')}")

    print("✅ [완료] 레이드 알림 재등록 완료")


# ✅ 전체 레이드 목록 조회 메시지 생성 (Embed)
async def generate_full_raid_list_embed(server_id: str):
    raids = get_all_raids_with_count(server_id)

    embed = discord.Embed(
        title="📅 전체 레이드 목록",
        description="예정된 모든 레이드를 확인할 수 있습니다.",
        color=discord.Color.teal()
    )

    if not raids:
        embed.add_field(name="레이드 없음", value="예정된 레이드가 없습니다.", inline=False)
    else:
        for raid in raids:
            raid_id, title, time, count = raid
            embed.add_field(
                name=f"[{raid_id}] {title}",
                value=f"⏰ {time.strftime('%Y-%m-%d %H:%M')}\n👥 참가자: {count}명",
                inline=False
            )

    return embed