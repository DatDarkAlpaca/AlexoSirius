from utils.safe_functions import safe_delete_message
from discord.ext import commands
from datetime import datetime


class Timer(commands.Cog):
    def __init__(self, bot):
        self.current_timers = []
        self.bot = bot

    # Timer:
    async def _exists_timer(self, ctx):
        for timer in self.current_timers:
            if int(timer[0]) == int(ctx.message.guild.id):
                return True
        return False

    async def _insert_timer(self, ctx):
        mention = ctx.message.author.mention
        gid = ctx.message.guild.id

        if not await self._exists_timer(ctx):
            self.current_timers.append((gid, datetime.now()))
        else:
            return

    async def _delete_timer(self, ctx):
        gid = ctx.message.guild.id
        deleted = False

        for timer in self.current_timers:
            index = 0
            if int(timer[0]) == int(gid):
                self.current_timers.pop(index)
                deleted = True
            index += 1

        mention = ctx.message.author.mention
        if not deleted:
            return

    async def _get_timer(self, ctx):
        gid = ctx.message.guild.id

        for timer in self.current_timers:
            if int(timer[0]) == int(gid):
                return timer
        return None

    # Functions:
    async def start(self, ctx):
        if not ctx.message.guild.id == 528000032356565032:
            return

        await safe_delete_message(ctx.message)
        await self._insert_timer(ctx)

    async def stop(self, ctx):
        if not ctx.message.guild.id == 528000032356565032:
            return

        await safe_delete_message(ctx.message)

        timer = await self._get_timer(ctx)

        if timer:
            _, time = timer
            if time:
                await self._delete_timer(ctx)
                return datetime.now() - time


def setup(bot):
    bot.add_cog(Timer(bot))
