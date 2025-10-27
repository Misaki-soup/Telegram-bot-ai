import os 
from dotenv import load_dotenv
from groq import AsyncGroq
import asyncio

class AI_handler:
    def __init__(self,token):           
        self.client = AsyncGroq(api_key = token)

    async def generate(self,user_input):
        chat_completions = await self.client.chat.completions.create(
            messages = [
                {
                    'role':'user',
                    'content':user_input
                }
            ],
            model = 'groq/compound'
    )
        response = chat_completions.choices[0].message.content
        print(response)
        return response


if __name__ ==  '__main__':
    load_dotenv()
    token = os.getenv('GROQ_TOKEN')
    ai = AI_handler(token)
    asyncio.run(ai.generate(input('You: ')))
