import asyncio
from .. import loader, utils

@loader.tds
class SpamMod(loader.Module):
    """Модуль для спама сообщений. Разработчик: @userbotlk"""

    strings = {"name": "Spam"}

    async def spamcmd(self, message):
        """
        .spam <кол-во сообщений> <задержка в секундах> <текст> - Спам сообщениями
        """
        args = utils.get_args_raw(message)
        if not args:
            await message.edit("<b>Использование: .spam <кол-во> <задержка> <текст></b>")
            return

        try:
            count, delay, text = args.split(" ", maxsplit=2)
            count = int(count)
            delay = float(delay)
        except ValueError:
            await message.edit("<b>Некорректные аргументы. Используйте: .spam <кол-во> <задержка> <текст></b>")
            return

        if count <= 0 or delay < 0:
            await message.edit("<b>Количество сообщений и задержка должны быть больше нуля.</b>")
            return

        await message.delete()  # Удаляем команду

        for _ in range(count):
            await message.client.send_message(message.chat_id, text)
            await asyncio.sleep(delay)