from modules.functions import get_id
from modules.api_functions import handle_answer, get_info

def process(message):
    user_id = get_id(message)
    if user_id == None:
        handle_answer(message, 'В сообщении указан неверный ID!')
        return
    
    info_response = get_info(user_id)
    
    text = ''
    profile_status = 'открыт' if info_response['is_closed'] == False else 'закрыт'
    sex = 'женский' if info_response['sex'] == 1 else 'мужской' if info_response['sex'] == 2 else 'не указан'
    
    text += f'Информация о пользователе {info_response["first_name"]} {info_response["last_name"]}:\n' \
        f'- ID: {info_response["id"]}\n' \
        f'- Короткое имя: @{info_response["screen_name"]}\n' \
        f'- Пол: {sex}\n' \
        f'- Профиль: {profile_status}'
    text += f'\n- Друзей: {info_response["counters"]["friends"]}\n- Подписчиков: {info_response["counters"]["followers"]}' if profile_status == 'открыт' else ''
    
    handle_answer(message, text)