import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot

app = Flask(__name__)



PAGE_ACCESS_TOKEN = "EAAEGgHE2HqsBACcxBhVaejIKhe9ovXabfs6842IuAgz5w5lgjZAdOJNL2zB5lOySFDszCZAHOQfULiyvjXrg8S8MeOWZAJuMWpYz1QcRKmZA6L5arp7i7MysEdKzu8vWQsCLQs8UYsN62jtZCTYs8tavZBjdRB313jFFVGAlliQQZDZD"

bot = Bot(PAGE_ACCESS_TOKEN)



@app.route('/', methods =['GET'])
def verify():
    
        if request.args.get("hub.mode") == "subscribe" and            request.args.get("hub.challenge"):
            if not request.args.get("hub.challenge"):
                return "Verification token mismatch", 403
            return request.args["hub.challenge"], 200
        return "Hello world", 200
    
    
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)
    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:
                
                #IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']
                
                #Check message type
                if messaging_event.get('message'):
                    if 'text' in messaging_event['message']:
                        messaging_text  = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'
            
                    #Echo
                    response = None

                    entity, value = wit_response(messaging_text)

                    if entity == 'newstype':
                    	response = "Ok I will send you {} news".format(srt(value))
                    elif entity == "location":
                    	response = "Ok. So, you live in {0}. I will send you top headlines from {0}".format(str(value))
                    
                    if response == None :
                        response = "Sorry I didn't understand!"

                    bot.send_text_message(sender_id, response) 

    
    return "ok", 200
    
def log(message):
    print(message)
    sys.stdout.flush()
    
if __name__ == "__main__":
    app.run(debug= True, port = 80)
