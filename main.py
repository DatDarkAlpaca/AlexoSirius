from bot.extensions import load_extensions, display_header
from bot import Bot, HelpFormat, config


bot = Bot(command_prefix=config['prefix'], command_attrs=dict(hidden=True), help_command=HelpFormat())

# Header:
display_header()

# Loading:
load_extensions(bot)


try:
    bot.run(config['token'])
except Exception as e:
    print('[Error]: Failed to log-in', e)
