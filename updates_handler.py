import config
from modules.message import Message
from modules.functions import get_data, edit_data
from modules.api_functions import edit_message
from commands import *

def main(updates):
    for update in updates:
        if update[0] == 4:
            message = Message(update[1])
            
            if message.text == '' or message.text.split()[0] not in [get_data('prefix'), '.кк']:
                continue
            
            allowed_users = get_data('allowed_users')
            if message.from_id not in allowed_users and message.from_id != config.OWNER_ID:
                continue
            
            # message.text = /к[0] преф[1] .привет[2]
            cmd_args = message.text.split()[1:]
            
            if len(cmd_args) == 0:
                handle_answer(message, 'Необходимо ввести команду!')
                continue
            
            command = cmd_args[0].lower()
            
            if message.from_id == config.OWNER_ID:
                if command == 'преф':
                    if len(cmd_args) < 2:
                        edit_message(message.peer_id, message.message_id, 'Необходимо ввести префикс для изменения!')
                        continue
                    
                    edit_data('prefix', cmd_args[1])
                    edit_message(message.peer_id, message.message_id, f'Префикс успешно изменен на «{cmd_args[1]}»!')
                elif command in ['+доступ', '-доступ', '!доступ']:
                    access_control.process(message)
                
            if command == 'стикеры':
                stickers.process(message)
            elif command == 'инфо':
                user_information.process(message)
            elif command in ['гс', 'гсы', '-гс', '+гс']:
                audios.process(message)