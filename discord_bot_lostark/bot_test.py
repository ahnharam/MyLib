import discord
from discord.ext import commands
from discord.ui import View, Button
from config import DISCORD_TOKEN

TOKEN = DISCORD_TOKEN

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

class TestView(View):
    def __init__(self):
        super().__init__(timeout=None)
        print("✅ View 등록됨")

    @discord.ui.button(label="테스트 버튼", style=discord.ButtonStyle.green, custom_id="test_button")
    async def click(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("✅ 버튼 눌림!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"✅ 봇 로그인 성공: {bot.user}")
    bot.add_view(TestView())
    synced = await bot.tree.sync()
    print(f"🌿 슬래시 명령어 등록: {len(synced)}개")

@bot.tree.command(name="버튼테스트2", description="버튼 동작 확인")  # ← 여기 이름 바꿈
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("🔘 눌러봐!", view=TestView())

bot.run(TOKEN)
