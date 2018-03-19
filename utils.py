from wit import Wit
from gnewsclient import gnewsclient

access_token = "KZK5THS2X4KO4C5OWJFGHSFAEC2Z6GBO"

client = Wit(access_token = access_token)

def wit_response(message_text):
	resp = client.message(message_text)
	categories = {'saludo':None, 'quetal':None, 'message':None, 'rodoso':None, 'orden':None, 'agradecimiento':None, 'deporte':None, 'peticion':None}

	entities=list(resp['entities'])

	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']

	return categories

def get_response_message(categories):
	message = []
	if categories['saludo'] != None:
		message.append('saludo')

	if categories['quetal'] != None:
		message.append('quetal')

	if categories['message'] != None:
		message.append('message')

	if categories['orden'] != None:
		message.append('orden')

	if categories['agradecimiento'] != None:
		message.append('agradecimiento')

	if categories['deporte'] != None:
		message.append('deporte')

	if categories['peticion'] != None:
		message.append('peticion')

	return message


def get_translated_action(categories):
	actions = []
	if categories['saludo'] != None:
		actions.append(categories['orden'])

	if categories['quetal'] != None:
		actions.append('greet')

	if categories['orden'] != None:
		actions.append(categories['orden'])

	if categories['agradecimiento'] != None:
		actions.append('greet')

	if categories['deporte'] != None:
		actions.append('deporte')

	if categories['peticion'] != None:
		actions.append('peticion')


	return actions


def get_news_elements(categories):
	news_client = gnewsclient()
	news_client.query = ''

	if categories['location'] != None:
		news_client.query += categories['location']


	if categories['newstype'] != None:
		news_client.query += categories['newstype'] + ' '



	news_items = news_client.get_news()
	elements = []

	if news_items is NoneType:
		return elements.append('naita')
	else:
		for item in news_items:
			element = {
						'title': item['title'],
						'buttons': [{
									'type': 'web_url',
									'title': "Read more",
									'url': item['link']
						}],
						'image_url': item['img']
			}
			elements.append(element)

	return elements

#print(get_news_elements(wit_response("I want sports news in India")))
