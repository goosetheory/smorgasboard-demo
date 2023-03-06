from json import JSONEncoder
import json

class MembershipPublic(JSONEncoder):
	def __init__(self, board_name, join_code, cognito_username, given_name, status, join_date):
		self.board_name = board_name
		self.join_code = join_code
		self.cognito_username = cognito_username
		self.given_name = given_name
		self.status = status
		self.join_date = join_date

	def to_json(self):
		return {
			'boardName': self.board_name,
			'joinCode': self.join_code,
			'cognitoUsername': self.cognito_username,
			'givenName': self.given_name,
			'status': self.status,
			'joinDate': self.join_date.timestamp() * 1000 # ms since epoch
		}