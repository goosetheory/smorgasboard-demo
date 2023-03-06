import time
import math
import logging
import io
import zipfile
import uuid

from concurrent.futures import ThreadPoolExecutor

from s3_client import S3Client

NUM_WORKERS = 10
ARCHIVES_PATH = 'archives/'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_photo_contents_in_batch(s3_client, batch, result_photo_keys_and_contents):
	logger.info(f'Starting thread with batch of length {str(len(batch))}')
	try:
		for bucket, key in batch:
			logger.info(f'Retrieving {str(key)}...')
			photo_content = s3_client.get_object(bucket, key)
			result_photo_keys_and_contents.append((key, photo_content))
			logger.info(f'Finished retrieving {str(key)}.')
		logger.info('Worker finished processing.')
	except Exception as e:
		logging.exception('Could not process batch in thread.')
		raise e

class CompressionLeader:
	def __init__(self):
		self.s3_client = S3Client()

	def compress_shard(self, photos_in_shard):
		uncompressed_photo_contents = self.get_photo_contents(photos_in_shard)

		logger.info(f'Len contents: {str(len(uncompressed_photo_contents))}')
		if len(uncompressed_photo_contents) != len(photos_in_shard):
			logger.error('Could not get all photos from S3. Manual intervention required.')
			raise Exception('Could not get all photos from S3.')

		zip_buffer = io.BytesIO()
		logger.info('Creating shard.')
		with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zipper:
			for object_key, photo_content in uncompressed_photo_contents:
				logger.info(f'Adding {str(object_key)} to zip file...')
				zipper.writestr(object_key, photo_content)
				logger.info('Added.')

		# Join into a shard
		filename = ARCHIVES_PATH + str(uuid.uuid4()) + '.zip'

		# Upload shard to S3
		logger.info('Uploading zip file...')
		self.s3_client.put_file(filename, zip_buffer.getvalue())
		logger.info('Uploaded.')

		return filename

	def get_photo_contents(self, photos_in_shard):
		batch_size = math.ceil(len(photos_in_shard) / NUM_WORKERS)
		batches = []
		for i in range(NUM_WORKERS):
			batch = photos_in_shard[:batch_size]
			photos_in_shard = photos_in_shard[batch_size:]
			batches.append(batch)
			logger.info(f'batch size: {str(len(batch))}')

		photo_keys_and_contents = []
		futures = []
		with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
			for batch in batches:
				s3_client = S3Client()
				s3_client.eager_init()
				logger.info(f'Starting batch of size {str(len(batch))}')
				future = executor.submit(get_photo_contents_in_batch, s3_client, batch, photo_keys_and_contents)
				futures.append(future)

		for future in futures:
			exc = future.exception(timeout=0)
			if exc:
				logger.error(f'Error executing thread: {str(exc)}')
		return photo_keys_and_contents


