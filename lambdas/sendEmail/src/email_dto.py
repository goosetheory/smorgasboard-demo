class EmailDTO:
	def __init__(self, recipient, subject, body_text, body_html):
		self.recipient = recipient
		self.subject = subject
		self.body_text = body_text
		self.body_html = body_html
		self.sent = False
		self.message_id = None

	def set_message_id(self, message_id):
		self.message_id = message_id