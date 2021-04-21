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

    @commands.command(name='leave')
    @commands.has_role("Alexa")
    async def leave(self, ctx):
        await safe_delete_message(ctx.message)
        await safe_disconnect(ctx)


def setup(bot):
    bot.add_cog(VoiceChannel(bot))
