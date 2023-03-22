import requests
import config
from random import randint

def get_info(id):
    response = requests.post(f'{config.API_URL}/users.get?access_token={config.TOKEN}&user_ids={id}&fields=counters,screen_name,sex&v=5.131').json()['response'][0]
    
    return response

def edit_message(peer_id, message_id, text):
    requests.post(f'{config.API_URL}/messages.edit?access_token={config.TOKEN}&peer_id={peer_id}&message={text}&message_id={message_id}&keep_forward_messages=1&v=5.131')
    
def send_message(peer_id, text, attach = None):
    requests.post(f'{config.API_URL}/messages.send?access_token={config.TOKEN}&random_id={randint(1, 10000)}&peer_id={peer_id}&message={text}&attachment={attach}&v=5.131')
    
def del_message(peer_id, message_ids):
    requests.post(f'{config.API_URL}/messages.delete?access_token={config.TOKEN}&peer_id={peer_id}&message_ids={str(message_ids)[1:len(str(message_ids))-1].replace(" ", "")}&delete_for_all=1&v=5.131')
    
def handle_answer(message, text):
    if message.from_id == config.OWNER_ID:
        edit_message(message.peer_id, message.message_id, text)
    else:
        send_message(message.peer_id, text)
        
def get_params():
    response = requests.post(f'{config.API_URL}messages.getLongPollServer?access_token={config.TOKEN}&lp_version=3&v=5.131').json()['response']
    key, ts, server_url = response['key'], response['ts'], response['server']
    
    return key, ts, server_url