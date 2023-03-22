import json
from modules.api_functions import get_info

def get_data(key):
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
        
    return data.get(key)

def edit_data(key, new_data):
    with open('data.json', 'r') as f:
        data = json.loads(f.read())
    
    data[key] = new_data
    
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))        

def get_id(message):
    if message.reply_message != None:
        return message.reply_message.from_id
    else:
        if len(message.text.split()) < 3:
            user_id = message.from_id
        else:
            user_id = message.text.split()[2]
            
            if '@' in user_id and '|' in user_id:
                user_id = user_id.split('|')[1].replace('@', '').replace(']', '')
            else:
                return None
    
    return get_info(user_id)['id']

def plural_form(amount, variants):
    amount = abs(amount)

    if amount % 10 == 1 and amount % 100 != 11:
        variant = 0
    elif 2 <= amount % 10 <= 4 and (amount % 100 < 10 or amount % 100 >= 20):
        variant = 1
    else:
        variant = 2

    return f"{amount} {variants[variant]}"