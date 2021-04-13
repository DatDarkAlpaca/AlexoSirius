from discord.ext import commands
from utils.config import config
from gtts import gTTS


class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def talk(self, ctx, *, text=None):
        if not text:
            speech = gTTS(text='I have no idea what to talk', lang='en', slow=False)
        else:
            speech = gTTS(text=text, lang='en', slow=False)

        sound_name = 'text.mp3'

        speech.save(config['sounds'] + sound_name)

        await self.bot.get_cog('Voice').play(ctx, sound_name)

    @commands.command()
    async def falar(self, ctx, *, text=None):
        if not text:
            speech = gTTS(text='Eu não sei o que falar', lang='pt', tld='com.br', slow=False)
        else:
            speech = gTTS(text=text, lang='pt', tld='com.br', slow=False)

        sound_name = 'text.mp3'

        speech.save(config['sounds'] + sound_name)

        await self.bot.get_cog('Voice').play(ctx, sound_name)

    @commands.command()
    async def talk_accent(self, ctx, lang, tld, *, text=None):
        lang = str(lang).lower()
        tld = str(tld).lower()

        try:
            if not text:
                speech = gTTS(text='AA', lang=lang, tld=tld, slow=False)
            else:
                speech = gTTS(text=text, lang=lang, tld=tld, slow=False)

            sound_name = 'text.mp3'

            speech.save(config['sounds'] + sound_name)

            await self.bot.get_cog('Voice').play(ctx, sound_name)

        except Exception as e:
            await ctx.send(f"{ctx.message.author.mention}, sorry but something went wrong.")


def setup(bot):
    bot.add_cog(TTS(bot))
