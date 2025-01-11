from telethon import events
from .. import loader, utils
import asyncio


@loader.tds
class YaAdminMod(loader.Module):
    """YaAdmin: бан, кик, мут, варн и т.д."""

    strings = {
        "name": "YaAdmin",
        "muted": "✔️ Пользователь {user} успешно замучен на {time} минут(ы) по причине: {reason}",
        "unmuted": "✔️ Мут для пользователя {user} снят.",
        "warned": "✔️ Пользователь {user} успешно получил предупреждение на {time} дней по причине: {reason}",
        "warn_removed": "✔️ С пользователя {user} успешно сняты предупреждения: {warns}",
        "banned": "🚫 Пользователь {user} забанен за превышение лимита варнов.",
    }

    def __init__(self):
        self.warns = {}  # Хранение данных о варнах

    async def mutecmd(self, message):
        """Мутит пользователя: .mute <реплай/username/id> <время (минуты)> <причина>"""
        args = utils.get_args_raw(message).split()
        reply = await message.get_reply_message()
        
        if not args and not reply:
            await message.edit("❌ Укажите пользователя, время и причину.")
            return

        # Получаем пользователя
        user = await self._get_user(message, reply, args[0] if args else None)
        if not user:
            await message.edit("❌ Не удалось найти пользователя.")
            return

        # Получаем время мута
        try:
            time = int(args[1]) if len(args) > 1 else 10  # По умолчанию: 10 минут
        except ValueError:
            await message.edit("❌ Укажите корректное время (в минутах).")
            return

        # Получаем причину
        reason = " ".join(args[2:]) if len(args) > 2 else "Не указана"

        # Устанавливаем мут
        await message.client.edit_permissions(
            message.chat_id, 
            user.id, 
            send_messages=False  # Запрещаем отправлять сообщения
        )
        await message.edit(self.strings("muted").format(user=user.first_name, time=time, reason=reason))

        # Ждём указанный срок, затем снимаем мут
        await asyncio.sleep(time * 60)  # Перевод минут в секунды
        await message.client.edit_permissions(
            message.chat_id, 
            user.id, 
            send_messages=True  # Снимаем запрет на отправку сообщений
        )
        await message.client.send_message(
            message.chat_id, 
            f"✔️ Мут для пользователя {user.first_name} завершён."
        )

    async def unmutecmd(self, message):
        """Снимает мут: .unmute <реплай/username/id>"""
        args = utils.get_args_raw(message).split()
        reply = await message.get_reply_message()
        
        if not args and not reply:
            await message.edit("❌ Укажите пользователя для размутки.")
            return

        # Получаем пользователя
        user = await self._get_user(message, reply, args[0] if args else None)
        if not user:
            await message.edit("❌ Не удалось найти пользователя.")
            return

        # Убираем мут
        await message.client.edit_permissions(
            message.chat_id, 
            user.id, 
            send_messages=True
        )
        await message.edit(self.strings("unmuted").format(user=user.first_name))

    async def warncmd(self, message):
        """Выдаёт варн: .warn <реплай/username/id> <срок (дни)> <причина>"""
        args = utils.get_args_raw(message).split()
        reply = await message.get_reply_message()
        
        if not args and not reply:
            await message.edit("❌ Укажите пользователя, срок и причину варна.")
            return

        # Получаем пользователя
        user = await self._get_user(message, reply, args[0] if args else None)
        if not user:
            await message.edit("❌ Не удалось найти пользователя.")
            return

        # Получаем срок варна
        try:
            time = int(args[1]) if len(args) > 1 else 7  # По умолчанию: 7 дней
        except ValueError:
            await message.edit("❌ Укажите корректное время (в днях).")
            return

        # Получаем причину
        reason = " ".join(args[2:]) if len(args) > 2 else "Не указана"

        # Добавляем варн
        self.warns[user.id] = self.warns.get(user.id, 0) + 1

        # Проверяем лимит варнов
        if self.warns[user.id] >= 3:  # Лимит варнов = 3
            await message.client.edit_permissions(message.chat_id, user.id, view_messages=False)
            await message.edit(self.strings("banned").format(user=user.first_name))
            self.warns[user.id] = 0  # Сбрасываем варны
        else:
            await message.edit(self.strings("warned").format(user=user.first_name, time=time, reason=reason))
            await asyncio.sleep(time * 86400)  # Перевод дней в секунды
            self.warns[user.id] -= 1
            await message.client.send_message(
                message.chat_id, 
                f"✔️ Варн для пользователя {user.first_name} истёк."
            )

    async def _get_user(self, message, reply, arg):
        """Получает объект пользователя"""
        try:
            if reply:
                return await message.client.get_entity(reply.sender_id)
            if arg:
                return await message.client.get_entity(arg)
        except Exception:
            return None
