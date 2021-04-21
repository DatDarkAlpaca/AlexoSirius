from discord.ext.commands import AutoShardedBot, DefaultHelpCommand, errors
from discord import Forbidden
from bot.permissions import *

import bot.traceback as trace


class Bot(AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Ready: {self.user} | Servers: {len(self.guilds)}")

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot or not permissions.can_send(msg):
            return

        await self.process_commands(msg)

    async def on_command_error(self, ctx, err):
        if isinstance(err, errors.MissingRequiredArgument) or isinstance(err, errors.BadArgument):
            helper = str(ctx.invoked_subcommand) if ctx.invoked_subcommand else str(ctx.command)
            await ctx.send_help(helper)

        # Command Invoke:
        elif isinstance(err, errors.CommandInvokeError):
            if '2000 or fewer' in str(err) and len(ctx.message.clean_content) > 1900:
                return await ctx.send(f"{ctx.message.author.mention}, \
                                      You\'ve tried to use a command that \
                                      sends more than 2000 characters.", delete_after=7)

            await ctx.send('I\'m sorry, but there was an error '
                           'while trying to execute the last command. The '
                           'host should be able to read it from the bot menu.', delete_after=10)

        # Command Failure:
        elif isinstance(err, errors.CheckFailure):
            pass

        # Command Limit:
        elif isinstance(err, errors.MaxConcurrencyReached):
            await ctx.send(f"{ctx.message.author.mention}, \
                           You've reached the limit of commands you can use at a time.",
                           delete_after=5)

        # Command Cooldown:
        elif isinstance(err, errors.CommandOnCooldown):
            await ctx.send(f"This command is in cooldown. You can try it again later after {round(err.retry_after, 2)}"
                           f" seconds, {ctx.message.author.mention}", delete_after=7)

        # Command Not Found:
        elif isinstance(err, errors.CommandNotFound):
            pass


class HelpFormat(DefaultHelpCommand):
    def get_destination(self, no_pm: bool = False):
        if no_pm:
            return self.context.channel
        else:
            return self.context.author

    async def send_error_message(self, error):
        destination = self.get_destination(no_pm=True)
        await destination.send(error)

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages(no_pm=True)

    async def send_pages(self, no_pm: bool = False):
        try:
            if permissions.can_react(self.context):
                await self.context.message.add_reaction(chr(0x2709))
        except Forbidden:
            pass

        try:
            destination = self.get_destination(no_pm=no_pm)
            for page in self.paginator.pages:
                await destination.send(page)
        except Forbidden:
            destination = self.get_destination(no_pm=True)
            await destination.send('Couldn\'t help you since you blocked DMs.')
