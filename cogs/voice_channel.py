from utils.safe_functions import safe_delete_message, safe_disconnect
from discord.ext import commands


def convert_time(time):
    s = time.total_seconds()

    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)

    return '**{:02}h{:02}min{:02}s**'.format(int(hours), int(minutes), int(seconds))


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join')
    async def _join(self, ctx):
        channel = ctx.author.voice.channel

        await safe_delete_message(ctx.message)

        await ctx.guild.change_voice_state(channel=channel, self_deaf=True)

        await self.bot.get_cog('Timer').start(ctx)

        await channel.connect()

    @commands.command(name='leave')
    async def _leave(self, ctx):
        mention = ctx.message.author.mention

        await safe_delete_message(ctx.message)
        await safe_disconnect(ctx)

        # Stop the timer:
        time = await self.bot.get_cog('Timer').stop(ctx)

        # Sends a message:
        if time:
            await ctx.send(f"{mention}, I've been in this call for {convert_time(time)}")


def setup(bot):
    bot.add_cog(Voice(bot))
