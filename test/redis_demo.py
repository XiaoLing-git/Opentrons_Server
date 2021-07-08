import redis

r = redis.StrictRedis(host="127.0.0.1", port=6379, decode_responses=True)
print(r["mykey"])