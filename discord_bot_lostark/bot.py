import os
import discord
import asyncio
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from logic import scheduler_helper
from logic import raid_commands, join_commands
from logic.scheduler_helper import load_pending_alarms
from cogs.raid_slash import RaidJoinView
from webserver import run_webserver  # ✅ Flask 백그라운드 실행용

# ✅ Flask로 더미 서버 실행 (Render 포트 열기용)
run_webserver()

# ✅ 환경변수에서 토큰 안전하게 가져오기
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN:
    raise RuntimeError("❌ DISCORD_TOKEN 환경변수가 설정되지 않았습니다.")

# ✅ 디스코드 봇 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ 스케줄러 생성 및 주입
scheduler = AsyncIOScheduler()
raid_commands.scheduler = scheduler
scheduler_helper.bot = bot

# ✅ 기본 명령어 등록
bot.add_command(raid_commands.레이드등록)
bot.add_command(raid_commands.레이드삭제)
bot.add_command(raid_commands.레이드수정)
bot.add_command(raid_commands.목록)
bot.add_command(raid_commands.상세)
bot.add_command(join_commands.참가)
bot.add_command(join_commands.취소)

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 성공: {bot.user.name}")
    try:
        synced = await bot.tree.sync()
        print(f"🌿 슬래시 명령어 등록 완료: {len(synced)}개")
    except Exception as e:
        print(f"❌ 슬래시 명령어 등록 실패: {e}")

    scheduler.start()
    await load_pending_alarms(scheduler)

async def main():
    bot.scheduler = scheduler
    await bot.load_extension("cogs.raid_slash")  # ✅ 슬래시 명령어 Cog 로딩
    bot.add_view(RaidJoinView())  # ✅ 버튼 View 등록 (persistent view)
    await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
