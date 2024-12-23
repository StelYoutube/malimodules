from hikka import loader
import asyncio

@loader.tds
class AlwaysOnlineMod(loader.Module):
    """Модуль для поддержания бота всегда онлайн"""
    strings = {"name": "AlwaysOnline"}

    def __init__(self):
        self.running = False  # Флаг для управления процессом

    async def online_cmd(self, message):
        """
        Запустить или остановить поддержание онлайн статуса.
        Используй .online для включения/выключения.
        """
        if self.running:
            self.running = False
            await message.edit("<b>Статус 'онлайн' отключён 🛑</b>")
        else:
            self.running = True
            await message.edit("<b>Статус 'онлайн' активирован ✅</b>")
            await self._keep_online(message)

    async def _keep_online(self, message):
        """Процесс поддержания бота в сети."""
        while self.running:
            try:
                # Отправляем "ping" в Saved Messages
                await message.client.send_message("me", "ping")
                await asyncio.sleep(60)  # Интервал: 60 секунд
            except Exception as e:
                self.running = False
                await message.client.send_message(
                    "me", f"<b>Процесс остановлен из-за ошибки:</b> {e}"
                )
                break