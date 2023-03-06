from s3_client import S3Client

class Archive:
	def __init__(self, create_date, shard_infos):
		# Shards is a list of tuples of the form (s3_bucket_name, s3_object_key)
		self.create_date = create_date
		self.shard_infos = shard_infos
		self.shard_urls = None
		self.s3_client = S3Client()

	def to_dict(self):
		if not self.shard_urls:
			self.populate_urls()
		return {
			'createDate': self.create_date,
			'shards': [{ 'url': url } for url in self.shard_urls]
		}

	def populate_urls(self):
		self.shard_urls = []
		for bucket_name, object_key in self.shard_infos:
			shard_url = self.s3_client.get_object(bucket, object_key)
			self.shard_urls.append(shard_url)