import discord
from discord.ext import commands


_COGS = [
    "modules.admin",
    "modules.commands"
]


def closeness(search_term: str, match: str) -> int:
    return 2 if match.startswith(search_term) else 1 if search_term in match else 0


class Bot(commands.Bot):  # main bot class
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            intents=intents, command_prefix="!",
            allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
            allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=True)
        )

    async def setup_hook(self) -> None:
        for extension in _COGS:
            await self.load_extension(extension)
