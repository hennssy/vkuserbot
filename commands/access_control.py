from modules.functions import get_data, edit_data, get_id
from modules.api_functions import handle_answer, get_info
from config import OWNER_ID

def process(message):
    user_id = get_id(message)
    user_info = get_info(user_id)
    name, surname = user_info['first_name'], user_info['last_name']
    
    data = get_data('allowed_users')
    
    operation_type = message.text.split()[1][0]
    if user_id == OWNER_ID and operation_type != '!':
        handle_answer(message, 'Вы не можете настроить доступ самому себе!')
        return    
    
    if operation_type == '+':
        if user_id not in data:
            data.append(user_id)
            text = f'Доступ успешно выдан пользователю «{name} {surname}»!'
        else:
            text = f'У пользователя «{name} {surname}» уже есть доступ к вашему боту!'
    elif operation_type == '-':
        if user_id in data:
            data.remove(user_id)
            text = f'Пользователь «{name} {surname}» лишился доступа к вашему боту!'
        else:
            text = f'У пользователя «{name} {surname}» нет доступа!'
    elif operation_type == '!':
        if len(data) != 0:
            text = 'Вы выдали доступ следующим людям:\n'
            for user in data:
                user_info = get_info(user)
                text += f'{user} - {user_info["first_name"]} {user_info["last_name"]}\n'
        else:
            text = 'Никто не имеет доступа к вашему боту!'
        
    edit_data('allowed_users', data)
    handle_answer(message, text)