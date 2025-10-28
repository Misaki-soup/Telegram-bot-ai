import asyncio
from telebot.async_telebot import AsyncTeleBot
from ai_body import AI_handler 
from dotenv import load_dotenv
import os

load_dotenv()
bot = AsyncTeleBot(os.getenv('TG_TOKEN'))
ai = AI_handler(os.getenv('GROQ_TOKEN'))
    

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Hi, I am AiBot.\n'
    await bot.reply_to(message, text)

@bot.message_handler(commands=['kill'])
async def stop_bot(message):
    await bot.send_message(chat_id=536130090, text='Бот зупинено')
    await bot.close_session()

@bot.message_handler(func=lambda message: True)
async def answer(message):
    response = await ai.generate(message.text,message.chat.id)
    await bot.reply_to(message, response)


async def main():
    await bot.send_message(chat_id=536130090, text='Бот запущено')
    await bot.polling()

if __name__ == '__main__':
    asyncio.run(main())