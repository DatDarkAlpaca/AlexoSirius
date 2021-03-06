from utils.safe_functions import safe_delete_message
from discord.ext import commands


class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def nuke(self, ctx, amount: int = 20):
        await safe_delete_message(ctx.message)
        await ctx.message.channel.purge(limit=amount)

    @commands.command(hidden=True, name='reload')
    @commands.is_owner()
    async def _reload_cog(self, ctx, *, cog_path: str):
        await safe_delete_message(ctx.message)

        mention = ctx.message.author.mention
        cog_path = 'cogs.' + cog_path.lower()

        try:
            self.bot.unload_extension(cog_path)
            self.bot.load_extension(cog_path)
            await ctx.send(f"{mention}, {cog_path} reloaded")
        except Exception:
            await ctx.send(f"{mention}, {cog_path} couldn't be reloaded.")

    @commands.command(hidden=True, name='load')
    @commands.is_owner()
    async def _load_cog(self, ctx, *, cog_path: str):
        await safe_delete_message(ctx.message)

        mention = ctx.message.author.mention
        cog_path = 'cogs.' + cog_path.lower()

        try:
            self.bot.load_extension(cog_path)
            await ctx.send(f"{mention}, {cog_path} loaded")
        except Exception:
            await ctx.send(f"{mention}, {cog_path} couldn't be loaded.")

    @commands.command(hidden=True, name='unload')
    @commands.is_owner()
    async def _unload_cog(self, ctx, *, cog_path: str):
        await safe_delete_message(ctx.message)

        mention = ctx.message.author.mention
        cog_path = 'cogs.' + cog_path.lower()

        try:
            self.bot.load_extension(cog_path)
            await ctx.send(f"{mention}, {cog_path} unloaded")
        except Exception:
            await ctx.send(f"{mention}, {cog_path} couldn't be unloaded.")


def setup(bot):
    bot.add_cog(AdminCommands(bot))
