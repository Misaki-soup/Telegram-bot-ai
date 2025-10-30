import asyncio
from telebot.async_telebot import AsyncTeleBot
from ai_body import AI_handler 
from dotenv import load_dotenv
import os
import sys

load_dotenv() 
bot = AsyncTeleBot(os.getenv('DEV_TOKEN')) #замінити назад на оригінал
ai = AI_handler()
    

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    text = """🎉 Вітаю!

Я твій AI-друг, готовий допомагати, спілкуватися та відповідати на різноманітні питання!

Уяви мене як кишенькову енциклопедію (поки що без доступу до інтернету 😅). Я можу:
💡 Пояснювати складні теми
✍️ Допомагати з написанням текстів
🤔 Генерувати ідеї
💬 Просто поговорити!

📝 Я постійно вдосконалюю свою українську! Якщо помітиш помилку - обов'язково скажи, і я стану краще. Твоя допомога робить мене кориснішим для всіх! 🙏

Що тебе цікавить?"""
    await bot.reply_to(message, text)

@bot.message_handler(commands=['kill'])
async def stop_bot(message):
    if message.chat.id == 536130090:
        await bot.send_message(chat_id=536130090, text='Бот зупинено')
        await sys.exit('Stopped from telegram')
    else:
        await bot.reply_to(message,'Did you try to kill me? 0_o')



@bot.message_handler(func=lambda message: True)
async def answer(message):
    response = await ai.generate(message.text,message.chat.id)
    await bot.reply_to(message, response)


async def main():
    await bot.send_message(chat_id=536130090, text='Бот запущено')
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(main())