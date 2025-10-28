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
        with (self.user / 'context.jsonl').open('a+',encoding='utf-8') as context_json:
            context_json.seek(0)
            content = context_json.readlines()

            for line in content:
                if line.strip():
                    history.append(json.loads(line))
        return history
            
    def write(self,chat_id,message):
        self.create_user_folder(chat_id)
        message['time'] = datetime.now().isoformat()
        with (self.user / 'context.jsonl').open('a+',encoding='utf-8') as context_json:
            json.dump(message,context_json)
            context_json.write('\n')
