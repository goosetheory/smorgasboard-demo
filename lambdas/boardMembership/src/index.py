import post_handler
import get_handler
import http

def handler(event, context):
	print('received event:')
	print(event)

	if event['httpMethod'] == 'GET':
		return get_handler.handle(event, context)
	elif event['httpMethod'] == 'POST':
		return post_handler.handle(event, context)
	else:
		return {
			'statusCode': http.HTTPStatus.METHOD_NOT_ALLOWED,
			'headers': {
				'Access-Control-Allow-Headers': '*',
				'Access-Control-Allow-Origin': '*',
				'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
			},
			'body': "This method is not supported."
		}
