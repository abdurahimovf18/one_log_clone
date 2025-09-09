
from aiogram import Bot
from aiogram.types import BotCommand as AiogramBotCommand
from aiogram.utils.i18n import I18n

from src.bot.utils.i18n import i18n
from src.config.enums import BotCommand
from src.config.settings import LANGUAGES, UserLanguage


async def setup_bot_commands(
        bot: Bot, 
        commands: list[BotCommand]
    ) -> None:
    """
    This command sets the BOT's commands
    """

    with i18n.context():
        _ = i18n.gettext

        for language in LANGUAGES:
            bot_commands = get_locale_commands(
                commands=commands, 
                language=language, 
                i18n=i18n
            )
            await bot.set_my_commands(
                commands=bot_commands,
                language_code=language.code.value.lower()
            )


def get_locale_commands(
    commands: list[BotCommand],
    language: UserLanguage,
    i18n: I18n
) -> list[AiogramBotCommand]:
    
    """
    This is a function which is used internally to setup bot commands.

    this function gets command, language, i18n objects and turns it into
    a bot command which can be registered to the bot with language code.
    """
    
    _ = i18n.gettext
    locale_commands: list[AiogramBotCommand] = []
            
    for command in commands:
        bot_command = AiogramBotCommand(
            command=command.command,
            description=_(
                str(command.description),
                locale=language.code.value
            )
        )
        locale_commands.append(
            bot_command
        )
    
    return locale_commands
            