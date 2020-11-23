import redis
import json

class redis_client():
    def __init__(self, host, port):
        self.conn = redis.Redis(host=host, port=port, db=0)

    def save_dict(self, key, data_dict):
        json_dict = json.dumps(data_dict)
        result = self.conn.set(key, json_dict)
        print(result)
        return result