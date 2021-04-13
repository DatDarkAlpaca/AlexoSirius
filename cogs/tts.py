from discord.ext import commands
from utils.config import config
from aiogtts import aiogTTS


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Alexa")
    async def talk(self, ctx, *, text=None):
        aiogtts = aiogTTS()
        sound_name = 'text.mp3'

        if not text:
            await aiogtts.save(text='I have no idea what to talk', lang='en', slow=False,
                               filename=config['sounds'] + sound_name)
        else:
            await aiogtts.save(text=text, lang='en', slow=False, filename=config['sounds'] + sound_name)

        await self.bot.get_cog('Voice').play(ctx, sound_name)

    @commands.command()
    @commands.has_role("Alexa")
    async def falar(self, ctx, *, text=None):
        aiogtts = aiogTTS()
        sound_name = 'text.mp3'

        if not text:
            await aiogtts.save(text='I have no idea what to talk', lang='pt', tld='com.br', slow=False,
                               filename=config['sounds'] + sound_name)
        else:
            await aiogtts.save(text=text, lang='pt', tld='com.br', slow=False,
                               filename=config['sounds'] + sound_name)

        await self.bot.get_cog('Voice').play(ctx, sound_name)

    @commands.command()
    @commands.has_role("Alexa")
    async def talk_accent(self, ctx, lang, tld, *, text=None):
        aiogtts = aiogTTS()
        sound_name = 'text.mp3'

        if not text:
            await aiogtts.save(text='I have no idea what to talk', lang=lang, tld=tld, slow=False,
                               filename=config['sounds'] + sound_name)
        else:
            await aiogtts.save(text=text, lang=lang, tld=tld, slow=False, filename=config['sounds'] + sound_name)

        await self.bot.get_cog('Voice').play(ctx, sound_name)


def setup(bot):
    bot.add_cog(TTS(bot))
