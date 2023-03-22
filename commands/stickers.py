import requests
from modules.functions import get_id, plural_form
from modules.api_functions import handle_answer
from config import STICKER_HEADERS

def process(message):
    user_id = get_id(message)
    if user_id == None:
        handle_answer(message, 'В сообщении указан неверный ID!')
        return
            
    response = requests.get(f'https://stickers.loupg.one/user/{user_id}', headers = STICKER_HEADERS).json()
    
    try:
        text = ''
        name = response["user"]["name"]
        all_count = len(response["all"]["items"]) + len(response["all"]["styles"]["items"])
        sticks = all_count - len(response["all"]["styles"]["items"])
        paid_sticks = len(response["paid"]["items"])
        free_sticks = sticks - paid_sticks
        styles = all_count - sticks
        paid_styles = len(response["paid"]["styles"]["items"])
        free_styles = styles - paid_styles
        rubles_cost = response["paid"]["price"] + response["paid"]["styles"]["price"]
        text += f'{name} имеет всего {plural_form(all_count, ["стикерпак", "стикерпака", "стикерпаков"])}, из них:\n' \
            f'- {plural_form(sticks, ["стикерпак", "стикерпака", "стикерпаков"])}\n' \
            f'ㅤ- {plural_form(paid_sticks, ["платный", "платных", "платных"])}\n' \
            f'ㅤ- {plural_form(free_sticks, ["бесплатный", "бесплатных", "бесплатных"])}\n' \
            f'- {plural_form(styles, ["стиль", "стиля", "стилей"])}\n' \
            f'ㅤ- {plural_form(paid_styles, ["платный", "платных", "платных"])}\n' \
            f'ㅤ- {plural_form(free_styles, ["бесплатный", "бесплатных", "бесплатных"])}\n\n' \
            f'Общая стоимость (в голосах/в рублях): {rubles_cost // 7} / {rubles_cost} ₽'    
    except:
        text = 'Неверный ID!'
    
    handle_answer(message, text)