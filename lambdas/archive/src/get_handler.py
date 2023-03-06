import uuid
import json
import http
import queries
import logging

from s3_client import S3Client

s3_client = S3Client()


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}

	try:
		cognito_username = event['requestContext']['authorizer']['claims']['cognito:username']
	except:
		logger.info('No username.')
		cognito_username = None

	join_code = _parse_args(event)

	unauthorized_message = _validate_authorization(cognito_username, join_code)
	if unauthorized_message:
		response['statusCode'] = http.HTTPStatus.FORBIDDEN
		response['body'] = unauthorized_message
		return response

	return get_archive(join_code, response)


def get_archive(join_code, response):
	archive_info = queries.get_archive_info(join_code)
	logger.info('Archive info: ' + str(archive_info))
	if not archive_info:
		logger.error(f'Could not find archive for join code {str(join_code)}')
		response['statusCode'] = http.HTTPStatus.UNPROCESSABLE_ENTITY
		return response

	# First shard will be None if archive has no shards (possible when no photos were taken)
	first_shard_bucket_name, first_shard_object_key = archive_info[0]
	if not first_shard_bucket_name:
		body = {
			'shards': []
		}
	else:
		urls = []
		for bucket_name, object_key in archive_info:
			url = s3_client.get_presigned_url(bucket_name, object_key)
			urls.append(url)

		body = {
			'shards': [{
				'url': url
			} for url in urls]
		}

	response['body'] = json.dumps(body)
	response['statusCode'] = http.HTTPStatus.OK
	return response


def _validate_authorization(cognito_username, join_code):
	board_owner_username = queries.get_board_owner_username(join_code)
	if board_owner_username != cognito_username:
		return 'Only the owner of this board can see an archive.'
	else:
		return None


def _parse_args(event):
	join_code = uuid.UUID(event['queryStringParameters']['joinCode'])
	return join_code
