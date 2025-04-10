import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime, timedelta

from database.raids import (
    insert_raid,
    get_latest_raid,
    get_raid_id_by_message_id,
    add_participant,
    remove_participant,
    get_raid_info_with_participants
)
from logic.scheduler_helper import schedule_raid_alarm


class RaidJoinView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="참가", style=discord.ButtonStyle.success, custom_id="raid_join")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        guild_id = str(interaction.guild.id)
        message_id = interaction.message.id

        raid_id = get_raid_id_by_message_id(message_id)
        if not raid_id:
            await interaction.response.send_message("❌ 레이드를 찾을 수 없습니다.", ephemeral=True)
            return

        try:
            add_participant(raid_id, user_id)
            await interaction.response.send_message("✅ 참가 완료!", ephemeral=True)
        except ValueError as e:
            await interaction.response.send_message(f"⚠️ {str(e)}", ephemeral=True)

        await update_raid_embed(interaction, raid_id)

    @discord.ui.button(label="취소", style=discord.ButtonStyle.danger, custom_id="raid_cancel")
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        message_id = interaction.message.id

        raid_id = get_raid_id_by_message_id(message_id)
        if not raid_id:
            await interaction.response.send_message("❌ 레이드를 찾을 수 없습니다.", ephemeral=True)
            return

        remove_participant(raid_id, user_id)
        await interaction.response.send_message("🗑️ 참가 취소했습니다.", ephemeral=True)

        await update_raid_embed(interaction, raid_id)


async def update_raid_embed(interaction: discord.Interaction, raid_id: int):
    title, time, participants = get_raid_info_with_participants(raid_id)
    embed = discord.Embed(
        title=f"🛡️ 레이드 모집 - {title}",
        description=f"⏰ 시작 시각: `{time.strftime('%H:%M')}`\n👉 참가를 원하시면 버튼을 눌러주세요!",
        color=discord.Color.blue()
    )
    embed.add_field(name="👥 참가자 수", value=f"{len(participants)}명", inline=True)

    if participants:
        name_list = []
        for user_id in participants:
            member = interaction.guild.get_member(int(user_id))
            name_list.append(f"- {member.display_name if member else user_id}")
        embed.add_field(name="📋 참가자 목록", value="\n".join(name_list), inline=False)
    else:
        embed.add_field(name="📋 참가자 목록", value="없음", inline=False)

    await interaction.message.edit(embed=embed, view=interaction.message.components[0])


class RaidSlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="레이드등록", description="레이드를 등록합니다.")
    @app_commands.describe(보스명="보스 이름", 시간="예: 21:30")
    async def 레이드등록(self, interaction: discord.Interaction, 보스명: str, 시간: str):
        try:
            hour, minute = map(int, 시간.split(":"))
            now = datetime.now()
            raid_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if raid_time < now:
                raid_time += timedelta(days=1)

            server_id = str(interaction.guild.id)
            creator_id = str(interaction.user.id)

            message_embed = discord.Embed(
                title=f"🛡️ 레이드 모집 - {보스명}",
                description=f"⏰ 시작 시각: `{raid_time.strftime('%H:%M')}`\n👉 참가를 원하시면 버튼을 눌러주세요!",
                color=discord.Color.blue()
            )

            view = RaidJoinView()
            await interaction.response.send_message(embed=message_embed, view=view)
            sent_msg = await interaction.original_response()

            insert_raid(server_id, 보스명, creator_id, raid_time, sent_msg.id)
            raid_id = get_latest_raid(server_id)

            alarm_time = raid_time - timedelta(minutes=10)
            schedule_raid_alarm(self.bot.scheduler, alarm_time, server_id, raid_id, 보스명, raid_time)

        except Exception as e:
            await interaction.response.send_message(f"❌ 오류 발생: {str(e)}", ephemeral=True)


async def setup(bot):
    await bot.add_cog(RaidSlashCog(bot))
