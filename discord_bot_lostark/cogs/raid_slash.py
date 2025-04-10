import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from datetime import datetime, timedelta

from database.raids import (
    insert_raid,
    get_latest_raid,
    get_raid_id_by_message_id,
    get_raid_list,
    get_raid_info_with_participants,
    delete_raid,
    update_raid_time,
)
from logic.scheduler_helper import schedule_raid_alarm, generate_full_raid_list_embed


class RaidJoinView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="참가", style=discord.ButtonStyle.success, custom_id="raid_join")
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from database.raids import add_participant

        user_id = str(interaction.user.id)
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
        from database.raids import remove_participant

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
    @app_commands.describe(boss_name="보스 이름", time="예: 21:30")
    async def 레이드등록(self, interaction: discord.Interaction, boss_name: str, time: str):
        try:
            hour, minute = map(int, time.split(":"))
            now = datetime.now()
            raid_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if raid_time < now:
                raid_time += timedelta(days=1)

            server_id = str(interaction.guild.id)
            creator_id = str(interaction.user.id)

            embed = discord.Embed(
                title=f"🛡️ 레이드 모집 - {boss_name}",
                description=f"⏰ 시작 시각: `{raid_time.strftime('%H:%M')}`\n👉 참가를 원하시면 버튼을 눌러주세요!",
                color=discord.Color.blue()
            )
            view = RaidJoinView()
            await interaction.response.send_message(embed=embed, view=view)
            sent_msg = await interaction.original_response()

            insert_raid(server_id, boss_name, creator_id, raid_time, sent_msg.id)
            raid_id = get_latest_raid(server_id)

            alarm_time = raid_time - timedelta(minutes=10)
            schedule_raid_alarm(self.bot.scheduler, alarm_time, server_id, raid_id, boss_name, raid_time)

        except Exception as e:
            await interaction.response.send_message(f"❌ 오류 발생: {str(e)}", ephemeral=True)

    @app_commands.command(name="목록", description="오늘 등록된 레이드 목록을 확인합니다.")
    async def 목록(self, interaction: discord.Interaction):
        now = datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        server_id = str(interaction.guild.id)
        raids = get_raid_list(server_id, start, end)

        embed = discord.Embed(
            title="📋 오늘의 레이드 목록",
            description="레이드 ID를 통해 `/레이드삭제`, `/레이드수정`, `/상세` 명령어에 사용할 수 있어요.",
            color=discord.Color.green()
        )

        if not raids:
            embed.add_field(name="레이드 없음", value="오늘 등록된 레이드가 없습니다.", inline=False)
        else:
            for raid in raids:
                raid_id, title, time = raid
                embed.add_field(
                    name=f"[{raid_id}] {title}",
                    value=f"⏰ {time.strftime('%H:%M')}",
                    inline=False
                )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="레이드삭제", description="해당 ID의 레이드를 삭제합니다.")
    @app_commands.describe(raid_id="삭제할 레이드의 ID")
    async def 레이드삭제(self, interaction: discord.Interaction, raid_id: int):
        try:
            delete_raid(raid_id)
            await interaction.response.send_message(f"🗑️ 레이드(ID: {raid_id})가 삭제되었습니다.")
        except Exception as e:
            await interaction.response.send_message(f"❌ 삭제 실패: {str(e)}", ephemeral=True)

    @app_commands.command(name="레이드수정", description="레이드 시간을 수정합니다.")
    @app_commands.describe(raid_id="대상 ID", new_time="새로운 시간 (예: 21:00)")
    async def 레이드수정(self, interaction: discord.Interaction, raid_id: int, new_time: str):
        try:
            hour, minute = map(int, new_time.split(":"))
            new_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            update_raid_time(raid_id, new_time)
            await interaction.response.send_message(f"✏️ 레이드(ID: {raid_id}) 시간이 `{new_time}`으로 수정되었습니다.")
        except Exception as e:
            await interaction.response.send_message(f"❌ 수정 실패: {str(e)}", ephemeral=True)

    @app_commands.command(name="상세", description="레이드 참가자 상세 목록을 확인합니다.")
    @app_commands.describe(raid_id="확인할 레이드의 ID")
    async def 상세(self, interaction: discord.Interaction, raid_id: int):
        try:
            title, time, participants = get_raid_info_with_participants(raid_id)
            embed = discord.Embed(
                title=f"📋 레이드 상세 - {title}",
                description=f"⏰ 시작 시각: `{time.strftime('%H:%M')}`",
                color=discord.Color.purple()
            )
            if participants:
                embed.add_field(
                    name="👥 참가자 목록",
                    value="\n".join([f"- <@{user_id}>" for user_id in participants]),
                    inline=False
                )
            else:
                embed.add_field(name="👥 참가자 목록", value="없음", inline=False)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            await interaction.response.send_message(f"❌ 상세 정보 조회 실패: {str(e)}", ephemeral=True)

    @app_commands.command(name="전체목록", description="예정된 모든 레이드 목록을 확인합니다.")
    async def 전체목록(self, interaction: discord.Interaction):
        embed = await generate_full_raid_list_embed(str(interaction.guild.id))
        await interaction.response.send_message(embed=embed)



async def setup(bot):
    await bot.add_cog(RaidSlashCog(bot))
