import json
from pathlib import Path
from datetime import datetime


class ContextMemory:
    def __init__(self):
        dir = Path.cwd() #way where is the execute file
        self.users_folder = dir/'users' #reaches to all the stored users
        self.users_folder.mkdir(exist_ok = True)
        

    def create_user_folder(self,id): 
        self.user = self.users_folder / f'{id}'
        self.user.mkdir(exist_ok = True) #if exist - does nothing

    def read(self,chat_id) -> list[dict[str,str]]:
        self.create_user_folder(chat_id)
        history = []
        try:
            with (self.user / 'context.jsonl').open('r',encoding='utf-8') as context_json:
                content = context_json.readlines()

                for line in content:
                    if line.strip():
                        message = json.loads(line)
                        message.pop('time',None)
                        history.append(message) 
        except FileNotFoundError:
            return history
        return history
            
    def write(self,chat_id,message):#expects dict for message
        self.create_user_folder(chat_id)
        message['time'] = datetime.now().isoformat()
        with (self.user / 'context.jsonl').open('a+',encoding='utf-8') as context_json:
            json.dump(message,context_json,ensure_ascii=False)
            context_json.write('\n')

    def rewrite(self,chat_id,messages):#will take list and convert it to dict
        self.create_user_folder(chat_id)
        with (self.user / 'context.jsonl').open('w',encoding='utf-8') as context_json:
            for message in messages:  # Loop through each message
                message_copy = message.copy()  # Don't modify original dict
                message_copy['time'] = datetime.now().isoformat()
                json.dump(message_copy,context_json,ensure_ascii=False)
                context_json.write('\n')


