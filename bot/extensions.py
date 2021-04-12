from fnmatch import fnmatch
from os import walk


def load_extensions(bot):
    print('-=-=-= Alexo | v0.1a =-=-=-')
    file_pattern, exclude = '*.py', '_'
    any_cogs = False
    for path, subdirectories, files in walk('./cogs'):
        for cog in files:
            if cog.startswith(exclude):
                continue
            if fnmatch(cog, file_pattern):
                cog_path = path.replace('\\', '.').replace('./', '') + '.' + cog[:-3]
                try:
                    bot.load_extension(cog_path)
                    print(f"• {cog[:-3]} has been loaded.")
                    any_cogs = True
                except Exception as e:
                    print(f"• {cog[:-3]} couldn't be loaded. {e}")

    if not any_cogs:
        print('🤎 - Not cogs were detected.')
