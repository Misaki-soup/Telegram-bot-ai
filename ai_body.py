import os 
from memory import ContextMemory
from dotenv import load_dotenv
from groq import AsyncGroq
import asyncio


class AI_handler:
    def __init__(self,token):           
        self.client = AsyncGroq(api_key = token)
        self.temp_mem = ContextMemory()

    async def generate(self,user_input,chat_id):
        
        history = self.temp_mem.read(chat_id=chat_id)
        user_message = {'role':'user','content':user_input} #adjust input to dict format for write function

        if not history or history[0].get('role') != 'system':
            sys_msg= {
            'role': 'system',
            'content': 'You are telegram bot. You should format your answers as if you writing simple message, dont try to format it to markdown. also your answers cannot exceed telegram message limits'
            }
            self.temp_mem.write(chat_id = chat_id,message=sys_msg)

        self.temp_mem.write(chat_id = chat_id,message=user_message) 

        chat_completions = await self.client.chat.completions.create(
            messages = self.temp_mem.read(chat_id=chat_id),
            model = 'qwen/qwen3-32b',
            reasoning_format='hidden' 
    )
        response = chat_completions.choices[0].message.content
        assistant_response = {
            'role':'assistant',
            'content':response
        }

        self.temp_mem.write(chat_id = chat_id,message=assistant_response) 
        return response


if __name__ ==  '__main__':
    load_dotenv()
    token = os.getenv('GROQ_TOKEN')
    ai = AI_handler(token)
    asyncio.run(ai.generate(input('You: '), chat_id='test user'))
