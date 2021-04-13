from discord import FFmpegPCMAudio, ClientException
from discord.ext import commands
from utils.config import config


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def play(ctx, sound_name):
        vc = ctx.voice_client

        if vc:
            try:
                vc.play(FFmpegPCMAudio(executable=config['ffmpeg'], source=config['sounds'] + sound_name))
            except ClientException:
                await ctx.send(f"{ctx.message.author.mention}, I'm already playing a song", delete_after=5)
        else:
            await ctx.send(f"{ctx.message.author.mention}, am I connected to any voice chat?", delete_after=5)

    @commands.command()
    async def scream(self, ctx):
        await Voice.play(ctx, 'scream.mp3')

    @commands.command()
    async def rawn(self, ctx):
        await Voice.play(ctx, 'rawn.mp3')


def setup(bot):
    bot.add_cog(Voice(bot))
