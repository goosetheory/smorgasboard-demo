import get_handler

def handler(event, context):
	print('received event:')
	print(event)
	base_response = {
			'headers': {
				'Access-Control-Allow-Headers': '*',
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
			},
			'body': "This method is not supported."
		}

	if event['httpMethod'] == 'GET':
		return get_handler.handle(event, context)
	else:
		return base_response