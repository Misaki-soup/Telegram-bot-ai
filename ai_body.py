import os 
from dotenv import load_dotenv
from groq import AsyncGroq
import asyncio


class AI_handler:
    def __init__(self,token):           
        self.client = AsyncGroq(api_key = token)
        self.temp_memory = {}

    async def generate(self,user_input,user_id):
        if user_id not in self.temp_memory:
            self.temp_memory[user_id] = [{
                'role': 'system',
                'content': 'You are telegram bot. So you have to do text formats for telegram, if needed. also your answers cannot exceed telegram message limits'
            }]

        self.temp_memory[user_id].append({
            'role':'user',
            'content':user_input
        })
        chat_completions = await self.client.chat.completions.create(
            messages = self.temp_memory[user_id],
            model = 'qwen/qwen3-32b',
            reasoning_format='hidden' 
    )
        response = chat_completions.choices[0].message.content
        #print(response)
        self.temp_memory[user_id].append({
            'role':'assistant',
            'content':response
        })
        return response


if __name__ ==  '__main__':
    load_dotenv()
    token = os.getenv('GROQ_TOKEN')
    ai = AI_handler(token)
    asyncio.run(ai.generate(input('You: ')))
