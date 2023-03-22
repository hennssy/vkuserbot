import requests
import os
import json
from threading import Thread
from updates_handler import main
from modules.api_functions import get_params

if not os.path.exists('data.json'):
    with open('data.json', 'w') as f:
        data = {'prefix': '.к', 'allowed_users': [], 'saved_audios': {}}
        f.write(json.dumps(data))

params_flag = True

while True:
    if params_flag:
        key, ts, server_url = get_params()
        params_flag = False
        
    events = requests.post(f'https://{server_url}?act=a_check&key={key}&ts={ts}&wait=50&mode=2&version=3').json()
    
    if 'failed' in events:
        params_flag = True
        continue
    
    updates = events['updates']
    
    if len(updates) == 0:
        ts = events['ts']
        continue
    
    multiprocess = Thread(target = main, args = (updates,))
    multiprocess.start()
    
    ts = events['ts']