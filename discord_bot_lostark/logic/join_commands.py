from discord.ext import commands
from database.participants import (
    is_already_joined,
    add_participant,
    remove_participant
)
from database.raids import get_raid_with_participants_by_title
import discord

# ✅ 레이드 참가 명령어
@commands.command()
async def 참가(ctx, 보스명: str = None):
    if not 보스명:
        await ctx.send("❌ 사용법: `!참가 [보스명]`")
        return

    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    try:
        raid_info, _ = get_raid_with_participants_by_title(server_id, 보스명)
        if not raid_info:
            await ctx.send(f"⚠️ `{보스명}` 레이드는 등록되어 있지 않습니다.")
            return

        raid_id, title, time = raid_info

        if is_already_joined(raid_id, user_id):
            await ctx.send("⚠️ 이미 참가한 레이드입니다.")
            return

        add_participant(raid_id, user_id)
        await ctx.send(f"✅ `{title}` 레이드({time.strftime('%H:%M')})에 참가 완료!")

    except Exception as e:
        await ctx.send(f"❌ 참가 중 오류 발생: `{str(e)}`")

# ✅ 레이드 참가 취소 명령어
@commands.command()
async def 취소(ctx, 보스명: str = None):
    if not 보스명:
        await ctx.send("❌ 사용법: `!취소 [보스명]`")
        return

    server_id = str(ctx.guild.id)
    user_id = str(ctx.author.id)

    try:
        raid_info, _ = get_raid_with_participants_by_title(server_id, 보스명)
        if not raid_info:
            await ctx.send(f"⚠️ `{보스명}` 레이드는 등록되어 있지 않습니다.")
            return

        raid_id, title, time = raid_info

        if not is_already_joined(raid_id, user_id):
            await ctx.send("⚠️ 아직 참가하지 않은 레이드입니다.")
            return

        remove_participant(raid_id, user_id)
        await ctx.send(f"🗑️ `{title}` 레이드({time.strftime('%H:%M')}) 참가를 취소했어요.")

    except Exception as e:
        await ctx.send(f"❌ 취소 중 오류 발생: `{str(e)}`")
