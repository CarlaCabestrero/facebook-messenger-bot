from wit import Wit
from gnewsclient import gnewsclient

access_token = "6WHOSJPFPMFLSL4PQWVPL5RHWATOGZ7Q"

client = Wit(access_token = access_token)

def wit_response(message_text):
	resp = client.message(message_text)
	categories = {'newstype':None, 'location':None}

	entities=list(resp['entities'])

	for entity in entities:
		categories[entity] = resp['entities'][entity][0]['value']

	return categories

def get_news_elements(categories):
	news_client = gnewsclient()
	news_client.query = ''

	if categories['location'] != None:
		news_client.query += categories['location']


	if categories['newstype'] != None:
		news_client.query += categories['newstype'] + ' '


	news_items = news_client.get_news()
	elements = []

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