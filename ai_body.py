import os 
from memory import ContextMemory
from dotenv import load_dotenv
from groq import AsyncGroq
import asyncio


class AI_handler:
    def __init__(self):
        load_dotenv()
        helper_api = os.getenv('HELPER_API')
        main_api =os.getenv('GROQ_TOKEN')
        self.helper_client = AsyncGroq(api_key=helper_api)          
        self.client = AsyncGroq(api_key=main_api)
        self.temp_mem = ContextMemory()

    async def generate(self,user_input,chat_id):
        
        history = self.temp_mem.read(chat_id=chat_id)
        if len(history) >= 9:
            await self.create_context(chat_id=chat_id)

        user_message = {'role':'user','content':user_input} #adjust input to dict format for write function

        if not history or history[0].get('role') != 'system':
            sys_msg= {
            'role': 'system',
            'content': 'You are telegram bot. You should format your answers as if you writing simple message unless user askes otherwise, dont try to format it to markdown or use symbols like * etc. also your answers cannot exceed telegram message limits'
            }
            self.temp_mem.write(chat_id = chat_id,message=sys_msg)

        self.temp_mem.write(chat_id = chat_id,message=user_message) 

        chat_completions = await self.client.chat.completions.create(
            messages = self.temp_mem.read(chat_id=chat_id),
            model = 'qwen/qwen3-32b',
            #reasoning_format='hidden' need it only for qwen3
    )
        response = chat_completions.choices[0].message.content
        assistant_response = {
            'role':'assistant',
            'content':response
        }

        self.temp_mem.write(chat_id = chat_id,message=assistant_response) 
        return response

    async def create_context(self,chat_id):   #helper bot
        system_prompt = """
You are a conversation summarizer. Your task is to compress a conversation history into a SHORT, information-dense context summary.

RULES:
1. Maximum length: 300-500 tokens
2. Write in English (even if conversation is in other languages)
3. Focus on KEY INFORMATION only
4. Include what was discussed, decided, and still pending
5. Preserve technical details, names, numbers, and specific requests
6. Note user's preferences and communication style
7. DO NOT include greetings, small talk, or redundant information

FORMAT YOUR SUMMARY AS:
Topic: [Main subject of conversation]
Key Points:
- [Most important point 1]
- [Most important point 2]
- [etc., max 5-7 points]

Decisions/Solutions:
- [What was decided or solved]

User Preferences:
- [Any preferences user mentioned: language, style, specific requirements]

Pending/Unresolved:
- [Questions not answered, tasks not completed]

Technical Details:
- [Important code, commands, configurations, model names, etc.]

Context Notes:
- [Any other critical context needed to continue the conversation naturally]
"""
        chat = self.temp_mem.read(chat_id=chat_id)
        to_compress = chat[1:-2]

        handled_context = await self.helper_client.chat.completions.create(
            messages = [
                {
                    'role':'system',
                    'content':system_prompt
                },
                {
                    'role':'user',
                    'content':str(to_compress)  
                }
            ],
            model = 'openai/gpt-oss-120b',
            temperature = 0.3,
            max_completion_tokens = 600) 
        
        response = handled_context.choices[0].message.content
        assistant_response = {
            'role':'system',
            'content':response
        }

        self.temp_mem.rewrite(chat_id = chat_id,messages=[chat[0],assistant_response]+chat[-2:]) 



if __name__ ==  '__main__':
    ai = AI_handler()
    asyncio.run(ai.generate(input('You: '), chat_id='test user'))







#sysprom 'content': 
'''You are a telegram bot. 

IMPORTANT: 
- For current info (news, weather, prices, events), use search_web tool
- If you search and find no clear results, say "I couldn't find information about that"
- NEVER make up facts about people, especially non-famous individuals
- If you're unsure, admit it instead of guessing'''