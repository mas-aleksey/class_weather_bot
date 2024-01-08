import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.weather import Weather


class BotConfig(BaseSettings):
    token: str
    
    class Config:
        env_file = '.env'
        env_prefix = 'BOT_'


class WeatherBot:
    
    def __init__(self, config: BotConfig):
        self.config = config
        self.weather = Weather()
        self.dp = Dispatcher()
        self.bot = Bot(config.token, parse_mode=ParseMode.HTML)
        self.register_handlers()

    def register_handlers(self):
        self.dp.message.register(self.start_handler, CommandStart())
        self.dp.message.register(self.message_handler)
        
    async def message_handler(self, message: types.Message):
        try:
            text = await self.weather.get_weather(message.text)
            await message.answer(text)
        except Exception:
            await message.answer("Error")
    
    async def start_handler(self, message: types.Message):
        await message.answer(f"Hello 👋, Mr. {hbold(message.from_user.full_name)}!")
    
    async def start(self):
        await self.dp.start_polling(self.bot)


async def main():
    load_dotenv()
    config = BotConfig()
    bot = WeatherBot(config)
    await bot.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
