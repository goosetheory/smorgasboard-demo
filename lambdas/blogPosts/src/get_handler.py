import urllib.request
import json
import http
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)



logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASE_URL = 'https://public-api.wordpress.com/rest/v1.1/sites/trysmorgasboard.wordpress.com'

def handle(event, context):
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
	}

	try:
		slug = _parse_args(event)
	except:
		logging.exception('Bad request.')
		response['statusCode'] = http.HTTPStatus.BAD_REQUEST
		return response

	logger.info(f'Found slug: {str(slug)}')

	if slug:
		return _get_specific_post(slug, response)
	else:
		return _get_list_of_posts(response)


def _get_list_of_posts(response):
	all_posts = _get_all_posts()
	response['body'] = json.dumps(all_posts)
	response['statusCode'] = http.HTTPStatus.OK
	logger.info('Returning all posts.')
	return response


def _get_specific_post(slug, response):
	all_posts = _get_all_posts()
	for post in all_posts['posts']:
		if (post['slug'] == slug):
			logger.info('Returning specified post.')
			response['statusCode'] = http.HTTPStatus.OK
			response['body'] = json.dumps(post)
			return response
	# If post not found
	logger.error('Post not found.')
	response['statusCode'] = http.HTTPStatus.BAD_REQUEST
	return response


def _get_all_posts():
	url = BASE_URL + '/posts'
	with urllib.request.urlopen(url) as wp_response:
		return json.loads(wp_response.read().decode('utf-8', 'replace'))

def _parse_args(event):
	params = event.get('queryStringParameters')
	if not params or params == 'None':
		return None
	logger.info(f'params: {str(params)}')
	slug = params.get('slug', None)
	return slug