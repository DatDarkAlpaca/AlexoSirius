from discord import FFmpegPCMAudio, ClientException
from discord.ext import commands

from utils.safe_functions import safe_delete_message
from utils.config import config


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def play(ctx, sound_name):
        await safe_delete_message(ctx.message)

        vc = ctx.voice_client

        if vc:
            try:
                vc.play(FFmpegPCMAudio(executable=config['ffmpeg'], source=config['sounds'] + sound_name,
                                       options="-loglevel panic"))
            except ClientException:
                await ctx.send(f"{ctx.message.author.mention}, I'm already playing a song", delete_after=5)
        else:
            await ctx.send(f"{ctx.message.author.mention}, am I connected to any voice chat?", delete_after=5)

    @commands.command()
    @commands.has_role("Alexa")
    async def scream(self, ctx):
        await Sounds.play(ctx, 'scream.mp3')

    @commands.command()
    @commands.has_role("Alexa")
    async def rawn(self, ctx):
        await Sounds.play(ctx, 'rawn.mp3')

    @commands.command()
    @commands.has_role("Alexa")
    async def mama(self, ctx):
        await Sounds.play(ctx, 'mama.mp3')


def setup(bot):
    bot.add_cog(Sounds(bot))
