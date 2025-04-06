import discord
from config import DISCORD_TOKEN
from logic import scheduler_helper

from discord.ext import commands

# ✅ APScheduler 가져오기
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 명령어 모듈 import
from logic import raid_commands, join_commands
from logic.scheduler_helper import load_pending_alarms

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # ✅ 이걸 꼭 추가해야 get_member()가 작동함

bot = commands.Bot(command_prefix="!", intents=intents)

# ✅ 스케줄러 생성 및 시작
scheduler = AsyncIOScheduler()

# 스케줄러를 logic 모듈에서도 접근할 수 있도록 주입
raid_commands.scheduler = scheduler
scheduler_helper.bot = bot

# ✅ 명령어 등록 - add_command를 직접 추가하거나,
# 아래처럼 모듈 안에서 명령어가 등록되도록 해야 함

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

    scheduler.start()                      # 1️⃣ 먼저 스케줄러를 실행시키고
    await load_pending_alarms(scheduler)   # 2️⃣ 그 다음 알림들을 등록

bot.run(DISCORD_TOKEN)
