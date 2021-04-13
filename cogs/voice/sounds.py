from discord import FFmpegPCMAudio, ClientException, Embed
from discord.ext import commands

from utils.safe_functions import safe_delete_message
from utils.config import config

from os.path import isfile, join
from os import listdir


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

    @commands.command()
    @commands.has_role("Alexa")
    async def sound(self, ctx, sound_name: str):
        sound_name = str(sound_name).lower()

        audio_files = Sounds._get_audio_files()

        if sound_name in audio_files:
            await Sounds.play(ctx, f"{sound_name}.mp3")
        else:
            await ctx.send(f"{ctx.message.author.mention}, this audio does not exist!")

    @commands.command()
    @commands.has_role("Alexa")
    async def sound_list(self, ctx):
        audio_files = Sounds._get_audio_files()

        embed = Embed(title="Sound List", color=0x3dc5ff,
                      description="The available sounds for this bot. To use them, type: **=sound name**.")

        embed.set_author(name="Sound", icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        for audio_name in audio_files:
            embed.add_field(name=f":musical_note: {audio_name.title().replace('_', '')}:",
                            value=audio_name, inline=True)

        embed.set_footer(text="Have a nice day, people! And remember to brush your teeth.")
        await ctx.send(embed=embed)

    @staticmethod
    def _get_audio_files():
        return [f[:-4] for f in listdir(config['sounds']) if isfile(join(config['sounds'], f))]


def setup(bot):
    bot.add_cog(Sounds(bot))
