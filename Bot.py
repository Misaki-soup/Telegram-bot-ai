import asyncio
from telebot.async_telebot import AsyncTeleBot
from ai_body import AI_handler 
from dotenv import load_dotenv
import os

async def main():
    load_dotenv()
    bot = AsyncTeleBot(os.getenv('TG_TOKEN'))
    ai = AI_handler(os.getenv('GROQ_TOKEN'))
