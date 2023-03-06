class Board:
	def __init__(self, board_id, owner_id, board_name, join_code, board_status=None, board_type=None, start_date=None, end_date=None):
		self.board_id = board_id
		self.owner_id = owner_id
		self.board_name = board_name
		self.join_code = join_code
		self.board_status = board_status
		self.board_type = board_type
		self.start_date = start_date
		self.end_date = end_date


	def to_dict(self):
		return {
			'boardName': self.board_name,
			'joinCode': str(self.join_code),
			'boardStatus': self.board_status.value,
			'boardType': self.board_type.value,
			'startDate': self.start_date.timestamp() * 1000 if self.start_date else None, # ms since epoch
			'endDate': self.end_date.timestamp() * 1000 if self.end_date else None
		}