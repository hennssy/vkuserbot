import requests
import os
from modules.functions import get_data, edit_data
from modules.api_functions import edit_message, send_message, del_message, handle_answer
from config import API_URL, TOKEN, OWNER_ID

def process(message):
    attachments = get_data('saved_audios')
    
    cmd_args = message.text.split(maxsplit = 3)[1:]
    command = cmd_args[0].lower()
    
    if command in ['+гс', '-гс'] and message.from_id != OWNER_ID:
        handle_answer(message, 'У вас нет доступа к добавлению или удалению голосовых сообщений!')
        return
    
    if command == 'гс':
        if cmd_args[1] in attachments:
            if cmd_args[2] in attachments[cmd_args[1]]:
                send_message(message.peer_id, '', attachments[cmd_args[1]][cmd_args[2]])
                
                if message.from_id == OWNER_ID:
                    del_message(message.peer_id, [message.message_id])
            else:
                handle_answer(message, f'Такого голосового сообщения нет в категории «{cmd_args[1]}»!')
        else:
            handle_answer(message, f'Категории «{cmd_args[1]}» нет среди сохраненных аудиосообщений!')
    elif command == 'гсы':  
        if len(attachments) == 0:
            text = 'У вас нет сохраненных голосовых сообщений!'
            handle_answer(message, text)
            return
        
        cmd_args = message.text.split(maxsplit = 2)[1:]
        
        text = ''
        if len(cmd_args) == 1:
            text += 'Категории ваших голосовых сообщений: \n'
            for key in attachments.keys():
                text += f'- {key}\n'
        elif len(cmd_args) == 2:
            if cmd_args[1] in attachments:
                text += f'Голосовые сообщения в категории {cmd_args[1]}:\n'
                
                for key in attachments[cmd_args[1]].keys():
                    text += f'- {key}\n'
            else:
                handle_answer(message, f'Категории «{cmd_args[1]}» нет среди сохраненных голосовых сообщений!')
                return
        
        handle_answer(message, text)
            
    if message.from_id == OWNER_ID:
        if command == '-гс':
            if cmd_args[1] in attachments:
                if cmd_args[2] in attachments[cmd_args[1]]:
                    del attachments[cmd_args[1]][cmd_args[2]]
                    
                    if len(attachments[cmd_args[1]]) == 0:
                        del attachments[cmd_args[1]]
                    
                    edit_data('saved_audios', attachments)
                    edit_message(message.peer_id, message.message_id, f'Голосовое сообщение «{cmd_args[2]}» в категории «{cmd_args[1]}» успешно удалено!')
                else:
                    edit_message(message.peer_id, message.message_id, f'Такого голосового сообщения нет в категории «{cmd_args[1]}»!')
            else:
                edit_message(message.peer_id, message.message_id, f'Категории «{cmd_args[1]}» нет среди сохраненных аудиосообщений!')
        elif command == '+гс':
            if message.reply_message != None and message.reply_message.attachments != [] and message.reply_message.attachments[0]['type'] == 'audio_message':
                if len(cmd_args) < 3:
                    edit_message(message.peer_id, message.message_id, 'Необходимо указать категорию и название для сохраняемого аудиособщения!')
                    return
                
                if cmd_args[1] in attachments:
                    if cmd_args[2] in attachments[cmd_args[1]]:
                        edit_message(message.peer_id, message.message_id, f'Голосовое сообщение с названием «{cmd_args[2]}» уже есть в категории «{cmd_args[1]}»!')
                        return
                    elif len(attachments[cmd_args[1]]) == 20:
                        edit_message(message.peer_id, message.message_id, f'Категория «{cmd_args[1]}» переполнена, укажите другое название категории!')
                        return
                
                ogg_response = requests.get(message.reply_message.attachments[0]['audio_message']['link_ogg'])
                
                with open('temp', 'wb') as f:
                    f.write(ogg_response.content)
                
                upload_url = requests.post(f'{API_URL}docs.getMessagesUploadServer?access_token={TOKEN}&type=audio_message&peer_id={message.peer_id}&v=5.131').json()['response']['upload_url']
                
                file = requests.post(upload_url, files = {'file': open('temp', 'rb')}).json()['file']
                os.remove('temp')
                save_response = requests.post(f'{API_URL}docs.save?access_token={TOKEN}&file={file}&v=5.131').json()['response']['audio_message']
                
                if cmd_args[1] not in attachments:
                    attachments[cmd_args[1]] = {}
                attachments[cmd_args[1]][cmd_args[2]] = f'audio_message{save_response["owner_id"]}_{save_response["id"]}_{save_response["access_key"]}'
                edit_data('saved_audios', attachments)
                
                edit_message(message.peer_id, message.message_id, f'Голосовое сообщение успешно сохранено под названием «{cmd_args[2]}» в категории «{cmd_args[1]}»!')
            else:
                edit_message(message.peer_id, message.message_id, 'Необходимо ответить на сообщение с аудиосообщением!')