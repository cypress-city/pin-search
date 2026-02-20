import asyncio
import discord
from discord.ext import commands

from modules.core import Bot, closeness


async def search(inter: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
    matches = sorted(
        list({message.content async for message in inter.channel.pins(limit=None)
              if closeness(current.lower(), message.content.lower())}),
        key=lambda c: -closeness(current.lower(), c.lower())
    )
    return [discord.app_commands.Choice(name=g, value=g) for g in matches][:25]


class PinsCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @discord.app_commands.command(
        name="pins",
        description="Search this channel's pinned messages."
    )
    @discord.app_commands.autocomplete(
        query=search
    )
    @discord.app_commands.describe(
        query="Search term"
    )
    async def search_command(self, inter: discord.Interaction, query: str):
        if matches := [message async for message in inter.channel.pins(limit=None) if message.content == query]:
            most_recent = sorted(matches, key=lambda m: m.created_at)[-1]
            response = await inter.response.send_message(f"Retrieved message: {most_recent.jump_url}")
            try:
                await most_recent.forward(inter.channel)
            except discord.HTTPException:
                pass
            else:
                await asyncio.sleep(10)
                await response.resource.delete()
        else:
            return await inter.response.send_message(
                "⚠️ Something went wrong, and the message could not be forwarded.", ephemeral=True
            )


async def setup(bot: Bot):
    await bot.add_cog(PinsCog(bot))
