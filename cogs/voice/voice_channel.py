from utils.safe_functions import safe_delete_message, safe_disconnect
from discord.ext import commands


def convert_time(time):
    s = time.total_seconds()

    hours, remainder = divmod(s, 3600)
    minutes, seconds = divmod(remainder, 60)

    return '**{:02}h{:02}min{:02}s**'.format(int(hours), int(minutes), int(seconds))


class VoiceChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def _leave(ctx):
        await safe_disconnect(ctx)

    @commands.command(name='join')
    @commands.has_role("Alexa")
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel

        await safe_delete_message(ctx.message)

        # Failsafe:
        if ctx.author.voice is None or ctx.author.voice.channel is None:
            await ctx.send(f"{ctx.message.author.mention}, you're not connected to any channel.",
                           delete_after=5)
            return

        # Connect:
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

        # Deafen:
        await ctx.guild.change_voice_state(channel=voice_channel, self_deaf=True)

        # Start Timer:
        if ctx.message.guild.id == 528000032356565032:
            await self.bot.get_cog('Timer').start(ctx)

    @commands.command(name='leave')
    @commands.has_role("Alexa")
    async def leave(self, ctx):
        mention = ctx.message.author.mention

        await safe_delete_message(ctx.message)
        await VoiceChannel._leave(ctx)

        # Stop the timer:
        time = await self.bot.get_cog('Timer').stop(ctx)

        # Sends a message:
        if time and ctx.message.guild.id == 528000032356565032:
            await ctx.send(f"{mention}, I've been in this call for {convert_time(time)}",
                           delete_after=10)


def setup(bot):
    bot.add_cog(VoiceChannel(bot))
