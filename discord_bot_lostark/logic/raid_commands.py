import datetime
import discord
from discord.ext import commands

# 데이터베이스 레이어
from database.raids import (
    insert_raid,
    get_latest_raid,
    get_all_raids_with_count,
    get_raid_with_participants_by_title,
    get_raid_by_title_and_time,
    get_raid_with_creator_by_title,
    delete_raid,
    recreate_raid_with_new_time
)
from database.participants import is_already_joined

# 로직 / 스케줄러 유틸
from logic.utils import parse_time_string
from logic.scheduler_helper import schedule_raid_alarm  # send_raid_alarm은 scheduler 내부에서만 사용



scheduler = None    # bot.py에서 주입됨  
bot = None          # DM 보낼 때 필요 bot.py에서 주입됨  

# 레이드 등록 명령어 (!레이드등록 보스명 시간)
@commands.command()
async def 레이드등록(ctx, 보스명: str = None, 시간: str = None):
    if not 보스명 or not 시간:
        await ctx.send("❌ 사용법: `!레이드등록 [보스명] [시간]` 예: `!레이드등록 에키드나 21:30`")
        return

    try:
        raid_time = parse_time_string(시간)
    except ValueError as ve:
        await ctx.send(str(ve))
        return

    server_id = str(ctx.guild.id)
    creator_id = str(ctx.author.id)

    try:
        insert_raid(server_id, 보스명, creator_id, raid_time)
    except ValueError as ve:
        await ctx.send(f"⚠️ {str(ve)}")
        return
    except Exception as e:
        await ctx.send(f"⚠️ 등록 중 오류 발생: `{str(e)}`")
        return

    await ctx.send(f"✅ **[{보스명}]** 레이드를 **{시간}**에 등록했어요!")

    try:
        raid_id = get_latest_raid(server_id)
        if not raid_id:
            return

        alarm_time = raid_time - datetime.timedelta(minutes=10)
        schedule_raid_alarm(scheduler, alarm_time, ctx.guild.id, raid_id, 보스명)
    except Exception as e:
        print(f"[알림 예약 실패] {e}")

# 레이드 목록 조회 명령어 (!목록)
@commands.command()
async def 목록(ctx):
    server_id = str(ctx.guild.id)

    try:
        raids = get_all_raids_with_count(server_id)

        if not raids:
            await ctx.send("⚠️ 현재 등록된 레이드가 없습니다.")
            return

        embed = discord.Embed(
            title=f"📋 현재 등록된 레이드 목록 ({len(raids)}개)",
            color=discord.Color.blue()
        )

        for raid in raids:
            raid_id, title, time, count = raid
            embed.add_field(
                name=f"🛡 {title} - {time.strftime('%H:%M')}",
                value=f"{count}명 참가 중",
                inline=False
            )

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"⚠️ 레이드 목록 불러오기 중 오류 발생: `{str(e)}`")


# 레이드 상세 조회 명령어 (!상세 보스명)
@commands.command()
async def 상세(ctx, 보스명: str = None):
    if not 보스명:
        await ctx.send("❌ 사용법: `!상세 [보스명]` 예: `!상세 에키드나`")
        return

    server_id = str(ctx.guild.id)

    try:
        raid_info, participants = get_raid_with_participants_by_title(server_id, 보스명)

        if not raid_info:
            await ctx.send(f"⚠️ `{보스명}` 레이드는 등록되어 있지 않습니다.")
            return

        _, title, time = raid_info

        embed = discord.Embed(
            title=f"📋 {title} 레이드 상세 정보",
            description=f"🕒 시간: {time.strftime('%H:%M')}\n👥 참가자 수: {len(participants)}명",
            color=discord.Color.green()
        )

        if participants:
            names = []
            for user_id in participants:
                member = ctx.guild.get_member(int(user_id))
                names.append(f"- {member.display_name if member else '알 수 없음({user_id})'}")
            embed.add_field(name="👥 참가자 목록", value="\n".join(names), inline=False)
        else:
            embed.add_field(name="👥 참가자 목록", value="없음", inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        await ctx.send(f"⚠️ 레이드 상세 조회 중 오류 발생: `{str(e)}`")


# 레이드 삭제 명령어 (!레이드삭제 보스명 or !레이드삭제 보스명 시간)
@commands.command()
async def 레이드삭제(ctx, 보스명: str = None, 시간: str = None):
    if not 보스명:
        await ctx.send("❌ 사용법: `!레이드삭제 [보스명] [시간(선택)]` 예: `!레이드삭제 에키드나` 또는 `!레이드삭제 에키드나 21:30`")
        return

    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    # 시간까지 입력된 경우: 특정 시간 레이드 삭제
    if 시간:
        try:
            hour, minute = map(int, 시간.split(":"))
        except ValueError:
            await ctx.send("❌ 시간 형식이 잘못되었습니다. `HH:MM` 형태로 입력해주세요.")
            return

        result = get_raid_by_title_and_time(server_id, 보스명, hour, minute)
        if not result:
            await ctx.send(f"⚠️ `{보스명}` 레이드 ({시간})를 찾을 수 없습니다.")
            return

    # 시간 미입력 시: 가장 최근 레이드 삭제
    else:
        result = get_raid_with_creator_by_title(server_id, 보스명)
        if not result:
            await ctx.send(f"⚠️ `{보스명}` 레이드는 존재하지 않습니다.")
            return

    raid_id, creator_id = result

    # 작성자 본인 or 관리자만 삭제 가능
    if user_id != creator_id and not ctx.author.guild_permissions.administrator:
        await ctx.send("🚫 이 레이드를 삭제할 권한이 없습니다.")
        return

    delete_raid(raid_id)

    # 스케줄 제거
    try:
        scheduler.remove_job(f"alarm_{raid_id}")
    except:
        pass

    msg_time = 시간 if 시간 else "최근"
    await ctx.send(f"🗑️ `{보스명}` 레이드 ({msg_time})를 성공적으로 삭제했습니다.")

@commands.command()
async def 레이드수정(ctx, 보스명: str = None, 기존시간: str = None, 새시간: str = None):
    if not 보스명 or not 기존시간 or not 새시간:
        await ctx.send("❌ 사용법: `!레이드수정 [보스명] [기존시간] [새시간]`\n예: `!레이드수정 베히모스 20:30 21:00`")
        return

    try:
        hour, minute = map(int, 기존시간.split(":"))
        new_time = parse_time_string(새시간)
    except ValueError:
        await ctx.send("❌ 시간 형식이 잘못되었습니다. `HH:MM` 형식으로 입력해주세요.")
        return

    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    result = get_raid_by_title_and_time(server_id, 보스명, hour, minute)
    if not result:
        await ctx.send(f"⚠️ `{보스명}` 레이드 ({기존시간})를 찾을 수 없습니다.")
        return

    old_raid_id, creator_id = result

    if user_id != creator_id and not ctx.author.guild_permissions.administrator:
        await ctx.send("🚫 이 레이드를 수정할 권한이 없습니다.")
        return

    try:
        # 1. 기존 레이드 Soft Delete + 새 레이드 등록
        new_raid_id = recreate_raid_with_new_time(old_raid_id, new_time)

        # 2. 알림 스케줄 새로 등록
        try:
            scheduler.remove_job(f"alarm_{old_raid_id}")
        except:
            pass

        alarm_time = new_time - datetime.timedelta(minutes=10)
        schedule_raid_alarm(scheduler, alarm_time, ctx.guild.id, new_raid_id, 보스명)

        await ctx.send(f"🔄 `{보스명}` 레이드를 **{기존시간} → {새시간}** 으로 수정했습니다.")

    except Exception as e:
        await ctx.send(f"❌ 레이드 수정 실패: `{str(e)}`")
