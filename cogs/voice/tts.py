from utils.safe_functions import safe_delete_message
from discord.ext import commands
from utils.config import config
from aiogtts import aiogTTS


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _talk(self, ctx, lang, tld, text):
        await safe_delete_message(ctx.message)

        aiogtts = aiogTTS()
        sound_name = 'text.mp3'

        try:
            if not text:
                await aiogtts.save(text='I have no idea what to talk', lang=lang, slow=False,
                                   filename=config['sounds'] + sound_name, tld=tld)
            else:
                await aiogtts.save(text=text, lang=lang, slow=False, filename=config['sounds'] + sound_name,
                                   tld=tld)
        except ValueError:
            await ctx.send(f"{ctx.message.author.mention}, something went wrong. Perhaps you've chosen a "
                           f"language that doesn't exist.?")
            return

        await self.bot.get_cog('Sounds').play(ctx, sound_name)

    @commands.command()
    @commands.has_role("Alexa")
    async def talk(self, ctx, *, text=None):
        await self._talk(ctx, lang='en', tld='com', text=text)

    @commands.command()
    @commands.has_role("Alexa")
    async def brit(self, ctx, *, text=None):
        await self._talk(ctx, lang='en', tld='co.uk', text=text)

    @commands.command()
    @commands.has_role("Alexa")
    async def talk_male(self, ctx, *, text=None):
        await self._talk(ctx, lang='en', tld='com', text=text)

    @commands.command()
    @commands.has_role("Alexa")
    async def falar(self, ctx, *, text=None):
        await self._talk(ctx, lang='pt', tld='com.br', text=text)

    @commands.command()
    @commands.has_role("Alexa")
    async def hanashi(self, ctx, *, text=None):
        await self._talk(ctx, lang='ja', tld='jp', text=text)

    @commands.command()
    @commands.has_role("Alexa")
    async def talk_accent(self, ctx, lang, tld, *, text=None):
        await self._talk(ctx, lang=lang, tld=tld, text=text)


def setup(bot):
    bot.add_cog(TTS(bot))
