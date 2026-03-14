import discord
from discord.ext import commands, tasks


_COGS = [
    "modules.admin",
    "modules.commands"
]


def closeness(search_term: str, match: str) -> int:
    return 2 if match.startswith(search_term) else 1 if search_term in match else 0


class PinCache:
    def __init__(self, messages: list[str]):
        self.messages = messages

    @staticmethod
    async def from_channel(channel: discord.TextChannel):
        return PinCache(
            [message.content[:100] async for message in channel.pins(limit=None) if message.content]
        )


async def get_pin_cache(channel: discord.TextChannel) -> PinCache:
    if channel.id not in pin_cache:
        pin_cache[channel.id] = await PinCache.from_channel(channel)
    return pin_cache[channel.id]


pin_cache: dict[int, PinCache] = {}


class Bot(commands.Bot):  # main bot class
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            intents=intents, command_prefix="ps!",
            allowed_contexts=discord.app_commands.AppCommandContext(guild=True, dm_channel=True, private_channel=True),
            allowed_installs=discord.app_commands.AppInstallationType(guild=True, user=True)
        )

    async def setup_hook(self) -> None:
        for extension in _COGS:
            await self.load_extension(extension)
        self.clear_cache.start()

    @tasks.loop(minutes=10)
    async def clear_cache(self):
        pin_cache.clear()
