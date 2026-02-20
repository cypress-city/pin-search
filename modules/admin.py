from discord.ext import commands

from modules.core import Bot


class AdminCog(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="close", aliases=["stop"], hidden=True)
    async def close_command(self, ctx: commands.Context):
        if ctx.author == self.bot.application.owner:
            await ctx.send("😴 Stopping bot.")
            await self.bot.close()

    @commands.command(name="ping")
    async def ping_command(self, ctx: commands.Context):
        message = await ctx.send("🏓 Discord latency: ...")
        discord_latency = round((message.created_at - ctx.message.created_at).total_seconds() * 1000)
        await message.edit(content=f"🏓 Discord latency: {discord_latency} ms")

    @commands.command(name="sync", hidden=True)
    async def sync_command(self, ctx: commands.Context):
        if ctx.author == self.bot.application.owner:
            await self.bot.tree.sync()
            return await ctx.send("✅ Command tree re-synced.")


async def setup(bot: Bot):
    await bot.add_cog(AdminCog(bot))
