from telethon import events
from .. import loader, utils

@loader.tds
class MaliStealMod(loader.Module):
    "MaliSteal - Сохраняет сообщения в Избранное."

    strings = {
        "name": "MaliSteal",
        "no_reply": "<b>Ответьте на сообщение для сохранения</b>",
        "success": ""  # Сообщение об успехе не отображается, т.к. команда удаляется.
    }

    async def stealcmd(self, message):
        "Используйте steal в ответ на сообщение, чтобы украсть его"
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings["no_reply"])
            return

        sender = await reply.get_sender()
        sender_name = utils.escape_html(getattr(sender, "first_name", "Неизвестно"))
        group_name = utils.escape_html(getattr(reply.chat, "title", "Личные сообщения"))

        # Формируем текст для отправки в Избранное
        text = (
            f"Сообщение от <b>{sender_name}</b> из группы <b>{group_name}</b>\n\n"
            f"<i>{utils.escape_html(reply.text)}</i>"
        )

        # Отправляем сообщение в Избранное
        await message.client.send_message("me", text)

        # Если в сообщении есть медиа/мультимедиа, отправляем его отдельно
        if reply.media:
            await message.client.send_file("me", reply.media)

        # Удаляем команду .steal
        await message.delete()
