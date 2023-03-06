import get_handler
import post_handler
import other_lambda_handler
import http

def handler(event, context):
	print('received event:')
	print(event)

	if 'httpMethod' not in event: # This call comes from another lambda function
		return other_lambda_handler.handle(event, context)
	elif event['httpMethod'] == 'POST':
		return post_handler.handle(event, context)
	elif event['httpMethod'] == 'GET':
		return get_handler.handle(event, context)
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
