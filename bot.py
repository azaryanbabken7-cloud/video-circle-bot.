
import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import CommandStart
from aiogram.enums import ContentType

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN)
dp = Dispatcher()

# Пока временное хранение пользователей
users = set()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет! Я превращаю видео в кружочки!\n\n"
        "🎁 Первое видео бесплатно.\n"
        "⭐ Безлимитная подписка — 20 Stars."
    )

@dp.message(F.video)
async def video(message: Message):
    user_id = message.from_user.id

    if user_id not in users:
        users.add(user_id)
        await message.answer("🎁 Первое видео бесплатно! Обрабатываю...")
        await process_video(message)
    else:
        await message.answer_invoice(
            title="Безлимитная подписка",
            description="Безлимитное превращение видео в кружочки",
            payload="unlimited",
            currency="XTR",
            prices=[LabeledPrice(label="Безлимит", amount=20)]
        )

async def process_video(message: Message):
    await message.answer("⚙️ Обработка видео скоро будет подключена.")

@dp.pre_checkout_query()
async def checkout(query: PreCheckoutQuery):
    await query.answer(ok=True)

@dp.message(F.successful_payment)
async def payment(message: Message):
    await message.answer("⭐ Оплата получена! Безлимит активирован.")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

