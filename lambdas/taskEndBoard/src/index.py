import logging
import http

import queries
from lambda_client import LambdaClient
from board_type import BoardType

logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda_client = LambdaClient()

def handler(event, context):
	logger.info('received event:')
	logger.info(event)
	response = {
		'headers': {
			'Access-Control-Allow-Headers': '*',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT'
		},
		'statusCode': http.HTTPStatus.OK
	}

	join_code, board_type_id = queries.get_first_expired_board()

	if not join_code:
		logger.info('No expired boards found. Bailing out.')
		return response

	logger.info(f'Ending board (join code: {str(join_code)}, type: {str(board_type_id)}')
	if board_type_id == BoardType.FREE_TRIAL:
		_mark_board_complete(join_code)
		lambda_client.send_free_trial_end_email(join_code)
	else:
		success = lambda_client.create_archive(join_code)
		_mark_board_complete(join_code)
		if not success:
			logger.error('Unable to create archive. Manual intervention needed.')
			response['statusCode'] = http.HTTPStatus.INTERNAL_SERVER_ERROR
			return response
		logger.info('Archive created.')

		lambda_client.send_board_end_email(join_code)

	return response


def _mark_board_complete(join_code):
	logger.info(f'Marking board {str(join_code)} complete...')
	queries.mark_board_completed(join_code)
	logger.info(f'Marked board complete.')