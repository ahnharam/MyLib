import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from discord.ui import View, Button, Select
from discord.ext import commands
import json
import os

# 환경 변수에서 토큰 로드 (dotenv 사용 시)
from dotenv import load_dotenv

load_dotenv()

# 토큰 로드
TOKEN = os.getenv("DISCORD_TOKEN")
# 인원 로드
DATA_FILE = "members.json"

# 봇 초기화
intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.message_content = True 
intents.members = True  # 멤버 정보를 읽을 수 있도록 활성화
bot = commands.Bot(command_prefix="$", intents=intents)

# 스케줄러 설정
scheduler = AsyncIOScheduler()
# 가능한 시간 저장
availability = {}

def load_data():
    """JSON 파일에서 데이터를 로드"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}  # 파일이 없으면 빈 딕셔너리 반환

def save_data(data):
    """데이터를 JSON 파일에 저장"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# 멤버 데이터를 JSON에서 로드
participants = load_data()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    scheduler.start()  # 스케줄러 시작
    global participants
    participants = load_data()  # JSON 데이터 불러오기
    
    # 등록된 명령어를 출력
    command_list = [command.name for command in bot.commands]
    for command in command_list:
        print(f"- {command}")
    
    # 명령어 목록을 특정 채널에 보내는 코드 (선택 사항)
    # 디스코드 서버의 특정 텍스트 채널 ID를 설정해 메시지를 보낼 수 있습니다.
    guild = bot.guilds[0]  # 첫 번째 서버로 접근 (필요시 변경)
    default_channel = guild.text_channels[0]  # 첫 번째 채널로 접근 (필요시 변경)
    
    # 디스코드 채널에 보내는 메세지
    # try:
    #     await default_channel.send(
    #         "봇이 성공적으로 시작되었습니다. 등록된 명령어 목록:\n" +
    #         "\n".join([f"`{command}`" for command in command_list])
    #     )
    # except discord.Forbidden:
    #     print("디폴트 채널에 메시지를 보낼 수 없습니다.")

# 인사
@bot.command(name="인사")
async def hello(ctx):
    await ctx.send("안녕하세요! 저는 디스코드 봇입니다.")

# 멤버 추가
@bot.command(name="멤버추가")
async def add_member(ctx, member: discord.Member):
    """참여 멤버 추가"""
    member_id = str(member.id)  # ID를 문자열로 저장
    if member_id in participants:
        await ctx.send(f"{member.name}은(는) 이미 참여 멤버입니다.")
        return
    
    participants[member_id] = {"name": member.name}
    save_data(participants)  # JSON 파일에 저장
    await ctx.send(f"{member.name}을(를) 참여 멤버로 추가했습니다.")


# 멤버 삭제
@bot.command(name="멤버삭제")
async def remove_member(ctx, member: discord.Member):
    """참여 멤버 제거"""
    if member.id not in participants:
        await ctx.send(f"{member.name}은(는) 참여 멤버가 아닙니다.")
        return
    
    del participants[member.id]
    save_data(participants)  # JSON 파일에 저장
    await ctx.send(f"{member.name}을(를) 참여 멤버에서 제거했습니다.")


# DM 전송
@bot.command(name="DM전송")
async def send_dm(ctx):
    """월요일 DM 발송"""
    for member_id in participants.keys():
        member = await bot.fetch_user(member_id)
        await member.send("이번 주에 가능한 날짜와 시간을 선택해 주세요!")
    await ctx.send("DM을 발송했습니다.")

# 멤버 목록 조회
@bot.command(name="멤버목록조회")
async def list_members(ctx):
    """참여 멤버 목록 출력"""
    if not participants:
        await ctx.send("참여 멤버가 없습니다.")
        return

    member_list = []
    for member_id in participants:
        try:
            user = bot.get_user(member_id) or await bot.fetch_user(member_id)
            member_list.append(f"{user.name}")
        except Exception:
            member_list.append(f"Unknown Member (ID: {member_id})")

    member_list_str = "\n".join(member_list)
    await ctx.send(f"참여 멤버 목록:\n{member_list_str}")


# 매주 월요일 참여 멤버들에게 DM 보내기
async def send_weekly_dm():
    """참여 멤버들에게 매주 월요일 DM 발송"""
    for member_id in participants:
        user = bot.get_user(member_id)
        if user:
            try:
                await user.send(
                    "이번 주 가능한 요일과 시간을 입력해주세요! 형식: '월/화/수/목/금 10:00~12:00'"
                )
            except discord.Forbidden:
                print(f"{user}님에게 DM을 보낼 수 없습니다.")
    print("주간 DM 발송 완료!")

# 매주 월요일 오전 10시에 스케줄링
scheduler.add_job(send_weekly_dm, 'cron', day_of_week='mon', hour=10)

@bot.event
async def on_message(message):
    """사용자 메시지 처리"""
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        user_id = message.author.id
        if user_id in participants:
            # 사용자의 입력을 저장
            availability[user_id] = message.content
            await message.channel.send(f"가능한 시간 '{message.content}'이(가) 저장되었습니다.")
        else:
            await message.channel.send("참여 멤버가 아니므로 데이터를 저장할 수 없습니다.")
    await bot.process_commands(message)

# 날짜 선택
@bot.command(name="날짜선택")
async def select_day(ctx):
    """요일 선택 인터페이스를 제공"""
    # 디버깅용: 요청한 사용자의 ID 출력
    print(f"요청한 사용자 ID: {ctx.author.id}")
    print(f"현재 참여 멤버: {participants}")

    # 참여 멤버 확인
    if str(ctx.author.id) not in participants:
        await ctx.send("참여 멤버가 아닙니다. /add_member 명령어로 추가하세요.")
        return


    # 요일 선택 UI 표시
    view = DaySelectView(user_id=ctx.author.id)
    try:
        await ctx.author.send("가능한 요일을 선택하세요.", view=view)
    except discord.Forbidden:
        await ctx.send(f"{ctx.author.name}은(는) DM을 차단했기 때문에 메시지를 보낼 수 없습니다.")

class DaySelectView(View):
    """요일 선택 버튼 및 다음 단계 호출"""
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("이 버튼은 당신을 위한 것이 아닙니다!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="월요일", style=discord.ButtonStyle.primary)
    async def select_monday(self, interaction: discord.Interaction, button: Button):
        await self.handle_day_selection(interaction, "월요일")

    @discord.ui.button(label="화요일", style=discord.ButtonStyle.primary)
    async def select_tuesday(self, interaction: discord.Interaction, button: Button):
        await self.handle_day_selection(interaction, "화요일")
        
    @discord.ui.button(label="수요일", style=discord.ButtonStyle.primary)
    async def select_wednesday(self, interaction: discord.Interaction, button: Button):
        await self.handle_day_selection(interaction, "수요일")
        
    @discord.ui.button(label="목요일", style=discord.ButtonStyle.primary)
    async def select_thursday(self, interaction: discord.Interaction, button: Button):
        await self.handle_day_selection(interaction, "목요일")
        
    @discord.ui.button(label="금요일", style=discord.ButtonStyle.primary)
    async def select_friday(self, interaction: discord.Interaction, button: Button):
        await self.handle_day_selection(interaction, "금요일")

    async def handle_day_selection(self, interaction: discord.Interaction, day: str):
        await interaction.response.send_message(f"{day}를 선택했습니다. 시간을 설정해주세요!", ephemeral=True)
        view = TimeRangeView(user_id=self.user_id, day=day)
        print("View 상태:", view)

        await interaction.followup.send(f"{day} 시간 선택을 진행하세요.", view=view)

class TimeRangeView(View):
    def __init__(self,user_id,day):
        super().__init__(timeout=300)  # 5분 타임아웃
        self.user_id = user_id
        self.day = day
        self.start_time = None
        self.end_time = None

        # 시작 시간 선택
        start_options = [discord.SelectOption(label=f"{hour:02d}:00", value=f"{hour:02d}:00") for hour in range(0, 24)]
        print("시작 시간 옵션:", start_options)  # 디버깅 메시지
        self.add_item(discord.ui.Select(
            placeholder="시작 시간을 선택하세요",
            options=start_options,
            custom_id="start_time"
        ))

        # 종료 시간 선택
        end_options = [discord.SelectOption(label=f"{hour:02d}:00", value=f"{hour:02d}:00") for hour in range(0, 24)]
        print("종료 시간 옵션:", end_options)  # 디버깅 메시지
        self.add_item(discord.ui.Select(
            placeholder="종료 시간을 선택하세요",
            options=end_options,
            custom_id="end_time"
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("이 상호작용은 당신을 위한 것이 아닙니다!", ephemeral=True)
            return False
        return True

    @discord.ui.select(custom_id="start_time")
    async def select_start_time(self, interaction: discord.Interaction, select: Select):
        self.start_time = select.values[0]
        await interaction.response.send_message(f"시작 시간을 {self.start_time}로 설정했습니다.", ephemeral=True)

    @discord.ui.select(custom_id="end_time")
    async def select_end_time(self, interaction: discord.Interaction, select: Select):
        self.end_time = select.values[0]
        if self.start_time and self.end_time:
            await interaction.response.send_message(
                f"시간 범위가 {self.start_time}부터 {self.end_time}까지로 설정되었습니다!", ephemeral=True)
        else:
            await interaction.response.send_message("시간 범위를 완전히 선택해주세요!", ephemeral=True)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        # UI 비활성화 처리 후 업데이트
        if hasattr(self, 'message') and self.message:
            await self.message.edit(view=self)


bot.run(TOKEN)
