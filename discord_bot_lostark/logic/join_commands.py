from discord.ext import commands
from database import get_latest_raid, is_already_joined, join_raid, cancel_participation
import pymysql

# 레이드 참가 명령어 (!참가)
@commands.command()
async def 참가(ctx):
    try:
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        # 최신 레이드 ID 가져오기
        try:
            raid_id = get_latest_raid(server_id)
        except pymysql.err.OperationalError:
            await ctx.send("❌ 데이터베이스 연결에 실패했습니다. 나중에 다시 시도해주세요.")
            return

        if not raid_id:
            await ctx.send("⚠️ 현재 등록된 레이드가 없습니다.")
            return

        # 중복 참가 여부 확인
        try:
            if is_already_joined(raid_id, user_id):
                await ctx.send("⚠️ 이미 이 레이드에 참가하셨습니다.")
                return
        except pymysql.err.OperationalError:
            await ctx.send("❌ 참가자 확인 중 오류가 발생했습니다.")
            return

        # 참가 처리
        try:
            join_raid(raid_id, user_id)
            await ctx.send(f"✅ {ctx.author.display_name} 님이 레이드에 참가하셨습니다!")
        except pymysql.err.IntegrityError:
            await ctx.send("❌ 참가 처리 중 문제가 발생했습니다.")
            return

    except Exception as e:
        await ctx.send(f"⚠️ 알 수 없는 오류가 발생했습니다: `{str(e)}`")

@commands.command()
async def 취소(ctx):
    try:
        server_id = str(ctx.guild.id)
        user_id = str(ctx.author.id)

        # 최신 레이드 ID 가져오기
        raid_id = get_latest_raid(server_id)

        if not raid_id:
            await ctx.send("⚠️ 취소할 수 있는 레이드가 없습니다.")
            return

        # 참가 여부 확인
        if not is_already_joined(raid_id, user_id):
            await ctx.send("⚠️ 현재 레이드에 참가 중이 아닙니다.")
            return

        # 참가 취소 처리
        cancel_participation(raid_id, user_id)
        await ctx.send(f"❎ {ctx.author.display_name} 님의 참가가 취소되었습니다.")

    except Exception as e:
        await ctx.send(f"⚠️ 참가 취소 중 오류 발생: `{str(e)}`")
