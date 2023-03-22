import requests
from config import TOKEN, API_URL

class Message:
    def __init__(self, message_id):
        self.message_id = message_id
        response = requests.post(f'{API_URL}messages.getById?access_token={TOKEN}&message_ids={message_id},&v=5.131').json()['response']['items'][0]
        self.from_id = response['from_id']
        self.peer_id = response['peer_id']
        self.attachments = response['attachments']
        self.conver_id = response['conversation_message_id']
        self.text = response['text']
        self.reply_message = None
        
        if response.get('reply_message') != None:
            self.reply_message = ReplyMessage(response['reply_message'])
        
class ReplyMessage:
    def __init__(self, message):
        self.from_id = message['from_id']
        self.text = message['text']
        self.message_id = message['id']
        self.conver_id = message['conversation_message_id']
        self.attachments = message['attachments']