import os, sys
from flask import Flask, request
from utils import wit_response, get_response_message, get_translated_action, get_news_elements
from pymessenger import Bot

app = Flask(__name__)
one = 0
jamala = '1557317664386664'
bot_id = '897695543743171'


PAGE_ACCESS_TOKEN = "EAAEGgHE2HqsBACcxBhVaejIKhe9ovXabfs6842IuAgz5w5lgjZAdOJNL2zB5lOySFDszCZAHOQfULiyvjXrg8S8MeOWZAJuMWpYz1QcRKmZA6L5arp7i7MysEdKzu8vWQsCLQs8UYsN62jtZCTYs8tavZBjdRB313jFFVGAlliQQZDZD"


bot = Bot(PAGE_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
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
                # IDs
                    sender_id = messaging_event['sender']['id']
                    recipient_id = messaging_event['recipient']['id']
                    if messaging_event.get('message'):
                        if sender_id == jamala or recipient_id == jamala or sender_id == bot_id:
                            pass
                        else:
                            # Extracting text message
                            respond(messaging_event, sender_id, recipient_id, jamala)
    return 'ok', 200
                       
                            
def respond(messaging_event, sender_id, recipient_id, jamala):

    if sender_id == jamala or recipient_id == jamala or sender_id == bot_id:
        pass
    else:
        if 'text' in messaging_event['message']:
            messaging_text = messaging_event['message']['text']
        else:
            messaging_text = 'no text'

        categories = wit_response(messaging_text)
        response_messages = get_response_message(categories)
        actions = get_translated_action(categories)
        print('aqui van')
        print(response_messages)
        print(actions)

        for response_message, action in zip(response_messages, actions):
            if response_message == 'saludo':
                if(action == 'adios'):
                    bot.send_text_message(sender_id, '¡Hasta la vista!')
                else:
                    bot.send_text_message(sender_id, '¡Hola!')

                bot.send_text_message(jamala, 'wave left hand')

            if response_message == 'quetal':
                bot.send_text_message(sender_id, 'Yo estoy muy bien, ¿y tu?')
                bot.send_text_message(jamala, action)

            if response_message == 'rodoso':
                pass  

            if response_message == 'agradecimiento':

                bot.send_text_message(sender_id, 'De nada.')
                bot.send_text_message(jamala, action) 

            if(response_message == 'deporte'):
                    bot.send_text_message(sender_id, 'Soy el mejor Karateka.')
                    bot.send_text_message(jamala, 'Left kick')

            if(response_message == 'peticion'):
                    bot.send_text_message(sender_id, '¡Claro!')


            if response_message == 'orden':
                if(action == 'sientate'):
                    bot.send_text_message(sender_id, 'Sentadito me quedé.')
                    bot.send_text_message(jamala, 'sit')
                if(action == 'baila'):
                    bot.send_text_message(sender_id, '¡Que alguien suba la música!')
                    bot.send_text_message(jamala, 'dance')
                if(action == 'arriba'):
                    bot.send_text_message(sender_id, '¡Arriba!')
                    bot.send_text_message(jamala, 'stand up')
                if(action == 'ejercicio'):
                    bot.send_text_message(sender_id, 'Esto no me cuesta nada.')
                    bot.send_text_message(jamala, 'push up')



        #elements = get_news_elements(categories)
        #print(type(sender_id))

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug = True, port = 80)

