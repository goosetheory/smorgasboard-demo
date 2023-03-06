class Photo:
	def __init__(self, photo_key, s3_bucket_name, s3_object_key, board_add_date, uploader_username, board_photo_status):
		self.photo_key = photo_key
		self.s3_bucket_name = s3_bucket_name
		self.s3_object_key = s3_object_key
		self.board_add_date = board_add_date
		self.uploader_username = uploader_username
		self.board_photo_status = board_photo_status
		self.url = None

	def set_url(self, url):
		self.url = url

	def to_dict(self):
		return {
			'photoKey': str(self.photo_key),
			's3BucketName': self.s3_bucket_name,
			's3ObjectKey': self.s3_object_key,
			'boardAddDate': self.board_add_date.timestamp() * 1000, # ms since epoch
			'uploaderCognitoUsername': self.uploader_username,
			'boardPhotoStatus': self.board_photo_status,
			'url': self.url
		}
