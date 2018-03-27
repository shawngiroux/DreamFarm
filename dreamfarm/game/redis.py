import redis
import os
import pickle

class Redis:
	conn = None

	@staticmethod
	def initialize():
		host = os.environ.get('REDIS_HOST')
		port = int(os.environ.get('REDIS_PORT'))
		db = int(os.environ.get('REDIS_DB'))

		conn = redis.StrictRedis(host=host, port=port, db=db)
		conn.flushdb()
		Redis.conn = conn

	@staticmethod
	def pstore(key, item, bucket=None):
		if bucket is not None:
			Redis.conn.hset(bucket, key, pickle.dumps(item))
		else:
			Redis.conn.set(key, pickle.dumps(item))

	@staticmethod
	def pget(key, bucket=None):
		if bucket is not None:
			return pickle.loads(Redis.conn.hget(bucket, key))
		else:
			return pickle.loads(Redis.conn.get(key))
