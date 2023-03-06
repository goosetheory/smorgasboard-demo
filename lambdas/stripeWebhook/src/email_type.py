from enum import Enum

class EmailType(Enum):
	ON_JOIN = 1
	ON_PAY_FOR_BOARD = 2
	ON_BOARD_START = 3
	ON_BOARD_END = 4
	ON_FREE_TRIAL_END = 5