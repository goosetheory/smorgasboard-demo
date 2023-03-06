import post_handler
import get_handler
import other_lambda_handler

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

	if 'httpMethod' not in event: # This call comes from another lambda function
		return other_lambda_handler.handle(event, context)
	elif event['httpMethod'] == 'POST':
		return post_handler.handle(event, context)
	elif event['httpMethod'] == 'GET':
		return get_handler.handle(event, context)
	else:
		return base_response