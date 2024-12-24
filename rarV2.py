import asyncio
from .. import loader, utils

@loader.tds
class TypingEffectModeMod(loader.Module):
    """Модуль для постоянного эффекта печатания текста. Разработчик: @userbotlk"""

    strings = {"name": "TypingEffectMode"}

    def __init__(self):
        self.typing_mode = False  # Флаг для отслеживания режима печатания

    async def typecmd(self, message):
        """
         - Включает режим печатания
        """
        self.typing_mode = True
        premium_emoji = "<emoji document_id=5447644880824181073>⚠️</emoji>"
        await message.edit(f"{premium_emoji} <b>Режим печатания активирован!</b>")

    async def ntypecmd(self, message):
        """
         - Выключает режим печатания
        """
        self.typing_mode = False
        premium_emoji = "<emoji document_id=5447644880824181073>⚠️</emoji>"
        await message.edit(f"{premium_emoji} <b>Режим печатания отключен!</b>")

    async def watcher(self, message):
        # Проверяем, включен ли режим печатания и не является ли сообщение командой
        if self.typing_mode and not message.out:
            return  # Игнорируем входящие сообщения (чужие)
        
        if self.typing_mode and message.out and not message.text.startswith("."):
            # Текст для печатания
            text = message.text
            tbp = ""  # Временная переменная для накопления текста
            typing_symbol = "▒"  # Символ для имитации печатания

            try:
                for char in text:
                    tbp += char  # Добавляем символ
                    await message.edit(tbp + typing_symbol)  # Редактируем сообщение
                    await asyncio.sleep(0.05)  # Задержка между символами
                await message.edit(tbp)  # Окончательный результат без символа "▒"
            except Exception as e:
                premium_emoji = "<emoji document_id=5447644880824181073>⚠️</emoji>"
                await message.edit(f"{premium_emoji} <b>Ошибка:</b> {str(e)}")
